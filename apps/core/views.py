# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template
from registration.models import RegistrationProfile
from apps.core.forms import MailMessageForm
import settings

def set_status(list, stat):
    """
    Устанавливаем статусы аукционам по cron'у
    """
    for obj in list:
        obj.status = stat
        obj.save()


def mail_delivery(request):
    """
    Рассылаем пользователям сообщение
    """
    request.breadcrumbs(((u'Список сообщений системы',reverse('notification_notices')),(u"Отправка сообщения" ,request.path)))

    if "notification" in settings.INSTALLED_APPS:
        from notification import models as notification
    else:
        notification = None

    profiles = RegistrationProfile.objects.all()

    if request.method == 'POST':
        form = MailMessageForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            for profile in profiles:
                if notification:
                    print profile.user.email
                    notification.send([profile.user], "operator_notice",{'subject':subject,'body':body,})
            return redirect('notification_notices') # Redirect after POST
    else:
        form = MailMessageForm()

    return direct_to_template(request,'core/mail_message.html', {'form': form,})

