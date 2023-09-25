from wagtail import hooks
from django.urls import path
from django.urls import reverse
from wagtail.admin.menu import MenuItem
from wagtail.permission_policies.pages import PagePermissionPolicy
from .views import ScheduledPagesPanel
from django.utils.translation import gettext_lazy as _
from .urls import urlpatterns


@hooks.register('construct_homepage_panels')
def register_scheduled_pages_panel(request, panels):
    panels.append(ScheduledPagesPanel())
    

class ScheduledPagesMenuItem(MenuItem):
    def is_shown(self, request):
        return PagePermissionPolicy.user_has_permission(request.user, "publish")

@hooks.register("register_reports_menu_item")
def register_scheduled_pages_menu_item():
    return ScheduledPagesMenuItem(
        _("Scheduled pages"),
        reverse("wagtailschedules:scheduled_pages"),
        icon_name="time",
        order=700,
    )

@hooks.register('register_admin_urls')
def register_admin_urls():
    return urlpatterns