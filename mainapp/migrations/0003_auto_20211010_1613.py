# Generated by Django 3.2.8 on 2021-10-10 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_article_hab'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hab',
            options={'verbose_name': 'хаб', 'verbose_name_plural': 'хабы'},
        ),
        migrations.DeleteModel(
            name='AdvUser',
        ),
    ]
