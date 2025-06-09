# filepath: dashboard/urls.py
from django.urls import path
from . import views, api_views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard pages
    path('', views.dashboard_home, name='home'),
    path('donations/', views.dashboard_donations, name='donations'),
    path('campaigns/', views.dashboard_campaigns, name='campaigns'),
    path('bookmarks/', views.dashboard_bookmarks, name='bookmarks'),
    path('notifications/', views.dashboard_notifications, name='notifications'),
      # API endpoints
    path('api/toggle-bookmark/', api_views.toggle_bookmark, name='api_toggle_bookmark'),
    path('api/mark-notification-read/', api_views.mark_notification_read, name='api_mark_notification_read'),
    path('api/mark-all-notifications-read/', api_views.mark_all_notifications_read, name='api_mark_all_notifications_read'),
    path('api/notifications/', api_views.get_notifications, name='api_get_notifications'),
    path('api/stats/', api_views.get_dashboard_stats, name='api_get_stats'),
    path('api/activity/', api_views.get_recent_activity, name='api_get_activity'),
    path('api/real-time-data/', api_views.real_time_dashboard_data, name='api_real_time_data'),
]
