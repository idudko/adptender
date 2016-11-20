# -*- coding: utf-8 -*-
from django.contrib.formtools.wizard import FormWizard
from django.http import Http404
from django import forms

class UploadLastFormWizard(FormWizard):

    def get_form(self, step, data=None, files=None):
        return self.form_list[step](data, files, prefix=self.prefix_for_step(step), initial=self.initial.get(step, None))

    def __call__(self, request, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        if 'extra_context' in kwargs:
            self.extra_context.update(kwargs['extra_context'])
        current_step = self.determine_step(request, *args, **kwargs)
        self.parse_params(request, *args, **kwargs)

        # Sanity check.
        if current_step >= self.num_steps():
            raise Http404('Step %s does not exist' % current_step)

        previous_form_list = []
        for i in range(current_step):
            f = self.get_form(i, request.POST, request.FILES)
            if request.POST.get("hash_%d" % i, '') != self.security_hash(request, f):
                return self.render_hash_failure(request, i)

            if not f.is_valid():
                return self.render_revalidation_failure(request, i, f)
            else:
                self.process_step(request, f, i)
                previous_form_list.append(f)

        # Process the current step. If it's valid, go to the next step or call
        # done(), depending on whether any steps remain.
        if request.method == 'POST':
            form = self.get_form(current_step, request.POST, request.FILES)
        else:
            form = self.get_form(current_step)

        if form.is_valid():
            self.process_step(request, form, current_step)
            next_step = current_step + 1


            if next_step == self.num_steps():
                return self.done(request, previous_form_list + [form])
            else:
                form = self.get_form(next_step)
                self.step = current_step = next_step

        return self.render(form, request, current_step)

class MailMessageForm(forms.Form):
    """
    Форма отправки сообщения всем пользователям
    """
    subject = forms.CharField(label=u'Тема', max_length=100,required=True,)
    body = forms.CharField(label=u'Текст сообщения', widget=forms.Textarea,required=True,max_length=255,)
