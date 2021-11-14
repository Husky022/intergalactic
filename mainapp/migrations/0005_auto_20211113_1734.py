# Generated by Django 3.2.8 on 2021-11-13 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20211113_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendations',
            name='hub',
        ),
        migrations.AlterField(
            model_name='recommendations',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.article', verbose_name='Статья'),
        ),
    ]
