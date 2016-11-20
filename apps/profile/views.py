# -*- coding:utf-8 -*-
from datetime import datetime
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.auction.models import SellRequest, Auction, BuyRequest
from apps.profile.models import Profile
from apps.profile.forms import LegalForm,IndividualForm
from django.views.generic.simple import direct_to_template

@login_required
def edit(request):
    form = None
    profile = get_object_or_404(Profile,user=request.user)
    #form = None
    if request.method == 'POST':
        if profile.member_type==1:
            # Физическое лицо
            form = IndividualForm(request.POST,instance=profile)
        elif profile.member_type==2:
            # Юридическое лицо
            form = LegalForm(request.POST,instance=profile)

        if form.is_valid():
            form.save()
            return redirect('apps.profile.views.view')
    else:
        if profile.member_type==1:
            # Физическое лицо
            form = IndividualForm(instance=profile)
        elif profile.member_type==2:
            # Юридическое лицо
            form = LegalForm(instance=profile)

    return direct_to_template(request,'accounts/edit_profile.html',{'form':form})


@login_required
def view(request):
    template=''
    profile = get_object_or_404(Profile, user=request.user)
    if profile.member_type == 1:
        template = 'accounts/view_individual_profile.html'
    elif profile.member_type == 2:
        template = 'accounts/view_legal_profile.html'
    return direct_to_template(request,template,{'profile': profile})


@login_required
def buy_list(request,mode=None):
    list ={}
    if mode == u"active":
        list = BuyRequest.objects.filter(author=request.user, auction__event_start_date__lte=datetime.now(),auction__review__isnull=True).select_related()
    elif mode == u"winner":
        list = BuyRequest.objects.filter(author=request.user, auction__winner= request.user).select_related()
    elif mode == u"history":
        list = BuyRequest.objects.filter(author=request.user, auction__review_date__lte=datetime.now(),auction__review__isnull=False).select_related()
    return direct_to_template(request, 'accounts/buy_list.html', {'list': list})

@login_required
def sell_auction_list(request,mode=None):
    list ={}
    if mode == u"announced":
        list = Auction.objects.select_related().filter(~Q(status__in=[1,2,4]), sell_request__author=request.user,)
    elif mode == u"completed":
        list = Auction.objects.select_related().filter(sell_request__author=request.user,status__in=[1,2,4])
    return direct_to_template(request, 'accounts/sell_auction_list.html', {'auction_list': list})

@login_required
def sell_stock_list(request,mode=None):
    list ={}
    if mode == u"announced":
        list = SellRequest.objects.select_related().filter(author=request.user)
    elif mode == u"completed":
        list = SellRequest.objects.select_related().filter(author=request.user)

    return direct_to_template(request, 'accounts/sell_stock_list.html', {'list': list})