import logging

from django.contrib import messages
from django.shortcuts import render, redirect

from githubissues.models import Repository, User, Issue
from githubissues.service.github_api_operation import GithubApiOperation


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        github_username = request.POST.get('github_username')
        github_email = request.POST.get('github_email')
        user = GithubApiOperation.add_user_or_update(github_username, github_email)

        if user:
            request.session['github_username'] = user.github_username
            request.session['github_email'] = user.email
            return redirect('dashboard')
        else:
            messages.error(request, 'The username does not exist')
            return render(request, 'login.html', {'github_username': github_username, 'github_email': github_email})

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')


def dashboard(request):
    if not request.session.get('github_username'):
        return redirect('login')

    user = User.objects.filter(github_username=request.session['github_username']).first()
    repository_list = GithubApiOperation.add_or_update_repo(user)
    repositories_size = len(repository_list)

    total_issues = 0
    open_issues = 0
    closed_issues = 0

    issue_list = []
    rate_limit = GithubApiOperation.get_rate_limit()
    db_repository_list = Repository.objects.all()

    for repo in db_repository_list:
        issues = GithubApiOperation.fetch_and_store_issues(user.github_username, repo.repo_id)
        issue_list.extend(issues)
        total_issues += len(issues)

        for issue in issues:
            if issue.state == 'open':
                open_issues += 1
            elif issue.state == 'closed':
                closed_issues += 1
    context = {
        'repository_list': repository_list,
        'repositories_size': repositories_size,
        'rate_limit': rate_limit,
        'issue_list': issue_list,
        'total_issues': total_issues,
        'open_issues': open_issues,
        'closed_issues': closed_issues,
    }

    return render(request, 'dashboard.html', context)


def reopen_issue(request, issue_id):
    if not request.session.get('github_username'):
        return redirect('login')

    user = User.objects.filter(github_username=request.session['github_username']).first()

    try:
        issue = Issue.objects.get(issue_id=issue_id)
        repository = Repository.objects.get(id=issue.repository_id)

        if issue.state == 'closed':
            success = GithubApiOperation.reopen_github_issue(user.github_username, repository, issue)

            if success:
                issue.state = 'open'
                issue.save()
                print('The issue was reopened successfully.')
                return redirect('dashboard')
            else:
                logging.error('Failed to reopen the issue.')
                print('Failed to reopen the issue.')
    except Issue.DoesNotExist:
        logging.error('Issue does not exist.')
        print('Issue does not exist.')

    return redirect('open_issues')


def close_issue(request, issue_id):
    if not request.session.get('github_username'):
        return redirect('login')

    user = User.objects.filter(github_username=request.session['github_username']).first()

    try:
        issue = Issue.objects.get(issue_id=issue_id)
        repository = Repository.objects.get(id=issue.repository_id)

        if issue.state == 'open':
            success = GithubApiOperation.close_github_issue(user.github_username, repository, issue)

            if success:
                issue.state = 'closed'
                issue.save()
                print('The issue was closed successfully.')
                return redirect('dashboard')
            else:
                logging.error('Failed to close the issue.')
                print('Failed to close the issue.')
    except Issue.DoesNotExist:
        logging.error('Issue does not exist.')
        print('Issue does not exist.')

    return redirect('close_issues')


def open_issues_view(request):
    if not request.session.get('github_username'):
        return redirect('login')

    repository_list = Repository.objects.all()
    issues = None

    if request.method == 'POST':
        repo_id = request.POST.get('repo')
        try:
            repository = Repository.objects.get(id=repo_id)
            issues = Issue.objects.filter(repository=repository, state='open')
        except Repository.DoesNotExist:
            issues = []

    context = {
        'repository_list': repository_list,
        'issues': issues,
    }

    return render(request, 'open_issues.html', context)


def close_issues_view(request):
    if not request.session.get('github_username'):
        return redirect('login')

    repository_list = Repository.objects.all()
    issues = None

    if request.method == 'POST':
        repo_id = request.POST.get('repo')
        try:
            repository = Repository.objects.get(id=repo_id)
            issues = Issue.objects.filter(repository=repository, state='closed')
        except Repository.DoesNotExist:
            issues = []

    context = {
        'repository_list': repository_list,
        'issues': issues,
    }

    return render(request, 'close_issues.html', context)


def create_issues_view(request):
    if not request.session.get('github_username'):
        return redirect('login')

    user = User.objects.filter(github_username=request.session['github_username']).first()
    repository_list = Repository.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        labels = request.POST.get('labels')
        repository_name = request.POST.get('repository')

        repository = Repository.objects.filter(name=repository_name).first()

        if repository:
            issue_created = GithubApiOperation.create_github_issue(
                user.github_username, repository.repo_id, title, description, labels)

        return redirect('dashboard')

    context = {
        'repository_list': repository_list,
    }

    return render(request, 'create_issues.html', context)
