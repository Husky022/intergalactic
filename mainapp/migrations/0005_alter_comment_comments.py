# Generated by Django 3.2.8 on 2021-11-09 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20211109_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='_mainapp_comment_comments_+', to='mainapp.Comment'),
        ),
    ]
