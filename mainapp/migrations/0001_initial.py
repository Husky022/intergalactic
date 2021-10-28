# Generated by Django 3.2.8 on 2021-10-28 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mainapp.utilities


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=168, verbose_name='Название статьи')),
                ('image', models.ImageField(blank=True, upload_to=mainapp.utilities.get_timestamp_path, verbose_name='Изображение для статьи')),
                ('preview', models.TextField(max_length=250, verbose_name='Предпросмотр')),
                ('text', models.TextField(verbose_name='Текст статьи')),
                ('tag', models.CharField(blank=True, max_length=64, verbose_name='Тэг статьи')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Актуальность статьи')),
                ('add_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('article_status', models.CharField(choices=[('DR', 'Черновик'), ('MD', 'На модерации'), ('RC', 'Требует исправления'), ('PB', 'Опубликована'), ('AR', 'В архиве')], default='DR', max_length=2, verbose_name='Статус публикации')),
                ('views', models.IntegerField(default=0, verbose_name='просмотры')),
                ('rating', models.IntegerField(default=0, verbose_name='рейтинг')),
            ],
            options={
                'verbose_name': 'статья',
                'verbose_name_plural': 'статьи',
                'ordering': ['-add_datetime'],
            },
        ),
        migrations.CreateModel(
            name='ButtonsInProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='название кнопки')),
                ('include_html_file_name', models.CharField(max_length=100, verbose_name='html файл')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('image', models.ImageField(blank=True, upload_to=mainapp.utilities.get_timestamp_path)),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Активация комментария')),
                ('add_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления комментария')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mainapp.article', verbose_name='Статья')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'комментарии',
            },
        ),
        migrations.CreateModel(
            name='Hosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=22, verbose_name='АйПи посетителя')),
            ],
        ),
        migrations.CreateModel(
            name='Hub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='Название хаба')),
                ('order', models.SmallIntegerField(db_index=True, default=0, verbose_name='Порядок вывода')),
                ('is_active', models.BooleanField(default=True, verbose_name='активность')),
            ],
            options={
                'verbose_name': 'хаб',
                'verbose_name_plural': 'хабы',
            },
        ),
        migrations.CreateModel(
            name='SubComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст подкомментария')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Активация комментария')),
                ('add_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления ответа')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mainapp.article', verbose_name='Статья')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор подкомментария')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.comment', verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Подкомментарий',
                'verbose_name_plural': 'Подкомментарии',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('DZ', 'Дизлайк'), ('UND', 'Не установлено'), ('LK', 'Лайк')], default='UND', max_length=3, verbose_name='Статус лайка статьи')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'лайк',
                'verbose_name_plural': 'лайки',
            },
        ),
        migrations.CreateModel(
            name='ArticleStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=2, verbose_name='Краткое название')),
                ('name', models.CharField(max_length=50, verbose_name='Название статуса')),
                ('name_plural', models.CharField(max_length=50, verbose_name='Название раздела в ЛК (мн.число)')),
                ('buttons', models.ManyToManyField(to='mainapp.ButtonsInProfile', verbose_name='Кнопки для этого статуса в ЛК')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='article_status_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.articlestatus', verbose_name='Статус публикации (новый)'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор статьи'),
        ),
        migrations.AddField(
            model_name='article',
            name='hub',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='mainapp.hub', verbose_name='Хаб'),
        ),
        migrations.CreateModel(
            name='Art_Visits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.article', verbose_name='Статья')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.hosts', verbose_name='адрес посетителя')),
            ],
        ),
    ]