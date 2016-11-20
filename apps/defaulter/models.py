# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

class Defaulter(models.Model):
    #Арбитражный управляющий
    author = models.ForeignKey(User, verbose_name='Автор')
    receiver_last_name = models.CharField(u'Фамилия',max_length=255,blank=True,null=True,
            help_text=u'Фамилия арбитражного управляющего')
    receiver_first_name = models.CharField(u'Имя',max_length=255,blank=True,null=True,
            help_text=u'Имя арбитражного управляющего')
    receiver_middle_name = models.CharField(u'Отчество',max_length=255,blank=True,null=True,
            help_text=u'Отчество арбитражного управляющего')
    receiver_sro = models.CharField(u'СРО',max_length=255,blank=True,null=True,
            help_text=u'Наименование саморегулируемой организации, членом которой \
            является арбитражный управляющий')
    
    #Должник
    name = models.CharField(u'Наименование должника', max_length=255,
            help_text=u'Наименование (фамилия, имя, отчество - для физического лица) должника, имущество (предприятие) \
            которого выставляется на открытые торги')
    inn = models.CharField(u'ИНН', max_length=255, blank=True, null=True,
            help_text=u'Индивидуальный номер налогоплательщика должника')
    court_name = models.CharField(u'Название суда', max_length=255, blank=True, null=True,
            help_text=u'Наименование арбитражного суда, рассматривающего дело о банкротстве')
    case_number = models.CharField(u'Номер дела', max_length=255, blank=True, null=True,
            help_text=u'Номер дела о банкротстве')
    court_decision = models.TextField(u'Основание для проведения открытых торгов', blank=True, null=True,
            help_text=u'Реквизиты судебного акта арбитражного суда')

    publication_date = models.DateField(u'Дата публикации о проведении торгов в прессе',
            help_text=u'Дата публикации сообщения о проведении открытых торгов в официальном издании, \
            осуществляющем опубликование сведений, предусмотренных Федеральным законом от 26 октября 2002 г. \
            N 127-ФЗ "О несостоятельности (банкротстве)"',null=True, blank=True)
    
    class Meta():
        db_table = 'defaulter'
        verbose_name = u'банкрот'
        verbose_name_plural = u'банкроты'

    def __unicode__(self):
        return u"%s" % (self.name)

    def get_absolute_url(self):
        return reverse('apps.defaulter.views.view',args=[self.id])
