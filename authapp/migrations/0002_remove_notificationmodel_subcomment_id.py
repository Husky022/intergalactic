# Generated by Django 3.2.8 on 2021-11-09 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationmodel',
            name='subcomment_id',
        ),
    ]
