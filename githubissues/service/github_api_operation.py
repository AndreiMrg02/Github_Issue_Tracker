import logging
import os
from datetime import datetime, timezone
import requests

from dotenv import load_dotenv

from githubissues.dboperation.database_utils import DatabaseUtils
from githubissues.github_utils import Constants
from githubissues.models import Repository, Issue

load_dotenv()
GITHUB_TOKEN = os.getenv(Constants.GITHUB_TOKEN)

BASE_URL = 'https://api.github.com'
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}


class GithubApiOperation:

    @staticmethod
    def add_user_or_update(github_username, email):
        url = f"https://api.github.com/users/{github_username}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            github_username = data.get('login')
            user = DatabaseUtils.get_or_create_github_user_db(github_username, email)
            return user
        else:
            logging.error("This user does not exist")
            return None

    @staticmethod
    def add_or_update_repo(user):
        url = f"https://api.github.com/users/{user.github_username}/repos"
        response = requests.get(url, headers=HEADERS)
        repository_list = []

        if response.status_code == 200:
            for repo_response in response.json():
                repository_db = Repository()

                repository_db.repo_id = repo_response['id']
                repository_db.name = repo_response['name']
                repo_response_owner = repo_response['owner']
                repository_db.owner = repo_response_owner['login']
                repository_db.has_issues = repo_response['has_issues']
                repository_db.language = repo_response['language']
                repository_db.created_at = repo_response['created_at']
                repository_db.pushed_at = repo_response['pushed_at']
                repository_db.git_link = repo_response['clone_url']
                repository_db.opened_issues = repo_response['open_issues_count']
                DatabaseUtils.add_or_update_repo(repository_db)
                repository_list.append(repository_db)

            return repository_list

        else:
            logging.error(f"User {user.github_username} does not have any repository")
            return None

    @staticmethod
    def fetch_and_store_issues(github_username, repo_id):
        repository = Repository.objects.get(repo_id=repo_id)
        url = f"https://api.github.com/repos/{github_username}/{repository.name}/issues?state=all"
        response = requests.get(url, headers=HEADERS)
        issue_list = []

        if response.status_code == 200:
            for issue_data in response.json():
                issue_info = Issue()
                issue_info.issue_number = issue_data['number']
                issue_info.issue_id = issue_data['id']
                issue_info.title = issue_data['title']
                issue_info.description = issue_data.get('body')
                issue_info.comments_count = issue_data['comments']
                issue_info.state = issue_data['state']
                if issue_data['milestone']:
                    issue_milestone = issue_data['milestone']
                    issue_info.milestone = issue_milestone['number']
                else:
                    issue_info.milestone = None
                issue_user_created = issue_data['user']
                issue_info.created_by = issue_user_created['login']
                if issue_data.get('closed_by'):
                    issue_closed_by = issue_data['closed_by']
                    issue_info.closed_by = issue_closed_by['login']
                else:
                    issue_info.closed_by = 'Not closed'

                if issue_data.get('assignee'):
                    issue_assignee = issue_data['assignee']
                    issue_info.assigned_to = issue_assignee['login']
                else:
                    issue_info.assigned_to = 'Not assigned'
                if 'labels' in issue_data and issue_data['labels']:
                    issue_info.labels = [label['name'] for label in issue_data['labels']]
                else:
                    issue_info.labels = []

                issue_info.closed_at = issue_data.get('closed_at')
                issue_info.created_at = issue_data['created_at']
                DatabaseUtils.add_or_update_issue(issue_info, repo_id)
                issue_list.append(issue_info)

            logging.info(f"Issues for repository {repository.name} fetched and stored.")
            return issue_list

        else:
            logging.error(f"Repository {repository.name} does not have any issue")
            return None

    @staticmethod
    def get_rate_limit():

        url = f"{BASE_URL}/rate_limit"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            data = response.json().get('rate')
            rate_limit = {
                'limit': data['limit'],
                'remaining': data['remaining'],
                'reset_time': datetime.fromtimestamp(data['reset']).replace(tzinfo=timezone.utc).strftime(
                    '%Y-%m-%d %H:%M:%S')
            }
            return rate_limit
        else:
            logging.error(f"Failed to fetch rate limit. Status code: {response.status_code}")
            return {
                'limit': 0,
                'remaining': 0,
                'reset_time': None
            }

    @staticmethod
    def create_github_issue(github_username, repo_id, title, description, labels=None):

        repository = Repository.objects.get(repo_id=repo_id)
        url = f"{BASE_URL}/repos/{github_username}/{repository.name}/issues"

        payload = {
            "title": title,
            "body": description,
        }

        if labels:
            label_list = [label.strip() for label in labels.split(",")]
            payload["labels"] = label_list

        response = requests.post(url, json=payload, headers=HEADERS)

        if response.status_code == 201:

            issue_data = response.json()
            issue_info = Issue()
            issue_info.issue_number = issue_data["number"]
            issue_info.issue_id = issue_data['id']
            issue_info.title = issue_data['title']
            issue_info.description = issue_data.get('body')
            issue_info.state = issue_data['state']
            issue_info.created_at = issue_data['created_at']
            issue_info.closed_at = issue_data.get('closed_at')
            issue_info.assigned_to = issue_data['assignee']['login'] if issue_data.get('assignee') else 'Not assigned'
            issue_info.created_by = issue_data['user']['login']
            issue_info.labels = [label['name'] for label in issue_data['labels']] if issue_data.get('labels') else []

            DatabaseUtils.add_or_update_issue(issue_info, repo_id)

            return True
        else:

            return False

    @staticmethod
    def get_issue_by_id(github_username, repo_id, issue_id):

        repository = Repository.objects.get(repo_id=repo_id)
        url = f"{BASE_URL}/repos/{github_username}/{repository.name}/issues/{issue_id}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            issue_data = response.json()
            issue_info = Issue()
            issue_info.issue_number = issue_data["number"]
            issue_info.issue_id = issue_data['id']
            issue_info.title = issue_data['title']
            issue_info.description = issue_data.get('body')
            issue_info.state = issue_data['state']
            issue_info.created_at = issue_data['created_at']
            issue_info.closed_at = issue_data.get('closed_at')
            issue_info.assigned_to = issue_data['assignee']['login'] if issue_data.get('assignee') else 'Not assigned'
            issue_info.created_by = issue_data['user']['login']
            issue_info.labels = [label['name'] for label in issue_data['labels']] if issue_data.get('labels') else []

            return issue_info
        else:

            return None

    @staticmethod
    def reopen_github_issue(github_username, repository, issue):

        url = f"{BASE_URL}/repos/{github_username}/{repository.name}/issues/{issue.issue_number}"
        payload = {
            "state": "open"
        }

        response = requests.patch(url, json=payload, headers=HEADERS)

        if response.status_code == 200:
            logging.info(f"Issue #{issue.issue_number} has been reopened on GitHub.")
            return True
        else:
            logging.error(
                f"Failed to reopen issue #{issue.issue_number} on GitHub. Status code: {response.status_code}")
            return False

    @staticmethod
    def close_github_issue(github_username, repository, issue):

        url = f"{BASE_URL}/repos/{github_username}/{repository.name}/issues/{issue.issue_number}"
        payload = {
            "state": "closed"
        }

        response = requests.patch(url, json=payload, headers=HEADERS)

        if response.status_code == 200:
            logging.info(f"Issue #{issue.issue_number} has been reopened on GitHub.")
            return True
        else:
            logging.error(
                f"Failed to reopen issue #{issue.issue_number} on GitHub. Status code: {response.status_code}")
            return False