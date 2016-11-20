# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import RadioSelect
from apps.core.customfields import OgrnField, InnField, KppField, PhoneField
from apps.profile.models import Profile,MEMBER_TYPE_CHOICES
from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile
from django.forms.models import ModelForm


class CustomRegistrationFormUniqueEmail(RegistrationFormUniqueEmail):

    type = forms.ChoiceField(choices=MEMBER_TYPE_CHOICES,label=u'Тип участника',required=True,widget=RadioSelect)
    last_name = forms.CharField(label=u'Фамилия',required=True)
    first_name = forms.CharField(label=u'Имя',required=True)
    middle_name = forms.CharField(label=u'Отчество',required=True)
    phone_number = PhoneField(label=u'Номер телефона',max_length=100,required=True,)


    """
    Дополнительные поля для индивидуального предпринимателя
    """
    inn = InnField(label=u'ИНН',required=False,help_text=u'Идентификационный номер налогоплательщика')
    ogrn = OgrnField(label=u'ОГРН',required=False,help_text=u'Основной государственный регистрационный номер')

    """
    Дополнительные поля для юридического лица
    """
    company_name = forms.CharField(label=u'Наименование компании',help_text=u'Полное наименование компании, с указанием организационно-правовой формы',required=False)
    short_company_name = forms.CharField(label=u'Краткое наименование',help_text=u'Краткое наименование компании',required=False)
    kpp = KppField(label=u'КПП',required=False,help_text=u'Код причины постановки на учёт')

    def save(self,profile_callback=None):
        new_user = RegistrationProfile.objects.create_inactive_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password1'],
                email=self.cleaned_data['email'],
        )

        profile = Profile.objects.create(user=new_user)
        profile.member_type = self.cleaned_data['type']
        profile.last_name = self.cleaned_data['last_name']
        profile.first_name = self.cleaned_data['first_name']
        profile.middle_name = self.cleaned_data['middle_name']
        profile.company_name = self.cleaned_data['company_name']
        profile.short_company_name = self.cleaned_data['short_company_name']
        profile.inn = self.cleaned_data['inn']
        profile.kpp = self.cleaned_data['kpp']
        profile.ogrn = self.cleaned_data['ogrn']
        profile.phone_number = self.cleaned_data['phone_number']
        profile.save()

        return new_user

    def __init__(self, *args, **kw):
        super(RegistrationFormUniqueEmail, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'type',
            'last_name',
            'first_name',
            'middle_name',
            'company_name',
            'short_company_name',
            'inn',
            'kpp',
            'ogrn',
            'email',
            'phone_number',
            'username',
            'password1',
            'password2']


class LegalForm(ModelForm):
    """
    Форма редактирования профиля, юридического лица
    """
    company_name = forms.CharField(required=True,label='Компания')
    phone_number = PhoneField(label=u'Номер телефона',max_length=100,required=True,)

    class Meta:
        model = Profile
        fields = ('company_name','country','region', 'populated_locality_type','populated_locality',
                  'address','last_name','first_name','middle_name','post','phone_number')


class IndividualForm(ModelForm):
    """
    Форма редактирования профиля, физического лица
    """
    phone_number = PhoneField(label=u'Номер телефона',max_length=100,required=True,)
    inn = InnField(label=u'ИНН',required=False,help_text=u'Идентификационный номер налогоплательщика')
    document_series = forms.IntegerField(label=u'Серия',required=True,)
    document_number = forms.IntegerField(label=u'Номер',required=True,)
    document_date_of_issue = forms.DateField(label=u'Дата выдачи',required=True,)
    document_origin = forms.CharField(label=u'Кем выдан',min_length=2,required=True,)


    class Meta:
        model = Profile
        fields = ('country','region', 'populated_locality_type','populated_locality',
                  'address','last_name','first_name','middle_name','date_of_birth','inn','phone_number',
                  'document_name', 'document_series', 'document_number', 'document_date_of_issue', 'document_origin')

