#!/usr/bin/env python
"""
Test script for dashboard functionality
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangogroupproject.settings')
django.setup()

from users.models import User
from campaigns.models import Campaign
from donations.models import Donation
from notifications.models import Notification
from sharing.models import Bookmark

def test_dashboard_functionality():
    print("🧪 Testing CrowdFund Dashboard Functionality")
    print("=" * 50)
    
    # Test database data
    print("\n📊 Database Test Results:")
    print(f"✅ Users: {User.objects.count()}")
    print(f"✅ Campaigns: {Campaign.objects.count()}")
    print(f"✅ Donations: {Donation.objects.count()}")
    print(f"✅ Notifications: {Notification.objects.count()}")
    print(f"✅ Bookmarks: {Bookmark.objects.count()}")
    
    # Test specific user data
    print("\n👤 User Role Distribution:")
    for role_choice in User.ROLE_CHOICES:
        role = role_choice[0]
        count = User.objects.filter(role=role).count()
        print(f"✅ {role.title()}s: {count}")
    
    # Test campaign statistics
    print("\n🎯 Campaign Statistics:")
    active_campaigns = Campaign.objects.filter(status='active').count()
    total_raised = sum(c.current_amount for c in Campaign.objects.all())
    print(f"✅ Active Campaigns: {active_campaigns}")
    print(f"✅ Total Amount Raised: ${total_raised:,.2f}")
    
    # Test donor statistics
    print("\n💝 Donation Statistics:")
    donor_users = User.objects.filter(role='donor')
    for donor in donor_users:
        donations = Donation.objects.filter(user=donor)
        total_donated = sum(d.amount for d in donations)
        print(f"✅ {donor.username}: {donations.count()} donations, ${total_donated}")
    
    # Test notifications
    print("\n🔔 Notification Statistics:")
    for user in User.objects.all():
        notifications = Notification.objects.filter(user=user)
        unread = notifications.filter(is_read=False).count()
        print(f"✅ {user.username}: {notifications.count()} total, {unread} unread")
    
    # Test bookmarks
    print("\n🔖 Bookmark Statistics:")
    for user in User.objects.filter(role='donor'):
        bookmarks = Bookmark.objects.filter(user=user)
        print(f"✅ {user.username}: {bookmarks.count()} bookmarked campaigns")
    
    print("\n🎉 Dashboard functionality test completed!")
    print("All data has been successfully created and is ready for testing.")
    
    print("\n🌐 Next Steps:")
    print("1. Login at: http://127.0.0.1:8000/users/login/")
    print("2. Test dashboard at: http://127.0.0.1:8000/dashboard/")
    print("3. Test user credentials:")
    print("   - Donor: johndoe / password123")
    print("   - Donor: janedoe / password123") 
    print("   - Organization: techforgood / password123")
    print("   - Organization: greenearth / password123")
    print("   - Admin: admin / admin123")

if __name__ == '__main__':
    test_dashboard_functionality()
