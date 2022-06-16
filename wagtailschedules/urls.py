from django.urls import path

from .views import ScheduledPagesView, publish_all_scheduled_now, publish_now

app_name = 'wagtailschedules'

urlpatterns = [
    path("reports/scheduled", ScheduledPagesView.as_view(), name="scheduled_pages"),
    path("reports/scheduled/<int:page_id>/publish_now/", publish_now, name='publish_now'),
    path("reports/scheduled/publish_all_now/", publish_all_scheduled_now, name='publish_all_now'),
]