# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from apps.storage.extra import ContentTypeRestrictedFileField

ACCREDITATION_TYPE_CHOICES = (
    (1, 'Покупка'),
    (2, 'Продажа')
)

ACCREDITATION_STATUS_CHOICES = (
    (1, 'Заявление отправлено'),
    (2, 'Аккредитация подтверждена'),
    (3, 'В аккредитации отказано')
)

class Accreditation(models.Model):
    type = models.IntegerField(u'Вид аккредитации', choices=ACCREDITATION_TYPE_CHOICES, default=1)
    create_date = models.DateTimeField(u'Дата и время заявления', auto_now_add=True,null=True, blank=True)
    start_date = models.DateField(u'Начало действия', auto_now_add=True,null=True, blank=True)
    end_date = models.DateField(u'Окончание срока действия', auto_now_add=True,null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Заявитель')
    status = models.IntegerField(u'Статус', choices=ACCREDITATION_STATUS_CHOICES, default=1)
    review_date = models.DateTimeField(u'Рассмотрено',default=None,null=True,blank=True)
    review = models.TextField(u'Причина отказа в аккредитации',null=True, blank=True,)

    #Физическое лицо
    identity_card = ContentTypeRestrictedFileField(u'Документ, удостоверяющий личность', upload_to='documents',
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880, help_text='Копия документа, удостоверяющего личность.')

    #Индивидуальный предприниматель
    extract_egrip = ContentTypeRestrictedFileField(u'Выписка из ЕГРИП', upload_to='documents',
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880, help_text='Действительная на день представления заявления на аккредитацию выписка \
            из Единого государственного реестра индивидуальных предпринимателей или засвидетельствованная в нотариальном \
            порядке копия такой выписки.')

    #Юридическое лицо
    extract_egrul = ContentTypeRestrictedFileField(u'Выписка из ЕГРЮЛ', upload_to='documents',
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880, help_text='Действительная на день представления заявления на аккредитацию выписка \
            из Единого государственного реестра юридических лиц или засвидетельствованная в нотариальном порядке копия \
            такой выписки.')
    constituent_document = ContentTypeRestrictedFileField(u'Учредительные документы', upload_to='documents',
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880, help_text='Копии учредительных документов.')
    leader_permit_document = ContentTypeRestrictedFileField(u'Документы, подтверждающие полномочия руководителя',
            upload_to='documents',
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880,
            help_text='Копия документов, подтверждающих полномочия руководителя.')

    class Meta():
        db_table = 'accreditation'
        verbose_name = u'аккредитация'
        verbose_name_plural = u'аккредитации'
