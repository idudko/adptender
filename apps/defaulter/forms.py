# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from apps.defaulter.models import Defaulter

class DefaulterForm(ModelForm):
    class Meta:
        model = Defaulter