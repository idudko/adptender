# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_detail

from apps.defaulter.models import Defaulter

@login_required
def view(request, id):
    return object_detail(request, queryset=Defaulter.objects.all(), object_id=id, template_name="defaulter/view.html",
            template_object_name="defaulter")

@login_required
def list(request):
    defaulter_list = Defaulter.objects.all()
    return direct_to_template(request, 'defaulter/list.html', {'defaulter_list': defaulter_list})