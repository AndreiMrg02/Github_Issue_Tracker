# Generated by Django 5.1.2 on 2024-10-20 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('githubissues', '0004_issue_closed_by_issue_comments_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='state',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.DeleteModel(
            name='State',
        ),
    ]
