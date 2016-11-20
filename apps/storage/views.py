
import cStringIO as StringIO
import cgi
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.context import Context
from django.template.loader import get_template
from django.views.generic.simple import direct_to_template
from sx.pisa3.pisa_document import pisaDocument
from apps.auction.models import BuyRequest
from apps.storage.forms import FileStorageForm
from django.forms.formsets import formset_factory


@login_required
def upload_documents(request):

    FileStorageFormSet = formset_factory(FileStorageForm)
    if request.method == 'POST':
        formset = FileStorageFormSet(request.POST, request.FILES, prefix='mypost')
        if formset.is_valid():
            for form in formset.forms:
                new_obj = form.save(commit= False )
                new_obj.user = request.user
                new_obj.save()
            return redirect('/about/contact/')
    else:
        formset = FileStorageFormSet(prefix='mypost')
    return direct_to_template(request,'storage/file_storage.html',{'formset':formset})

"""
def my_view(request):


    req = get_object_or_404(BuyRequest,pk=1)

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
    
    #result = StringIO.StringIO()
    result = open(file, 'wb')

    pisaDocument().
    pdf = pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)

    #if not pdf.err:
    #    response.write(result.getvalue())
    #    return response
    result.close()

    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))
"""

def my_view(request):

    req = get_object_or_404(BuyRequest,pk=1)

    info = {'tender_type':req.auction.get_type_display(),
            'lot':req.auction.lot.object_name,
            'site': Site.objects.get_current(),}

    pdf = render_to_pdf('auction/request_accept_notification.html', { 'info': info, 'MEDIA_ROOT': settings.MEDIA_ROOT,})

    if pdf:
        pdf_file = open("%s/%s.pdf" % (settings.MEDIA_ROOT,'my_test'+req.id.__str__()), 'w').write(pdf)
    return HttpResponse()


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisaDocument(StringIO.StringIO(html.encode('utf-8')), result, show_error_as_pdf=True, encoding='UTF-8')
    if not pdf.err:
        return result.getvalue()
    return False