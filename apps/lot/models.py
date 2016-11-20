# -*- coding: utf-8 -*-
from django.db import models
from apps.defaulter.models import Defaulter
from apps.storage.extra import ContentTypeRestrictedFileField

class Lot(models.Model):
    object_name = models.CharField(u'Наименование объекта', max_length=255)
    description = models.TextField(u'Описание')
    file = ContentTypeRestrictedFileField(u'Файл', upload_to='documents',
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880, help_text='Файл, описывающий данный лот. Поддерживаемые форматы: PDF, GIF, JPEG, \
            PNG, TIFF.')

    defaulter = models.ForeignKey(Defaulter, related_name='defaulter', verbose_name='Банкрот')

    class Meta:
        db_table = 'lots'
        verbose_name = 'лот'
        verbose_name_plural = 'лоты'


    def __unicode__(self):
        return u"%s | %s" % (self.object_name, self.defaulter)
    
    