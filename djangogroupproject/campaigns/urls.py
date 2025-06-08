from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('', views.campaign_list, name='list'),
    path('<uuid:campaign_id>/', views.campaign_detail, name='detail'),
]