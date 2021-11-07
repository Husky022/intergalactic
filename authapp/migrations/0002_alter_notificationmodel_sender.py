# Generated by Django 3.2.8 on 2021-11-02 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationmodel',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель'),
        ),
    ]