# -*- coding:utf-8 -*-
import cStringIO as StringIO
from datetime import datetime
from operator import __eq__, __ne__
import cgi
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.mail.message import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.context import Context
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from django.views.generic.simple import direct_to_template
import simplejson
from sx.pisa3.pisa_document import pisaDocument
from apps.accreditation.models import Accreditation
from apps.auction.forms import BuyRequestsReview
from apps.auction.models import Auction, BuyRequest, SellRequest
from apps.defaulter.models import Defaulter
from apps.lot.models import Lot
from apps.profile.models import Profile
from apps.request.forms import SellRequestAuctionTypeForm, SellRequestWizard, StockRequestLotForm, StockRequestDefaulterForm, SellRequestAuctionSecondForm, SellRequestReviewForm, BuyRequestIndividualEnterpriseForm, BuyRequestLegalForm, BuyRequestIndividualForm, BuyRequestReviewForm, SellRequestUserForm, BuyRequestIndividualWOPriceForm, BuyRequestLegalWOPriceForm, BuyRequestIndividualEnterpriseWOPriceForm


@login_required
def sell_list(request):
    """
    Список заявок на проведение торгов
    """
    request.breadcrumbs(u'Список заявок на проведение торгов',request.path)

    prof=None
    if request.user.has_perm("request.view_all"):
        request_list = SellRequest.objects.all()
    else:
        prof = get_object_or_404(Profile, user=request.user)
        request_list = SellRequest.objects.filter(author=request.user)
    return direct_to_template(request, 'request/sell_list.html', {'request_list': request_list, 'profile': prof})


@login_required
#request.review
def sell_review(request, id):
    """
    Рассмотрение заявки на проведение тотргов
    и отправка уведомление о результатах на email
    """

    request.breadcrumbs(((u'Список заявок на проведение торгов',reverse('apps.request.views.sell_list')),(u"Заявление на проведение торгов №"+ id.__str__() ,request.path)))

    if "notification" in settings.INSTALLED_APPS:
        from notification import models as notification
    else:
        notification = None

    req = get_object_or_404(SellRequest,pk=id)
    profile = get_object_or_404(Profile,user=req.author)

    if request.method == "POST":
        form = SellRequestReviewForm(request.POST,instance=req)
        if form.is_valid():
            if not req.review_date:
                obj = form.save(commit=False)
                obj.review_date = datetime.now()
                obj.save()

                if notification:
                    if obj.status == 2:
                        notification.send([profile.user], "sell_request_accept",{'site':Site.objects.get_current()})

                    if obj.status == 3:
                        notification.send([profile.user], "sell_request_reject",{'site':Site.objects.get_current()})

            return redirect('apps.request.views.sell_list')
    else:
        form = SellRequestReviewForm(instance=req)
    return direct_to_template(request, 'request/sell_review.html',{'form':form,'profile': profile, 'req':req})

"""
@login_required
def sell_view(request, id):
    #Просмотр заявки на проведение торгов

    
    profile, defaulter, lot, auction = None
    req = get_object_or_404(SellRequest,pk=id)
    if request.user.has_perm("request.view_all"):
        profile = get_object_or_404(Profile,user=req.author)
        defaulter = get_object_or_404(Defaulter,author=req.author)
        lot = get_object_or_404(Lot,defaulter=defaulter)
        auction = get_object_or_404(Auction,lot=lot)
    else:
        if req.author == request.user:
            profile = get_object_or_404(Profile,user=request.user)
            defaulter = get_object_or_404(Defaulter,author=request.user)
            lot = get_object_or_404(Lot,defaulter=defaulter)
            auction = get_object_or_404(Auction,lot=lot)
        else:
            redirect('apps.request.views.sell_list')
    return direct_to_template(request,'request/view_sell_request.html',{'profile': profile, 'defaulter': defaulter,
        'lot':lot, 'auction':auction, 'req':req})
"""
    
@login_required
def sell_request_process(request, req_id):

    data = {'req_id':req_id,}
    #data['req_id'] = req_id
    return SellRequestWizard([StockRequestDefaulterForm,SellRequestAuctionTypeForm,SellRequestAuctionSecondForm,StockRequestLotForm])(request, extra_context=data)

