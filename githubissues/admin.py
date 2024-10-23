from django.contrib import admin
from githubissues.models import User, Issue, Repository, Reaction


class UserAdmin(admin.ModelAdmin):
    list_display = ('github_username', 'email', 'last_connection')
    search_fields = ('github_username', 'email')


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name', 'owner')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'repository', 'state', 'created_at', 'assigned_to')
    list_filter = ('state', 'repository')
    search_fields = ('title', 'repository__name')


class ReactionAdmin(admin.ModelAdmin):
    list_display = ('issue', 'content', 'count')
    search_fields = ('issue__title', 'content')

admin.site.register(User, UserAdmin)
admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Reaction, ReactionAdmin)
