# Generated by Django 3.2.8 on 2021-11-09 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sorting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sorting_type', models.CharField(choices=[('NEWEST', 'По дате сначала новые'), ('ELDEST', 'По дате сначала старые'), ('LK_MORE', 'По лайкам сначала больше'), ('LK_LESS', 'По лайкам сначала меньше'), ('COM_MORE', 'По комментариям сначала больше'), ('COM_LESS', 'По комментариям сначала меньше')], default='NEWEST', max_length=8, verbose_name='Тип сортировки статей')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
