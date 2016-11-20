# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from apps.lot.models import Lot
from apps.storage.extra import ContentTypeRestrictedFileField


AUCTION_STATUS_CHOICES = (
    10, 'Торги по лоту не состоялись',
    20, 'Торги по лоту проведены',
    30, 'Идет прием заявок',
    40, 'Торги окончены',
    50, 'Назначены повторные торги',
    60, 'Идут торги',
    70, 'Ожидание даты начала приема заявок',
    80, 'Подготовка к торгам',
)

AUCTION_TYPE_CHOICES = (
    10, 'Аукцион с открытой формой подачи предложений',
    20, 'Аукцион с закрытой формой подачи предложений',
    30, 'Конкурс с открытой формой подачи предложений',
    40, 'Конкурс с закрытой формой подачи предложений',
    50, 'Продажа посредством публичного предложения',
)

REQUEST_STATUS_SENT = 10
REQUEST_STATUS_ACCEPTED = 20
REQUEST_STATUS_REJECTED = 30

REQUEST_STATUS_CHOICES = (
    REQUEST_STATUS_SENT, 'Отправлено',
    REQUEST_STATUS_ACCEPTED, 'Заявка принята',
    REQUEST_STATUS_REJECTED, 'Отказано'
)

class SellRequest(models.Model):
    """
    Модель запроса на организацию торгов
    """
    status = models.IntegerField(u'Состояние', choices=REQUEST_STATUS_CHOICES, default=1)
    create_date = models.DateTimeField(u'Дата подачи заявки', auto_now_add=True,null=True, blank=True)
    author = models.ForeignKey(User, verbose_name='Автор')
    review_date = models.DateTimeField(u'Рассмотрено',default=None,null=True,blank=True)
    review = models.TextField(u'Результат рассмотрения заявки',null=True, blank=True,)
    request_document = ContentTypeRestrictedFileField(u'Заявка на проведение торгов', upload_to='documents',
           content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
           max_upload_size=5242880,
           help_text=u'Заявка на проведение торгов. Поддерживаемые форматы: PDF, GIF, JPEG, PNG, TIFF.')
    deposit_agreement_project = ContentTypeRestrictedFileField(u'Проект договора о задатке', upload_to='documents',
           content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
           max_upload_size=5242880,
           help_text=u'Проект договора о задатке. Поддерживаемые форматы: PDF, GIF, JPEG, PNG, TIFF.')
    sale_agreement_project = ContentTypeRestrictedFileField(u'Проект договора купли-продажи', upload_to='documents',
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880,
            help_text=u'Проект договора купли-продажи имущества (предприятия) должника. Поддерживаемые форматы: \
            PDF, GIF, JPEG, PNG, TIFF.')

    class Meta():
        db_table = 'request_sell'
        verbose_name = u'заявка'
        verbose_name_plural = u'заявки'
        permissions = (
            ("review", "Рассмотрение заявки на продажу"),
        )

    def __unicode__(self):
        return self.id

    
class Auction(models.Model):
    """
    Аукционы
    """
    sell_request = models.ForeignKey(SellRequest, verbose_name=u'Запрос')
    lot = models.ForeignKey(Lot, blank=True, null=True, verbose_name=u'Лот')
    type = models.IntegerField(u'Тип аукциона', choices=AUCTION_TYPE_CHOICES, default=1)
    review = models.TextField(u'Результат проведения торгов',null=True, blank=True,)
    review_date = models.DateTimeField(u'Рассмотрено',default=None,null=True,blank=True)

    #Рассмотрение заявок организатором торгов
    buy_request_review = ContentTypeRestrictedFileField(u'Протокол об определении участников торгов',
            upload_to='documents', null=True, blank=True,
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880, help_text='Протокол об определении участников торгов.')
    buy_request_review_date = models.DateTimeField(u'Дата отправки протокола',default=None,null=True,blank=True)

    #При проведении конкурса
    competition_terms = models.TextField(u'Условия конкурса', blank=True, null=True,
            help_text=u'Условия конкурса в случае проведения открытых торгов в форме конкурса')
    competition_review = models.TextField(u'Обоснование',
            blank=True, null=True, help_text=u'Обоснование решения о признании участника победителем')


    request_accept_start_date = models.DateTimeField(u'Дата и время начала подачи заявок',
            help_text=u'Дата и время начала представления заявок на участие в открытых торгах \
            и предложений о цене имущества (предприятия) должника')
    request_accept_end_date = models.DateTimeField(u'Дата и время окончания подачи заявок',
            help_text=u'Дата и время окончания представления заявок на участие в открытых торгах \
            и предложений о цене имущества (предприятия) должника')

    deposit_amount = models.DecimalField(u'Размер задатка', decimal_places=2, max_digits=65,
            blank=True, null=True, help_text=u'Размер задатка для участия в торгах')
    deposit_payment_date = models.DateTimeField(u'Окончание приёма задатка',blank=True, null=True,
            help_text=u'Дата и время окончания приема задатка')
    deposit_return_date = models.DateTimeField(u'Срок возврата задатка', help_text=u'Дата и время возврата задатка',
            blank=True, null=True,)
    banking_details = models.TextField(u'Банковские реквизиты', help_text=u'Реквизиты счетов, на которые вносится задаток',
            blank=True, null=True,)

    start_price = models.DecimalField(u'Начальная цена', decimal_places=2, max_digits=15,blank=True, null=True,
            help_text=u'Начальная цена продажи имущества (предприятия) должника')
    auction_step = models.DecimalField(u'Шаг торгов аукциона', blank=True, null=True, decimal_places=2, max_digits=15,
            help_text='Величина повышения начальной цены продажи имущества (предприятия) должника ("шаг аукциона")\
             в случае использования открытой формы подачи предложений о цене имущества (предприятия) должника')

    event_start_date = models.DateTimeField(u'Дата и время проведения', help_text=u'Дата и время начала торгов',)
    event_end_date = models.DateTimeField(u'Дата и время подведения итогов', help_text=u'Дата и время подведения итогов торгов',)

    status = models.IntegerField(u'Статус аукциона', choices=AUCTION_STATUS_CHOICES, default=7)

    result_price=models.DecimalField(u'Текущая цена', decimal_places=2, max_digits=15,
            help_text=u'Текущая цена продажи имущества (предприятия) должника',blank=True, null=True,)

    #При продаже посредством публичного предложения
    public_offer_interval = models.TimeField(u'Интервал снижения цены', blank=True, null=True,
            help_text=u'Срок, по истечении которого последовательно снижается указанная начальная цена')

    public_offer_step = models.DecimalField(u'Шаг снижения цены', blank=True, null=True, decimal_places=2, max_digits=15,
            help_text='Величина снижения начальной цены продажи имущества (предприятия) должника')

    public_offer_stop_price = models.DecimalField(u'Минимальная установленная цена', decimal_places=2, max_digits=15,blank=True, null=True,
            help_text=u'Минимальная установленная цена продажи имущества (предприятия) должника, при достижении которой торги останавливаются')


    winner = models.ForeignKey(User, blank=True, null=True, verbose_name='Победитель')


    class Meta():
        db_table = 'auction'
        verbose_name = u'аукцион'
        verbose_name_plural = u'аукционы'

    def __unicode__(self):
        return u"%s" % self.event_start_date

    def get_absolute_url(self):
        return reverse('apps.auction.views.view',args=[self.id])

