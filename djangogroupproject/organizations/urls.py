from django.urls import path
from . import views

app_name = 'organizations'

urlpatterns = [
    path('apply/', views.apply_for_organization, name='apply_for_organization'),
    
    # Admin review paths
    path('admin/pending/', views.admin_pending_organizations, name='admin_pending_organizations'),
    path('admin/review/<uuid:organization_id>/', views.admin_review_organization, name='admin_review_organization'),
]
