# Generated by Django 5.1.2 on 2024-10-23 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('githubissues', '0008_alter_repository_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='issue_number',
            field=models.CharField(default='', max_length=255),
        ),
    ]
