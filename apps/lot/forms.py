# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from apps.lot.models import Lot

class LotForm(ModelForm):
    class Meta:
        model = Lot
        exclude = ('defaulter',)
