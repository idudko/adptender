# -*- coding:utf-8 -*-
import cStringIO as StringIO
from datetime import datetime
from operator import __add__
import cgi
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.context import Context
from django.template.loader import get_template
from django.views.generic.list_detail import object_detail
from django.views.generic.simple import direct_to_template
import simplejson
from sx.pisa3 import pisaDocument
from apps.auction.forms import AuctionReviewForm
from apps.auction.models import Auction, Bet, SellRequest, BuyRequest
from apps.profile.models import Profile


def auction_review(request, id):
    """
    Подведение результатов проведения торгов
    и отправка уведомление о результатах на email
    """
#    profile = get_object_or_404(Profile,user=request.user)
    auction = get_object_or_404(Auction,pk=id)
    if request.method == "POST":
        form = AuctionReviewForm(request.POST,instance=auction)
        if form.is_valid():
            if not auction.review_date:
                obj = form.save(commit=False)
                obj.review_date = datetime.now()
                obj.save()

                """
                sending emails
                
                subject = render_to_string('accreditation/accreditation_email_subject.txt', {'site':Site.objects.get_current()})
                html_content = ''
                if obj.status == 2:
                    html_content = render_to_string('accreditation/accreditation_email_success.html', {'site':Site.objects.get_current()})

                if obj.status == 3:
                    html_content = render_to_string('accreditation/accreditation_email_fail.html', {'site':Site.objects.get_current()})

                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject,text_content,settings.DEFAULT_FROM_EMAIL,[profile.user.email])
                msg.attach_alternative(html_content,"text/html")
                msg.send()
                """

            return redirect('apps.accreditation.views.list')
    else:
        form = AuctionReviewForm(instance=auction)
    return direct_to_template(request, 'accreditation/review.html',{'form':form, 'auction': auction})


def view(request, id):
    """
    Просмотр аукциона
    """
    request_author = SellRequest.objects.filter(auction__id=id).values('author')
    pk = Profile.objects.filter(user=request_author).values("pk")
    organizer = get_object_or_404(Profile, pk = pk)

    req = {}
    if request.user.is_authenticated():
        req = BuyRequest.objects.filter(author=request.user,auction__id=id, status=2)

    org_dict = {}
    if req.__len__() > 0:
        org_dict['bet_approve'] = True
    else:
        org_dict['bet_approve'] = False

    if organizer.member_type==1:
        org_dict['name'] = organizer.last_name + ' ' + organizer.first_name + ' ' + organizer.middle_name
    elif organizer.member_type==2:
        org_dict['name'] = organizer.company_name
    elif organizer.member_type==3:
        org_dict['name'] = 'ИП ' + organizer.last_name + ' ' + organizer.first_name + ' ' + organizer.middle_name
    org_dict['address'] = organizer.country.name + ' ' + organizer.populated_locality +' '+ organizer.address
    org_dict['email'] = organizer.user.email
    org_dict['phone'] = organizer.phone_number

    return object_detail(request, queryset=Auction.objects.select_related(depth=2), object_id=id,
                         template_name="auction/view.html", template_object_name="auction",
                         extra_context={'organizer': org_dict})

def list(request):
    """
    Получаем список аукционов
    """
    auction_list = Auction.objects.filter(sell_request__status=2).select_related(depth=2)
    paginator = Paginator(auction_list, 25)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        auctions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        auctions = paginator.page(paginator.num_pages)

    return direct_to_template(request, 'auction/list.html', {'auctions': auctions})


@login_required
def bet_list(request):
    """
    Получаем список ставок для аукциона
    """
    if request.is_ajax():
        bets_list = []
        auction = Auction.objects.get(pk=request.GET.get('auction', ''))
        bets = Bet.objects.filter(auction=auction).order_by('-date')
        for bet in bets:
            bet_dict = {}
            profile = get_object_or_404(Profile, user=bet.owner)
            if profile.member_type==1:
                bet_dict['owner'] = profile.last_name + ' ' + profile.first_name + ' ' + profile.middle_name
            elif profile.member_type==2:
                bet_dict['owner'] = profile.company_name
            elif profile.member_type==3:
                bet_dict['owner'] = 'ИП ' + profile.last_name + ' ' + profile.first_name + ' ' + profile.middle_name
            bet_dict['date'] = bet.date.strftime('%d.%m.%Y %H:%M:%S')
            bet_dict['value'] = bet.value.__str__()
            bet_dict['result_price'] = bet.result_price.__str__()
            bet_dict['result'] = auction.result_price.__str__()
            bets_list.append(bet_dict)

        json = simplejson.dumps(bets_list)
        return HttpResponse(json, mimetype='application/json')

@login_required
def do_bet(request,tender):
    """
    Делаем ставку в аукционе с открытой формой подачи предложений
    """
    if request.is_ajax():
        auction = get_object_or_404(Auction,pk=tender)
        req = BuyRequest.objects.filter(author=request.user,auction=auction, status=2)
        if req.__len__() > 0:
            if auction.status == 6:
                amount = request.POST.get('amount',auction.auction_step)

                bet = Bet.objects.create(auction=auction,owner=request.user,value=amount,result_price=__add__(auction.result_price,Decimal(amount)))
                bet.date = datetime.now()

                if auction.result_price is None:
                    auction.result_price = auction.start_price + amount
                else:
                    auction.result_price = auction.result_price + Decimal(amount)
                bet.save()
                auction.save()


                json = {}
                return HttpResponse(json, mimetype='application/json')


def get_auction_report(request, tender):
    """
    Генерируем PDF из HTML шаблона
    Протокол о результатах проведения торгов
    """
    auct = get_object_or_404(Auction,pk=tender)
    buy_reqs = BuyRequest.objects.filter(~Q(status=1),auction=auct,)
    ctx = []
    for req in buy_reqs:
        data = {}
        profile = get_object_or_404(Profile, user=req.author)
        if profile.member_type == 1:
            data['name'] = profile.last_name + ' ' + profile.first_name + ' ' + profile.middle_name
        if profile.member_type == 2:
            data['name'] = profile.company_name
        data['address'] = profile.country.name + ', '+ profile.region.name + ', ' \
            + profile.populated_locality_type.name + ' '+ profile.populated_locality + ', ' + profile.address
        ctx.append(data)

    winner = {'tender_type': auct.get_type_display(),
              'lot': auct.lot.object_name,
              'site': Site.objects.get_current(),}
    
    win_reqs = buy_reqs.filter(~Q(auction__winner=None))
    for win_req in win_reqs:
        profile = get_object_or_404(Profile, user=win_req.author)
        if profile.member_type == 1:
            winner['name'] = profile.last_name + ' ' + profile.first_name + ' ' + profile.middle_name
        if profile.member_type == 2:
            winner['name'] = profile.company_name
        winner['address'] = profile.country.name + ', '+ profile.region.name + ', ' \
            + profile.populated_locality_type.name + ' '+ profile.populated_locality + ', ' + profile.address

    #Обоснование выбора победителя для конкурса
    if auct.type == 3 or auct.type == 4:
        winner['competition_review'] = auct.review


    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=adptender_protocol.pdf'
    template = get_template('auction/protocol.html')

    context = Context({'ctx':ctx, 'winner':winner})
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response.write(result.getvalue())
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))

