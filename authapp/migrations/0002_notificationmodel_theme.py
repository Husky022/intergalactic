# Generated by Django 3.2.8 on 2021-11-24 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationmodel',
            name='theme',
            field=models.TextField(blank=True, null=True, verbose_name='Тема'),
        ),
    ]
