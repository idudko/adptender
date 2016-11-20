# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

MEMBER_TYPE_CHOICES = (
    (1,'Физическое лицо'),
    (2,'Юридическое лицо'),
    (3,'Индивидуальный предприниматель')
)

class ProfileManager(models.Manager):
    def profile_callback(self, user):
        new_profile = Profile.objects.create(user=user,)

class Country(models.Model):
    iso = models.IntegerField(u"Код страны", null= True)
    name =  models.CharField(u'Страна', max_length=255, unique=True, db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = u"страна"
        verbose_name_plural = u"страны"

class Region(models.Model):
    code = models.IntegerField(u"Код региона", null= True)
    name =  models.CharField(u'Регион', max_length=255, unique=True, db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = u"регион"
        verbose_name_plural = u"регионы"

class PopulatedLocalityType(models.Model):
    code = models.IntegerField(u"Код типа населенного пункта", null= True)
    name =  models.CharField(u'Тип населенного пункта', max_length=255, unique=True, db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = u"тип населенного пункта"
        verbose_name_plural = u"типы населенных пунктов"

class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profile')
    member_type = models.IntegerField(u'Тип участника', choices=MEMBER_TYPE_CHOICES, default=1)

    #Название компании
    company_name = models.CharField(u'Наименование компании',max_length=255,blank=True, null=True,help_text=u'Полное наименование компании, с указанием организационно-правовой формы')
    short_company_name = models.CharField(u'Краткое наименование',max_length=255,blank=True, null=True,help_text=u'Краткое наименование компании')

    #ФИО
    last_name = models.CharField(u'Фамилия',max_length=255,blank=True,null=True)
    first_name = models.CharField(u'Имя',max_length=255,blank=True,null=True)
    middle_name = models.CharField(u'Отчество',max_length=255,blank=True,null=True)
    date_of_birth = models.DateField('Дата рождения',blank=True,null=True)

    #Документ, удостоверяющий личность
    document_name = models.CharField(u'Наименование документа',max_length=255,help_text=u'Например, паспорт')
    document_series = models.IntegerField(u'Серия',max_length=50,blank=True,null=True)
    document_number = models.IntegerField(u'Номер',max_length=100,blank=True,null=True)
    document_date_of_issue = models.DateField(u'Дата выдачи',blank=True,null=True)
    document_origin = models.CharField(u'Кем выдан',max_length=255,blank=True,null=True)

    #Реквизиты
    inn = models.CharField(u'ИНН',max_length=255,blank=True,null=True, help_text=u'Идентификационный номер налогоплательщика')
    ogrn = models.CharField(u'ОГРН',max_length=255,blank=True,null=True, help_text=u'Основной государственный регистрационный номер')
    kpp = models.CharField(u'КПП',max_length=255,blank=True,null=True, help_text=u'Код причины постановки на учёт')

    #Адрес
    country = models.ForeignKey(Country, default=171, verbose_name=u'Страна')
    region = models.ForeignKey(Region,verbose_name=u'Регион', blank=True, null=True)
    populated_locality_type = models.ForeignKey(PopulatedLocalityType, verbose_name=u'Тип населенного пункта', blank=True, null=True)
    populated_locality = models.CharField(u'Населенный пункт',max_length=255,blank=True,null=True)
    address = models.TextField(u'Адрес',max_length=255,blank=True,null=True)

    post = models.CharField(u'Должность',max_length=255,blank=True,null=True)
    phone_number = models.CharField(u'Номер телефона',max_length=100,blank=True,null=True)

    objects = ProfileManager()

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)
