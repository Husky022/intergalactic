# Generated by Django 3.2.8 on 2021-10-10 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_article_add_datatime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='add_datatime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время добавления'),
        ),
    ]