@login_required
def sell_request_send(request):
    """
    Добавляем заявку на проведение тотргов
    """
    if request.method == 'POST':
        form = SellRequestUserForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author_id = request.user.id
            obj.save()
        return redirect('apps.request.views.sell_list')
    else:
        form = SellRequestUserForm()

    return direct_to_template(request,'request/sell_add.html',{'form':form})


@login_required
def sell_request_view(request, id):
    """
    Просмотр заявки на проведение торгов
    """
    request.breadcrumbs(((u'Список заявок на проведение торгов',reverse('apps.request.views.sell_list')),(u'Заявление на проведение торгов №'+ id.__str__() ,request.path)))
    
    profile = None
    req = get_object_or_404(SellRequest,pk=id)

    auct = Auction.objects.filter(sell_request=req)
    if auct.__len__() > 0:
        state = {'auct_exist':True,}
    else:
        state = {'auct_exist':False,}

    if request.user.has_perm("request.view_all"):
        profile = get_object_or_404(Profile,user=req.author)
    else:
        if req.author == request.user:
            profile = get_object_or_404(Profile,user=request.user)
        else:
            redirect('apps.request.views.sell_list')
    return direct_to_template(request,'request/sell_request_view.html',{'profile': profile,'req':req, 'state':state,})

@login_required
def is_request_add_permitted(request,type):
    """
    Проверяем, есть ли у пользователя аккредитация, которая:
     - рассмотрена;
     - не просрочена;
     - имеет нужный тип;
     - рассмотрена с положительным результатом;
    """
    if request.is_ajax():
        json = {}
        accreditation = Accreditation.objects.filter(user=request.user).filter(start_date__lte=datetime.now, end_date__gte=datetime.now)
        accreditation = accreditation.filter(type=type).filter(review_date__isnull=False).filter(status=2)
        if accreditation.exists():
            json['permitted'] = True
        else:
            json['permitted'] = False
        json = simplejson.dumps(json)
        return HttpResponse(json,mimetype='application/json')
    else:
        raise Http404

@login_required
def buy_request_add(request, id):
    """
    Добавление заявки на участие в аукционе
    """
    auction = get_object_or_404(Auction,pk=id)
    form = None
    profile = get_object_or_404(Profile, user=request.user)
    if profile.member_type == 1:
        # Физическое лицо
        if auction.type in [1,5]:
            form = BuyRequestIndividualWOPriceForm(request.POST, request.FILES)
        elif auction.type in [2,3,4]:
            form = BuyRequestIndividualForm(request.POST, request.FILES)
    elif profile.member_type == 2:
        # Юридическое лицо
        if auction.type in [1,5]:
            form = BuyRequestLegalWOPriceForm(request.POST, request.FILES)
        elif auction.type in [2,3,4]:
            form = BuyRequestLegalForm(request.POST, request.FILES)
    elif profile.member_type == 3:
        # Индивидуальный предприниматель
        if auction.type in [1,5]:
            form = BuyRequestIndividualEnterpriseWOPriceForm(request.POST, request.FILES)
        elif auction.type in [2,3,4]:
            form = BuyRequestIndividualEnterpriseForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.auction_id = id
            obj.save()
            return redirect('apps.profile.views.buy_list', mode='active')
    return direct_to_template(request, 'request/buy_add.html', {'form': form})

@login_required
def buy_view(request, id):
    """
    Просмотр заявки на участие в аукционе
    """
    req = get_object_or_404(BuyRequest,pk=id)
    request.breadcrumbs(((u'Список торгов',reverse('apps.request.views.buy_auction_list')),
                        (u"Список заявок на участие в торгах АДП-"+ req.auction.id.__str__() ,reverse('apps.request.views.buy_request_list',args=[req.auction.id])),
                        (u"Заявка на участие №"+ id.__str__() ,request.path))
                        )
    profile = None

    if request.user.has_perm("auction.view_all_buy_requests"):
        profile = get_object_or_404(Profile,user=req.author)
    else:
        if req.author == request.user:
            profile = get_object_or_404(Profile,user=request.user)
        else:
            return redirect('apps.request.views.buy_request_list',id=req.auction)

    return direct_to_template(request,'request/view_buy_request.html',{'profile': profile, 'req':req})


@login_required
def buy_auction_list(request):
    """
    Список аукционов для личного кабинета
    """
    #request.breadcrumbs(((u"Аукцион",reverse('apps.accreditation.views.list')),(u"Заявки",reverse('apps.request.views.sell_request_view',args=[1])),(u'Тест',request.path)))
    request.breadcrumbs(u'Список торгов',request.path)
    auction_list = Auction.objects.filter(sell_request__status=2).select_related(depth=2)
    return direct_to_template(request, 'request/auction_list.html', {'auctions': auction_list})

