# -*- coding: utf-8 -*-
import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db import models

__all__ = (
    'PhoneField', 'InnField', 'KppField', 'OgrnField',
)

clean_reg = re.compile('[^\d\+]*')


class OgrnField(forms.RegexField):
    """
    Поле формы для ввода КПП
    """
    regex = re.compile('^[0-9]{13}$')

    default_error_messages = {
        'required': _(u'This field is required.'),
        'invalid': _(u'Неправильный формат ОГРН, убедитесь, что это значение содержит 13 цифр '),
    }

    def __init__(self, *args, **kwargs):
        self.error_messages = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            self.error_messages.update(kwargs['error_messages'])
        super(OgrnField, self).__init__(self.regex, *args, **kwargs)

    def clean(self, ogrn):
        super(OgrnField, self).clean(ogrn)
        return clean_reg.subn('', ogrn)[0]
    

class KppField(forms.RegexField):
    """
    Поле формы для ввода КПП
    """
    regex = re.compile('^[0-9]{9}$')

    default_error_messages = {
        'required': _(u'This field is required.'),
        'invalid': _(u'Неправильный формат КПП, убедитесь, что это значение содержит 9 цифр '),
    }

    def __init__(self, *args, **kwargs):
        self.error_messages = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            self.error_messages.update(kwargs['error_messages'])
        super(KppField, self).__init__(self.regex, *args, **kwargs)

    def clean(self, kpp):
        super(KppField, self).clean(kpp)
        return clean_reg.subn('', kpp)[0]


class InnField(forms.RegexField):
    """
    Поле формы для ввода ИНН
    """
    regex = re.compile('^[0-9]{10}$')

    default_error_messages = {
        'required': _(u'This field is required.'),
        'invalid': _(u'Неправильный формат ИНН, убедитесь, что это значение содержит 10 цифр '),
    }

    def __init__(self, *args, **kwargs):
        self.error_messages = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            self.error_messages.update(kwargs['error_messages'])
        super(InnField, self).__init__(self.regex, *args, **kwargs)

    def clean(self, inn):
        super(InnField, self).clean(inn)
        return clean_reg.subn('', inn)[0]


class PhoneField(forms.RegexField):
    """
    Form field checking that phone is full (starts with "+") and normalizes
    it to only plus symbol and digits
    """
    regex = re.compile('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')

    default_error_messages = {
        'required': _(u'This field is required.'),
        'invalid': _(u'Введите телефон с кодом страны и города (или мобильного '
                    u'оператора) в формате +7 (846) ххх-хх-хх или +7846ххххххх'),
    }

    def __init__(self, *args, **kwargs):
        self.error_messages = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            self.error_messages.update(kwargs['error_messages'])
        super(PhoneField, self).__init__(self.regex, *args, **kwargs)

    def clean(self, phone):
        super(PhoneField, self).clean(phone)
        return clean_reg.subn('', phone)[0]

class DBPhoneField(models.CharField):
    """
    Form field using PhoneField as formfield and normalizing phone value
    in the same way
    """

    description = _("String (up to %(max_length)s)")

    def __init__(self, *args, **kwargs):
        defaults = {'max_length': 20}
        defaults.update(kwargs)
        super(DBPhoneField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        value = self.to_python(value)
        if value:
            value = clean_reg.subn('', value)[0]
        return value

    def formfield(self, **kwargs):
        return super(DBPhoneField, self).formfield(form_class=PhoneField)