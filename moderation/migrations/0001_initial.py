# Generated by Django 3.2.8 on 2021-11-09 05:50

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
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст жалобы')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время жалобы')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Актуальность жалобы')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.article', verbose_name='Статья')),
                ('complainant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Жалоба от')),
            ],
            options={
                'verbose_name': 'жалоба',
                'verbose_name_plural': 'жалобы',
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='ComplaintMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время сообщения')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.article', verbose_name='Статья')),
                ('complaint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moderation.complaint', verbose_name='Жалоба')),
                ('message_from', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Сообщение от')),
            ],
        ),
        migrations.CreateModel(
            name='BlockedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, verbose_name='Причина блокировки')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время блокировки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время сообщения')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.article', verbose_name='Статья')),
                ('message_from', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Сообщение от')),
                ('moderator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='moderator', to=settings.AUTH_USER_MODEL, verbose_name='Модератор')),
            ],
        ),
    ]
