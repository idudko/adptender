# -*- coding: utf-8 -*-
from datetime import datetime
from django.forms.models import ModelForm
from django.forms.widgets import RadioSelect
from django.shortcuts import get_object_or_404
from apps.accreditation.models import Accreditation
from apps.core.forms import UploadLastFormWizard
from apps.profile.forms import IndividualForm, LegalForm
from django import forms
from django.shortcuts import redirect
from apps.profile.models import Profileф

class AccreditationReviewForm(ModelForm):
    """
    Форма принятия / отклонения заявки на аккредитацию
    """
    class Meta:
        model = Accreditation
        fields = ('status','review',)
        widgets = {
            'status': RadioSelect,
        }

class AccreditationTypeForm(ModelForm):
    """
    Форма выбора типа аккредитации
    """
    class Meta:
        model = Accreditation
        fields = ('type',)
        widgets = {
            'type':RadioSelect
        }

class AccreditationIndividualForm(IndividualForm):
    """
    Форма подачи заявления на аккредитацию физическим лицом
    """
    start_date = forms.DateField(label=u'Начало действия',initial=datetime.today)
    end_date = forms.DateField(label=u'Окончание срока действия',initial=datetime.today().replace(year=datetime.today().year+1))
    identity_card = forms.FileField(label=u'Документ, удостоверяющий личность')


class AccreditationIndividualEnterpriseForm(IndividualForm):
    """
    Форма подачи заявления на аккредитацию индивидуальным предпринимателем
    """
    start_date = forms.DateField(label=u'Начало действия',initial=datetime.today)
    end_date = forms.DateField(label=u'Окончание срока действия',initial=datetime.today().replace(year=datetime.today().year+1))
    extract_egrip = forms.FileField(label=u'Выписка из ЕГРИП')

class AccreditationLegalForm(LegalForm):
    """
    Форма подачи заявления на аккредитацию юридическим лицом
    """
    start_date = forms.DateField(label=u'Начало действия',initial=datetime.today)
    end_date = forms.DateField(label=u'Окончание срока действия',initial=datetime.today().replace(year=datetime.today().year+1))
    extract_egrul = forms.FileField(label=u'Выписка из ЕГРЮЛ')
    constituent_document = forms.FileField(label=u'Копии учредительных документов')
    leader_permit_document = forms.FileField(label=u'Документы, подтверждающие полномочия руководителя')

class AccreditationWizard(UploadLastFormWizard):

    def done(self, request, form_list):

        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        profile = get_object_or_404(Profile, user=request.user)
        profile.last_name = data['last_name']
        profile.first_name = data['first_name']
        profile.middle_name = data['middle_name']
        profile.date_of_birth = data['date_of_birth']
        profile.inn = data['inn']
        profile.country = data['country']
        profile.region = data['region']
        profile.populated_locality_type = data['populated_locality_type']
        profile.populated_locality = data['populated_locality']
        profile.address = data['address']
        profile.phone_number = data['phone_number']
        profile.document_name = data['document_name']
        profile.document_series = data['document_series']
        profile.document_number = data['document_number']
        profile.document_date_of_issue = data['document_date_of_issue']
        profile.document_origin = data['document_origin']
        profile.save()

        accreditation = Accreditation.objects.create(user = request.user)
        accreditation.type = data['type']
        accreditation.start_date = data['start_date']
        accreditation.end_date = data['end_date']
        if profile.member_type==1:
            accreditation.identity_card = data['identity_card']
        if profile.member_type==3:
            accreditation.extract_egrip = data['extract_egrip']
        if profile.member_type==2:
            accreditation.extract_egrul = data['extract_egrul']
            accreditation.constituent_document = data['constituent_document']
            accreditation.leader_permit_document = data['leader_permit_document']
        accreditation.save();

        return redirect('apps.accreditation.views.list')

    def get_form(self, step, data=None, files=None):
        return self.form_list[step](data, files, prefix=self.prefix_for_step(step), initial=self.initial.get(step, None),instance=self.instance)

    def get_template(self, step):
        return 'accreditation/wizard_%s.html' % step