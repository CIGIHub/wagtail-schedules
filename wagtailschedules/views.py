from datetime import datetime, timedelta

import django_filters
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _
from wagtail.admin import messages
from wagtail.admin.filters import DateRangePickerWidget, WagtailFilterSet
from wagtail.admin.views.reports.base import PageReportView
from wagtail.models import Page, UserPagePermissionsProxy, Revision
from wagtail.permission_policies.pages import PagePermissionPolicy

try:
    from wagtail.models import PageRevision
except ImportError:
    from wagtail.models import Revision as PageRevision

# Possible Homepagepanel
from wagtail.admin.ui.components import Component


def get_pages_for_user(request):
    permission_policy = PagePermissionPolicy()
    revisions = Revision.objects.filter(
        approved_go_live_at__gt=timezone.now()
    )
    object_ids = revisions.values_list('object_id', flat=True)
    id_integers = [int(object_id) for object_id in object_ids]
    pages = (Page.objects.filter(id__in=id_integers) & permission_policy.instances_user_has_permission_for(request.user, "publish"))

    if getattr(settings, "WAGTAIL_I18N_ENABLED", False):
        pages = pages.select_related("locale")
    return pages


class ScheduledPagesPanel(Component):
    name = "scheduled_pages"
    template_name = "wagtailschedules/scheduled_pages.html"
    order = 200

    def get_context_data(self, parent_context):
        request = parent_context["request"]
        context = super().get_context_data(parent_context)
        context["pages_to_be_scheduled"] = get_pages_for_user(request)
        context["request"] = request
        context["csrf_token"] = parent_context["csrf_token"]
        return context


class ScheduledPagesReportFilterSet(WagtailFilterSet):
    go_live_at = django_filters.DateFromToRangeFilter(
        widget=DateRangePickerWidget)

    class Meta:
        model = Page
        fields = ["go_live_at"]


class ScheduledPagesView(PageReportView):
    template_name = "wagtailadmin/reports/scheduled_pages.html"
    title = _("Pages scheduled for publishing")
    header_icon = "time"
    list_export = PageReportView.list_export
    filterset_class = ScheduledPagesReportFilterSet

    def get_filename(self):
        return "scheduled-pages-report-{}".format(
            datetime.today().strftime("%Y-%m-%d")
        )

    def get_queryset(self):
        self.queryset = get_pages_for_user(self.request)
        return super().get_queryset()

    def dispatch(self, request, *args, **kwargs):
        permission_policy = PagePermissionPolicy()
        if not permission_policy.instances_user_has_permission_for(request.user, "publish"):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def publish(request, page_id):
    page = get_object_or_404(Page, id=page_id).specific
    if not page.permissions_for_user(request.user).can_publish():
        raise PermissionDenied

    new_go_live_timestamp = timezone.now() - timedelta(seconds=1)
    page.go_live_at = new_go_live_timestamp
    page.save()
    # Save revision
    revision = page.save_revision(
        user=request.user,
        log_action=True)
    revision.publish()

    messages.success(request, _("Page '{0}' has been published.").format(
        page.get_admin_display_title()), extra_tags='time')

    # Redirect
    redirect_to = request.POST.get('next', None)
    if redirect_to and url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts={request.get_host()}):
        return redirect(redirect_to)
    else:
        return redirect('wagtailadmin_explore', page.get_parent().id)


def publish_all_scheduled_confirm(request):

    revisions_to_publish = get_pages_for_user(request)

    return TemplateResponse(
        request,
        "wagtailschedules/publish_all_confirm.html",
        {
            "revisions_to_publish": revisions_to_publish,
        }
    )


def publish_all_scheduled(request):
    if request.method == "POST":
        new_go_live_timestamp = timezone.now() - timedelta(seconds=1)
        revisions_to_publish = get_pages_for_user(request)
        for page in revisions_to_publish:
            page.go_live_at = new_go_live_timestamp
            page.save()
            revision = page.specific.save_revision(
                user=request.user,
                log_action=True)
            revision.publish()

        messages.success(request, _("{0} pages have been published.").format(
            len(revisions_to_publish)), extra_tags='time')

        # Redirect
        redirect_to = request.POST.get('next', None)
        if redirect_to and url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts={request.get_host()}):
            return redirect(redirect_to)
        else:
            return redirect('wagtailschedules:scheduled_pages')