@login_required
def buy_request_list(request, id):
    """
    Список заявок на проведение торгов
    """

    auct = get_object_or_404(Auction,id=id)
    request_list = BuyRequest.objects.filter(auction=auct)
    prof = get_object_or_404(Profile, user=auct.sell_request.author)

    request.breadcrumbs(((u'Список торгов',reverse('apps.request.views.buy_auction_list')),(u"Список заявок на участие в торгах АДП-"+ auct.id.__str__() ,request.path)))

    #Если заявки просматривает создатель (по умолчанию)
    template = 'request/buy_list.html'
    data = {'request_list': request_list.filter(author=request.user), 'profile': prof, 'auction':auct}

    #Если заявки рассматривает организатор торгов
    if auct.sell_request.author == request.user:
        #Если заявка еще не рассмотрена
        if auct.buy_request_review_date is None and datetime.now() > auct.request_accept_end_date and auct.status == 8:
            form = BuyRequestsReview(instance=auct)
            data = {'request_list': request_list, 'profile': prof, 'form':form,'auction':auct}
            template = 'request/buy_list_review.html'
            if request.method == 'POST':
                form = BuyRequestsReview(request.POST,request.FILES,instance=auct)
                if form.is_valid():
                    obj = form.save()
                    obj.buy_request_review_date = datetime.now()
                    obj.save()
        #Если заявка уже рассмотрена
        elif __ne__(auct.buy_request_review_date,None) and datetime.now() > auct.request_accept_end_date and auct.status == 8:
            data = {'request_list': request_list, 'profile': prof,'auction':auct}
            print auct.id
            template = 'request/buy_list_reviewed.html'

    #Если заявки рассматривает оператор площадки
    if request.user.has_perm("auction.view_all_buy_requests"):
        template = 'request/buy_list.html'
        if __ne__(auct.buy_request_review_date,None) and datetime.now() > auct.buy_request_review_date and auct.status == 8:
            data = {'request_list': request_list, 'profile': prof,'auction':auct}


    return direct_to_template(request, template, data)

@login_required
#"request.change_status"
def buy_review(request, id):
    """
    Рассмотрение заявки на проведение тотргов
    и отправка уведомление о результатах на email
    """

    if "notification" in settings.INSTALLED_APPS:
        from notification import models as notification
    else:
        notification = None

    req = get_object_or_404(BuyRequest,pk=id)
    profile = get_object_or_404(Profile,user=req.author)
    auction = get_object_or_404(Auction,id=req.auction.id)
    lot = get_object_or_404(Lot,id=auction.lot.id)
    defaulter = get_object_or_404(Defaulter,id=lot.defaulter.id)

    if request.method == "POST":
        form = SellRequestReviewForm(request.POST,instance=req)
        if form.is_valid():
            if not req.review_date:
                obj = form.save(commit=False)
                obj.review_date = datetime.now()
                obj.save()

                if notification:
                    if obj.status == 2:
                        notification.send([profile.user], "buy_request_accept",{'site':Site.objects.get_current()})
                    if obj.status == 3:
                        notification.send([profile.user], "buy_request_reject",{'site':Site.objects.get_current()})

            return redirect('apps.request.views.buy_request_list', id = auction.id)
    else:
        form = BuyRequestReviewForm(instance=req)
    return direct_to_template(request, 'request/buy_review.html',{'form':form,'profile': profile, 'defaulter': defaulter, 'lot':lot, 'auction':auction, 'req':req})

@login_required
def get_request_notification(request, req_id):
    """
    Генерируем PDF из HTML шаблона
    Уведомлеие о признании участником торгов или об отказе
    """
    req = get_object_or_404(BuyRequest,pk=req_id)

    info = {'tender_type':req.auction.get_type_display(),
            'lot':req.auction.lot.object_name,
            'site': Site.objects.get_current(),}

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=adptender_notification.pdf'

    template = ''
    if req.status == 2:
        template = 'auction/request_accept_notification.html'
    elif req.status == 3:
        template =  'auction/request_decline_notification.html'
    template = get_template(template)


    context = Context({ 'info':info})
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response.write(result.getvalue())
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))
