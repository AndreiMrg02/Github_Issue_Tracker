# Generated by Django 5.1.2 on 2024-10-20 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('githubissues', '0006_issue_issue_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='task_id',
            new_name='issue_id',
        ),
    ]
