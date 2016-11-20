from django.db.models import signals
from django.utils.translation import ugettext_noop as _
import settings


if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("operator_notice", _("Operator notice"), _("message from system operator"))

    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"