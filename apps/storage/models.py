# -*- coding: utf-8 -*-
from django.contrib.sessions.backends.db import SessionStore
from django.core.files.uploadhandler import FileUploadHandler
from django.db import models
from django.contrib.auth.models import User
from apps.storage.extra import ContentTypeRestrictedFileField

TYPE_CHOICES = (
    (1, u'Копия документов, удостоверяющих личность'),
    (2, u'Копия выписки из ЕГРИП '),
    (3, u'Копия выписки из ЕГРЮЛ'),
    (4, u'Копия документов, подтверждающих полномочия руководителя'),
    (5, u'Копия учредительных документов'),
    (6, u'Другие документы')
)

class FileStorage(models.Model):
    user = models.ForeignKey(User)
    type = models.IntegerField(u'Тип документа', choices=TYPE_CHOICES, default=1)
    create_date = models.DateTimeField(u'Дата загрузки файла', auto_now_add=True)
    modify_date = models.DateTimeField(u'Дата изменения файла', auto_now=True)
    name = models.CharField(u'Название', max_length=255,
                            help_text='Название документа, требуемого для предоставления, в соответствии с текущим регламентом ЭТП.')
    file = ContentTypeRestrictedFileField(u'Файл', upload_to='documents',
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880,
            help_text='Документ, требуемый для предоставления, в соответствии с текущим регламентом ЭТП. Поддерживаемые форматы: PDF, GIF, JPEG, PNG, TIFF.')
    hash = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s" % self.name

