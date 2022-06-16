from wagtail.core import hooks
from django.urls import path
from django.urls import reverse
from wagtail.admin.menu import MenuItem
from wagtail.core.models import UserPagePermissionsProxy
from .views import ScheduledPagesPanel
from django.utils.translation import gettext_lazy as _


@hooks.register('construct_homepage_panels')
def register_scheduled_pages_panel(request, panels):
    panels.append(ScheduledPagesPanel())
    

class ScheduledPagesMenuItem(MenuItem):
    def is_shown(self, request):
        return UserPagePermissionsProxy(request.user).can_publish_pages()

@hooks.register("register_reports_menu_item")
def register_scheduled_pages_menu_item():
    return ScheduledPagesMenuItem(
        _("Scheduled pages"),
        reverse("wagtailschedules:scheduled_pages"),
        icon_name="time",
        order=700,
    )