from django.contrib import admin
from .models import User,Profile, CampaignManagerAssignment

'''
fields – to whitelist specific fields,
exclude – to hide certain fields.
list display only affects the list view — the table of users you see at /admin/auth/user/, defines which columns 
appear in that list/table
this won’t block a superuser from accessing the data via shell or other means — but it hides 
fields from the admin UI form.
'''

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')

@admin.register(CampaignManagerAssignment)
class CampaignManagerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'organization', 'created_at')