class BuyRequest(models.Model):
    """
    Модель запроса на участие в торгах
    """
    auction = models.ForeignKey(Auction, related_name='tender', verbose_name='Аукцион')
    status = models.IntegerField(u'Состояние', choices=REQUEST_STATUS_CHOICES, default=1)
    create_date = models.DateTimeField(u'Дата подачи заявки', auto_now_add=True,null=True, blank=True)
    author = models.ForeignKey(User, verbose_name='Автор')
    review_date = models.DateTimeField(u'Рассмотрено',default=None,null=True,blank=True)
    review = models.TextField(u'Результат рассмотрения заявки',null=True, blank=True,)

    confirm = models.BooleanField(u'Подтверждение обязательств',
            help_text="Обязательство участника открытых торгов соблюдать требования, указанные в сообщении \
            о проведении открытых торгов.",)

    information_by_interest = models.TextField(u'Сведения о наличии или об отсутствии заинтересованности заявителя',
            help_text="Сведения о наличии или об отсутствии заинтересованности заявителя по отношению к должнику, \
            кредиторам, арбитражному управляющему и о характере этой заинтересованности, сведения об участии \
            в капитале заявителя арбитражного управляющего, а также сведения о заявителе, \
            саморегулируемой организации арбитражных управляющих, членом или руководителем которой \
            является арбитражный управляющий.")

    #Если торги в форме конкурса
    price_offer = models.DecimalField(u'Предложение о цене имущества', decimal_places=2, max_digits=15,
            null=True, blank=True)

    #Физическое лицо
    identity_card = ContentTypeRestrictedFileField(u'Документ, удостоверяющий личность', upload_to='documents',
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880, help_text='Копия документа, удостоверяющего личность.')

    #Индивидуальный предприниматель
    extract_egrip = ContentTypeRestrictedFileField(u'Выписка из ЕГРИП', upload_to='documents',
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880, help_text='Действительная на день представления заявления на аккредитацию выписка \
            из Единого государственного реестра индивидуальных предпринимателей или засвидетельствованная в нотариальном \
            порядке копия такой выписки.')

    #Юридическое лицо
    extract_egrul = ContentTypeRestrictedFileField(u'Выписка из ЕГРЮЛ', upload_to='documents',
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880, help_text='Действительная на день представления заявления на аккредитацию выписка \
            из Единого государственного реестра юридических лиц или засвидетельствованная в нотариальном порядке копия \
            такой выписки.')
    constituent_document = ContentTypeRestrictedFileField(u'Учредительные документы', upload_to='documents',
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880, help_text='Копии учредительных документов.')
    leader_permit_document = ContentTypeRestrictedFileField(u'Документы, подтверждающие полномочия руководителя',
            upload_to='documents',
            content_types=['application/pdf', 'application/zip', 'image/gif', 'image/jpeg', 'image/png', 'image/tiff'],
            max_upload_size=5242880,
            help_text='Копия документов, подтверждающих полномочия руководителя.')

    class Meta:
        db_table = 'request_buy'
        permissions = (
            ("view_all_buy_requests", "Просмотр всех заявок"),
        )

    def __unicode__(self):
        return self.id



class Bet(models.Model):
    """ Ставки """
    auction = models.ForeignKey(Auction, verbose_name='Аукцион')
    date = models.DateTimeField('Дата', auto_now_add=True)
    owner = models.ForeignKey(User, verbose_name='Автор')
    value = models.DecimalField(u'Ставка', decimal_places=2, max_digits=20)
    result_price = models.DecimalField(u'Предложение', decimal_places=2, max_digits=20)

    def __unicode__(self):
        return "%s" % self.date


