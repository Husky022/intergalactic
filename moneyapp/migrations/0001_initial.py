# Generated by Django 3.2.8 on 2021-11-16 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name='Баланс')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='Время обновления баланса')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Пользователь', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('CREATED', 'Создана'), ('DONE', 'Выполнена'), ('CANCELLED', 'Отменена')], default='CREATED', max_length=9, verbose_name='Статус лайка статьи')),
                ('sender', models.TextField(verbose_name='Отправитель')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Сопроводительное сообщение')),
                ('coins', models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name='Монеты')),
                ('is_read', models.BooleanField(db_index=True, default=False, verbose_name='Статус прочтения')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время транзакции')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Получатель', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
