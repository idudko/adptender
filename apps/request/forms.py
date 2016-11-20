# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from django.forms.widgets import RadioSelect
from django.shortcuts import redirect
from apps.auction.models import Auction, BuyRequest, SellRequest
from apps.core.forms import UploadLastFormWizard
from apps.defaulter.models import Defaulter
from apps.lot.models import Lot

class BuyRequestLegalForm(ModelForm):
    """
    Форма добавления запроса на участие в торгах, юр. лиц
    """
    class Meta:
        model = BuyRequest
        fields = ('information_by_interest', 'price_offer', 'extract_egrul', 'constituent_document',
                  'leader_permit_document', 'confirm',)

class BuyRequestLegalWOPriceForm(ModelForm):
    """
    Форма добавления запроса на участие в торгах, юр. лиц
    без предложения о цене
    """
    class Meta:
        model = BuyRequest
        fields = ('information_by_interest', 'extract_egrul', 'constituent_document',
                  'leader_permit_document', 'confirm',)


class BuyRequestIndividualEnterpriseForm(ModelForm):
    """
    Форма добавления запроса на участие в торгах, индивидуальных предпринимателей
    """
    class  Meta:
        model = BuyRequest
        fields = ('information_by_interest', 'price_offer', 'extract_egrip', 'confirm',)


class BuyRequestIndividualEnterpriseWOPriceForm(ModelForm):
    """
    Форма добавления запроса на участие в торгах, индивидуальных предпринимателей
    без предложения о цене
    """
    class  Meta:
        model = BuyRequest
        fields = ('information_by_interest', 'extract_egrip', 'confirm',)        

class BuyRequestIndividualForm(ModelForm):
    """
    Форма добавления запроса на участие в торгах, физ. лиц
    """
    class Meta:
        model = BuyRequest
        fields = ('information_by_interest', 'price_offer', 'identity_card','confirm')
        
class BuyRequestIndividualWOPriceForm(ModelForm):
    """
    Форма добавления запроса на участие в торгах, физ. лиц
    без предложения о цене
    """
    class Meta:
        model = BuyRequest
        fields = ('information_by_interest', 'identity_card','confirm')


class BuyRequestReviewForm(ModelForm):
    """
    Форма принятия / отклонения заявки на проведение торгов
    """
    class Meta:
        model = BuyRequest
        fields = ('status','review',)
        widgets = {
            'status': RadioSelect,
        }

class SellRequestAuctionTypeForm(ModelForm):
    
    class Meta:
        model = Auction
        fields = ('type', 'competition_terms','request_accept_start_date','request_accept_end_date',
        'start_price','auction_step','event_start_date','event_end_date','public_offer_interval',
        'public_offer_step','public_offer_stop_price')
        widgets = {
            'type': RadioSelect,
        }

class SellRequestAuctionSecondForm(ModelForm):

    class Meta:
        model = Auction
        fields = ('deposit_amount', 'deposit_payment_date', 'deposit_return_date', 'banking_details',)


class StockRequestDefaulterForm(ModelForm):

    class Meta:
        model = Defaulter
        exclude = ('author',)


class StockRequestLotForm(ModelForm):

    def set_request(self, request):
        self.request = request
        
    class Meta:
        model = Lot
        exclude = ('defaulter',)

        
class SellRequestWizard(UploadLastFormWizard):
    """
    Визард оформления аукциона на основании заявки
    """

    def done(self, request, form_list):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        defaulter = Defaulter.objects.create(author = request.user)
        defaulter.receiver_first_name = data['receiver_first_name']
        defaulter.receiver_middle_name = data['receiver_middle_name']
        defaulter.receiver_last_name = data['receiver_last_name']
        defaulter.receiver_sro = data['receiver_sro']
        defaulter.name = data['name']
        defaulter.inn = data['inn']
        defaulter.publication_date = data['publication_date']
        defaulter.case_number = data['case_number']
        defaulter.court_name = data['court_name']
        defaulter.court_decision = data['court_decision']
        defaulter.save()

        lot = Lot.objects.create(defaulter=defaulter)
        lot.object_name = data['object_name']
        lot.description = data['description']
        lot.file = data['file']
        lot.save()

        auction = Auction.objects.create(lot=lot, event_start_date = data['event_start_date'],
            event_end_date = data['event_end_date'], request_accept_start_date = data['request_accept_start_date'],
            request_accept_end_date = data['request_accept_end_date'],sell_request_id = self.extra_context.get('req_id'),)
        auction.type = data['type']
        auction.competition_terms = data['competition_terms']
        auction.start_price = data['start_price']
        auction.result_price = data['start_price']
        auction.auction_step = data['auction_step']
        auction.deposit_amount = data['deposit_amount']
        auction.deposit_payment_date = data['deposit_payment_date']
        auction.deposit_return_date = data['deposit_return_date']
        auction.banking_details = data['banking_details']
        auction.public_offer_interval = data['public_offer_interval']
        auction.public_offer_step = data['public_offer_step']
        auction.public_offer_stop_price = data['public_offer_stop_price']
        auction.save()

        return redirect('apps.profile.views.sell_auction_list', mode='announced')

    def get_template(self, step):
        return "request/sell_wizard_%s.html" % step

class SellRequestReviewForm(ModelForm):
    """
    Форма принятия / отклонения заявки на проведение торгов
    """
    class Meta:
        model = SellRequest
        fields = ('status','review',)
        widgets = {
            'status': RadioSelect,
        }

class SellRequestUserForm(ModelForm):
    """
    Форма подачи заявки на проведение торгов
    """
    class Meta:
        model = SellRequest
        fields = ('request_document', 'deposit_agreement_project', 'sale_agreement_project')
