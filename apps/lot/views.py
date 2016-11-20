# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_detail
from django.views.generic.list_detail import object_list
from apps.auction.models import Auction
from apps.lot.models import Lot

@login_required
def view(request, id):
    return object_detail(request, queryset=Lot.objects.all(), object_id=id, template_name="lot/view.html",
            template_object_name="lot")

@login_required
def list(request, defaulter_id):
    auction_list = Auction.objects.filter(lot=1)
    return object_list(request, queryset=Lot.objects.filter(defaulter=defaulter_id),
                       template_name='lot/list.html', template_object_name="lot",
                       extra_context={'defaulter_id': defaulter_id, 'auction': auction_list})
