# Generated by Django 5.1.2 on 2024-10-20 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('githubissues', '0005_alter_issue_state_delete_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='task_id',
            field=models.CharField(default='', max_length=255),
        ),
    ]
