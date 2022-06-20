from django.urls import path, include

from .views import ScheduledPagesView, publish_all_scheduled, publish_all_scheduled_confirm, publish

app_name = 'wagtailschedules'

scheduled_patterns = ([
    path("", ScheduledPagesView.as_view(), name="scheduled_pages"),
    path("<int:page_id>/publish/", publish, name='publish'),
    path("publish_all/", publish_all_scheduled, name='publish_all'),
    path("publish_all/confirm/", publish_all_scheduled_confirm, name='publish_all_confirm'),
], app_name)

urlpatterns = [
    path("scheduled/", include(scheduled_patterns)),
]