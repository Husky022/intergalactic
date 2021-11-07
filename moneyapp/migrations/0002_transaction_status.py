# Generated by Django 3.2.8 on 2021-11-07 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneyapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Создана'), ('DONE', 'Выполнена'), ('CANCELLED', 'Отменена')], default='REG', max_length=9, verbose_name='Статус лайка статьи'),
        ),
    ]