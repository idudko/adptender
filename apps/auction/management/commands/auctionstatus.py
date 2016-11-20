# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q
from apps.auction.models import Bet, Auction
from apps.core.views import set_status

class Command(BaseCommand):
    """
    Команда, которую используем в crontab'e
    для изменения статусов аукционов
    """
    """
    Статусы:
    1 - Торги по лоту не состоялись
    2 - Торги по лоту проведены
    3 - Идет прием заявок
    4 - Торги окончены
    5 - Назначены повторные торги
    6 - Идут торги
    7 - Ожидание даты начала приема заявок
    8 - Подготовка к торгам

    Типы:
    1 - Аукцион с открытой формой подачи предложений
    2 - Аукцион с закрытой формой подачи предложений
    3 - Конкурс с открытой формой подачи предложений
    4 - Конкурс с закрытой формой подачи предложений
    5 - Продажа посредством публичного предложения
    """


    help = 'Change status of auctions to actual state'

    def handle(self, *args, **options):
        self.stdout.write("Running Django jobs...\n")

        #Неоконченные торги
        auction_list = Auction.objects.filter(~Q(status = 1),~Q(status = 2), ~Q(status = 4))

        #Идет прием заявок
        auctions = auction_list.filter(~Q(status = 3), request_accept_start_date__lte=datetime.now,
            request_accept_end_date__gte=datetime.now)
        set_status(auctions,3)

        #Подготовка к торгам
        auctions = auction_list.filter(~Q(status = 6), request_accept_end_date__lte=datetime.now,
            event_start_date__gte=datetime.now)
        set_status(auctions,8)


        #Идут торги
        auctions = auction_list.filter(~Q(status = 6), event_start_date__lte=datetime.now, type__in=[1,5])
        set_status(auctions,6)


        #Завершаем аукцион с открытой формой подачи предложений
        auctions = auction_list.filter(type=1, event_start_date__lte=datetime.now()-timedelta(hours=1) )
        for auction in auctions:
            try:
                bet = Bet.objects.filter(auction = auction).latest('date')
                if datetime.now()-bet.date >timedelta(minutes=30):
                    auction.status = 4
                    auction.save()
            except Bet.DoesNotExist :
                print "Oops!  That was no Bet for this Auction number.  Try again..."

        #Понижаем ставку в продаже посредством публичного предложения,
        #если цена достигла минимума - закрываем
        auctions = auction_list.filter(type=5, event_start_date__lte=datetime.now())
        for auction in auctions:
            if auction.result_price - auction.public_offer_step > auction.public_offer_stop_price:
                interval = auction.public_offer_interval
                zz = (datetime.now() - auction.event_start_date).total_seconds()
                xx = timedelta(hours=interval.hour,minutes=interval.minute).total_seconds()
                #yy=zz%xx
                self.stdout.write(str(zz)+"Yahoo!\n")
                self.stdout.write(str(xx)+"Yahoo!\n")
                self.stdout.write(str(auction.public_offer_step*(Decimal(zz//xx)))+" Yahoo!\n")
                if (auction.result_price+auction.public_offer_step*Decimal(zz%xx)) < auction.start_price:
                    self.stdout.write("Yahoo!\n")


            else:
                auction.status = 4
                auction.save()
                
        #Завершаем аукцион с закрытой формой подачи предложений
        auctions = Auction.objects.filter(~Q(type = 1), ~Q(type=5), event_start_date__lte=datetime.now)
        set_status(auctions,4)

