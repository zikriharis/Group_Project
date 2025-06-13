from django.contrib import admin
from .models import Organization
'''
Register your models here.
decorator that registers the Organization model with the admin site
=admin.site.register(Organization, OrganizationAdmin)
associate it with a custom admin class (OrganizationAdmin in this case)
Inherits from `admin.ModelAdmin`, which gives you many options to customize how the model 
appears in the admin interface.
'''
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'contact_email')
    '''
    defines the columns that will be shown in the list view
    of the Django admin panel for the Organization model
    instead of just showing the default (e.g., string version like __str__()) shows name, country, website and email
    '''


