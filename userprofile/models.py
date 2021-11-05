from django.db import models


class ButtonsInProfile(models.Model):
    name = models.CharField(verbose_name='название кнопки', max_length=20)
    include_html_file_name = models.CharField(verbose_name='html файл', max_length=100)
