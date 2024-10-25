# Generated by Django 5.1.2 on 2024-10-20 11:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('githubissues', '0002_repository_repo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='closed_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='repository',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='repository',
            name='git_link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='repository',
            name='has_issues',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='repository',
            name='language',
            field=models.CharField(default='Unknown', max_length=250),
        ),
        migrations.AddField(
            model_name='repository',
            name='opened_issues',
            field=models.CharField(default='0', max_length=10),
        ),
        migrations.AddField(
            model_name='repository',
            name='pushed_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
