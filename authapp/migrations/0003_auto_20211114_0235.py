# Generated by Django 3.2.8 on 2021-11-13 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_auto_20211114_0235'),
        ('authapp', '0002_auto_20211114_0213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intergalacticuser',
            name='chats',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
    ]
