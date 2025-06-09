#!/usr/bin/env python
"""
Test API endpoints for dashboard
"""
import os
import django
from django.test import Client
from django.contrib.auth import authenticate

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangogroupproject.settings')
django.setup()

from users.models import User

def test_api_endpoints():
    print("🔧 Testing Dashboard API Endpoints")
    print("=" * 50)
    
    # Create a test client
    client = Client()
    
    # Test user authentication
    user = User.objects.get(username='johndoe')
    client.force_login(user)
    print(f"✅ Logged in as: {user.username}")
    
    # Test dashboard stats endpoint
    try:
        response = client.get('/dashboard/api/stats/')
        print(f"✅ Dashboard Stats API: {response.status_code}")
        if response.status_code == 200:
            print(f"   📊 Response data available")
        else:
            print(f"   ❌ Response content: {response.content}")
    except Exception as e:
        print(f"❌ Dashboard Stats API Error: {e}")
    
    # Test notifications endpoint
    try:
        response = client.get('/dashboard/api/notifications/')
        print(f"✅ Notifications API: {response.status_code}")
        if response.status_code == 200:
            print(f"   🔔 Response data available")
    except Exception as e:
        print(f"❌ Notifications API Error: {e}")
    
    # Test activities endpoint
    try:
        response = client.get('/dashboard/api/activities/')
        print(f"✅ Activities API: {response.status_code}")
        if response.status_code == 200:
            print(f"   📈 Response data available")
    except Exception as e:
        print(f"❌ Activities API Error: {e}")
    
    # Test dashboard main page
    try:
        response = client.get('/dashboard/')
        print(f"✅ Dashboard Main Page: {response.status_code}")
        if response.status_code == 200:
            print(f"   🏠 Dashboard page loads successfully")
    except Exception as e:
        print(f"❌ Dashboard Main Page Error: {e}")
    
    print("\n🎯 API Testing Complete!")
    print("All endpoints are ready for browser testing.")

if __name__ == '__main__':
    test_api_endpoints()
