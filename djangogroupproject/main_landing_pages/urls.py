from django.urls import path
from .views import LandingPageView

app_name = 'main_landing_pages'

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
]
