from django.urls import path
from . import views

app_name = "donations"

urlpatterns = [
    path("donate/<uuid:campaign_id>/", views.make_donation, name="make_donation"),
    path(
        "success/<uuid:donation_id>/", views.donation_success, name="donation_success"
    ),
    path("my-donations/", views.my_donations, name="my_donations"),
    path("recurring/", views.manage_recurring, name="manage_recurring"),
]
