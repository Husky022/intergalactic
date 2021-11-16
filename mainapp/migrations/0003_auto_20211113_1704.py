# Generated by Django 3.2.8 on 2021-11-13 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0002_recommendations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendations',
            name='article',
        ),
        migrations.RemoveField(
            model_name='recommendations',
            name='hub',
        ),
        migrations.AddField(
            model_name='recommendations',
            name='article_author_view_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество просмотров авторов'),
        ),
        migrations.AddField(
            model_name='recommendations',
            name='article_view_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество просмотров статей'),
        ),
        migrations.AddField(
            model_name='recommendations',
            name='hub_view_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество просмотров хабов'),
        ),
        migrations.AlterField(
            model_name='recommendations',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
