# Generated by Django 3.2.8 on 2021-11-17 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_recommendations'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='count_dislike',
            field=models.IntegerField(default=0, verbose_name='количество дизлайков'),
        ),
        migrations.AddField(
            model_name='comment',
            name='count_like',
            field=models.IntegerField(default=0, verbose_name='количество лайков'),
        ),
        migrations.AddField(
            model_name='comment',
            name='status_like_dislike',
            field=models.CharField(default='UND', max_length=8, verbose_name='статус лайка'),
        ),
        migrations.AddField(
            model_name='likes',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.comment'),
        ),
    ]
