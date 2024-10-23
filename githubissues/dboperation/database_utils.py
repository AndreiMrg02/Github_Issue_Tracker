import logging

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from githubissues.models import User, Repository, Issue


class DatabaseUtils:

    @staticmethod
    def get_or_create_github_user_db(github_username, email=None):
        try:
            logging.info(f"User was updated {github_username}")
            user = User.objects.get(github_username=github_username)
            user.last_connection = timezone.now()
            user.save()
            return user
        except ObjectDoesNotExist:
            logging.info(f"User was created {github_username}")
            user = User.objects.create(
                github_username=github_username,
                email=email,
                last_connection=timezone.now()
            )
            user.save()
            return user

    @staticmethod
    def add_or_update_repo(repository):
        try:
            # Try to find the repository by repo_id and update it if it exists
            repository_db = Repository.objects.get(repo_id=repository.repo_id)
            logging.info(f"Repository with ID {repository.repo_id} was updated in db")

            if repository_db:
                # Update the repository details
                repository_db.repo_id = repository.repo_id
                repository_db.created_at = repository.created_at
                repository_db.opened_issues = repository.opened_issues
                repository_db.owner = repository.owner
                repository_db.git_link = repository.git_link
                repository_db.name = repository.name
                repository_db.pushed_at = repository.pushed_at
                repository_db.language = repository.language
                repository_db.has_issues = repository.has_issues

                repository_db.save()
                return repository_db

        except Repository.DoesNotExist:
            # If the repository does not exist, create a new one
            logging.info(f"Repository with ID {repository.repo_id} was added in db")

            # Create a new repository
            repo = Repository.objects.create(
                repo_id=repository.repo_id,
                name=repository.name if repository.name else '',
                owner=repository.owner if repository.owner else '',
                has_issues=repository.has_issues if repository.has_issues is not None else False,
                opened_issues=repository.opened_issues if repository.opened_issues else '0',
                language=repository.language if repository.language else 'Unknown',
                git_link=repository.git_link if repository.git_link else '',
                pushed_at=repository.pushed_at,
                created_at=repository.created_at,
            )

            # Save the new repository to set created_at and pushed_at timestamps automatically
            repo.save()
            return repo

    @staticmethod
    def add_or_update_issue(issue_data, repository_id):
        repository = Repository.objects.get(repo_id=repository_id)
        print(f'Repository: {repository_id}')
        try:
            issue_db = Issue.objects.get(issue_id=issue_data.issue_id, repository=repository)
            # Update issue details
            issue_db.description = issue_data.description
            issue_db.issue_number = issue_data.issue_number
            issue_db.comments_count = issue_data.comments_count
            issue_db.state = issue_data.state
            issue_db.milestone = issue_data.milestone
            issue_db.closed_at = issue_data.closed_at
            issue_db.created_by = issue_data.created_by
            issue_db.closed_by = issue_data.closed_by
            issue_db.assigned_to = issue_data.assigned_to
            issue_db.labels = issue_data.labels
            issue_db.created_at = issue_data.created_at
            issue_db.save()
            return issue_db
        except Issue.DoesNotExist:
            logging.info(f"Issue with id '{issue_data.issue_id}' does not exist, creating new.")
            issue_db = Issue.objects.create(
                issue_id=issue_data.issue_id,
                issue_number=issue_data.issue_number,
                repository=repository,
                title=issue_data.title,
                description=issue_data.description,
                comments_count=issue_data.comments_count,
                state=issue_data.state,
                milestone=issue_data.milestone,
                closed_at=issue_data.closed_at,
                created_by=issue_data.created_by,
                closed_by=issue_data.closed_by,
                assigned_to=issue_data.assigned_to,
                labels=issue_data.labels,
                created_at=issue_data.created_at
            )
            issue_db.save()
            return issue_db
        except Exception as e:
            logging.error(f"[add_or_update_issue] An error occurred {e}")
            raise

