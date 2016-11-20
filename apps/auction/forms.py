# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from apps.auction.models import Auction

class BuyRequestsReview(ModelForm):
    class Meta:
        model = Auction
        fields = ('buy_request_review',)

class AuctionReviewForm(ModelForm):
    class Meta:
        model = Auction
        fields = ('status','review','winner')