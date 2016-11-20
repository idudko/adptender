# -*- coding: utf-8 -*-
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from apps.accreditation.forms import AccreditationWizard, AccreditationTypeForm, AccreditationIndividualForm, AccreditationReviewForm, AccreditationLegalForm, AccreditationIndividualEnterpriseForm
from apps.accreditation.models import Accreditation
from apps.profile.models import Profile

@login_required
def add(request):
    """
    Добавление заявки на аккредитацию, в зависимости от типа участника
    """
    profile = get_object_or_404(Profile, user=request.user)
    form = None
    if profile.member_type == 1:
        form = AccreditationIndividualForm
    elif profile.member_type == 2:
        form = AccreditationLegalForm
    elif profile.member_type == 3:
        form = AccreditationIndividualEnterpriseForm
    return AccreditationWizard([AccreditationTypeForm, form])(request, instance=profile)

@login_required
def review(request, id):
    """
    Рассмотрение заявки и отправка уведомление о результатах на email
    """
    request.breadcrumbs(((u'Список заявок на аккредитацию',reverse('apps.accreditation.views.list')),(u"Заявление на аккредитацию №"+ id.__str__() ,request.path)))

    if "notification" in settings.INSTALLED_APPS:
        from notification import models as notification
    else:
        notification = None

    
    profile = get_object_or_404(Profile,user=request.user)
    accreditation = get_object_or_404(Accreditation,pk=id)
    if request.method == "POST":
        form = AccreditationReviewForm(request.POST,instance=accreditation)
        if form.is_valid():
            if not accreditation.review_date:
                obj = form.save(commit=False)
                obj.review_date = datetime.now()
                obj.save()

                if notification:

                    if obj.status == 2:
                        notification.send([profile.user], "accreditation_accept",{'site':Site.objects.get_current()})

                    if obj.status == 3:
                        notification.send([profile.user], "accreditation_reject",{'site':Site.objects.get_current()})

            return redirect('apps.accreditation.views.list')
    else:
        form = AccreditationReviewForm(instance=accreditation)
    return direct_to_template(request, 'accreditation/review.html',{'form':form,'profile': profile, 'accreditation': accreditation})

@login_required
def list(request):
    """
    Список заявок на аккредитацию
    """
    request.breadcrumbs(u'Список заявок на аккредитацию',request.path)

    accreditation_list = Accreditation.objects.filter(user=request.user)
    return direct_to_template(request, 'accreditation/list.html', {'accreditation_list': accreditation_list})

@login_required
def view(request, id):
    """
    Просмотр заявки на аккредитацию
    """
    request.breadcrumbs(((u'Список заявок на аккредитацию',reverse('apps.accreditation.views.list')),(u"Заявление на аккредитацию №"+ id.__str__() ,request.path)))

    profile = get_object_or_404(Profile,user=request.user)
    accreditation = get_object_or_404(Accreditation,pk=id)
    return direct_to_template(request, 'accreditation/view.html',{'profile': profile, 'accreditation': accreditation})


