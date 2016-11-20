from django.db.models import signals
from django.utils.translation import ugettext_noop as _
import settings


if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("sell_request_accept", _("Acceptance Received"), _("sell request you sent has been accepted"))
        notification.create_notice_type("sell_request_reject", _("Rejection Received"), _("sell request you sent has been rejected"))
        notification.create_notice_type("buy_request_accept", _("Acceptance Received"), _("buy request you sent has been accepted"))
        notification.create_notice_type("buy_request_reject", _("Rejection Received"), _("buy request you sent has been rejected"))

    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"