from django.db import models


class User(models.Model):
    github_username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    last_connection = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.github_username


class Repository(models.Model):
    repo_id = models.CharField(max_length=255, unique=True, default='')
    name = models.CharField(max_length=255,null='true')
    owner = models.CharField(max_length=255,null='true')
    has_issues = models.BooleanField(default=False,null='true')
    opened_issues = models.CharField(max_length=10, default='0')
    language = models.CharField(max_length=250, default='Unknown', null='true')
    created_at = models.DateTimeField(auto_now_add=True,null='true')
    pushed_at = models.DateTimeField(auto_now_add=True,null='true')
    git_link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.owner}/{self.name}"


class Issue(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='issues')
    issue_id = models.CharField(max_length=255, default='')
    issue_number = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    comments_count = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=255, default="Unknown")
    milestone = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=255, default='Unknown')
    closed_by = models.CharField(max_length=255, default='Unknown')
    assigned_to = models.CharField(max_length=255, null=True, blank=True)
    labels = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=1000, null=True)
    user = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author_association = models.CharField(max_length=50, null=True,
                                          blank=True)


class Reaction(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='reactions')
    content = models.CharField(max_length=50)  # tipul de reacție (thumbs_up, heart, etc.)
    count = models.IntegerField()  # numărul de reacții de acest tip

    def __str__(self):
        return f"{self.content} ({self.count})"
