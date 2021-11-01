# Generated by Django 3.2.8 on 2021-10-31 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время сообщения')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.article', verbose_name='Статья')),
                ('message_from', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Сообщение от')),
            ],
        ),
    ]
