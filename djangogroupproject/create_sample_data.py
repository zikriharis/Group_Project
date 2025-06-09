#!/usr/bin/env python
"""
Sample data creation script for the CrowdFund platform
"""
import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangogroupproject.settings')
django.setup()

from users.models import User, Profile
from campaigns.models import Campaign
from organizations.models import Organization
from donations.models import Donation
from notifications.models import Notification
from sharing.models import Bookmark

def create_sample_data():
    print("Creating sample data for CrowdFund platform...")
    
    # Create sample donor users
    donor1, created = User.objects.get_or_create(
        username='johndoe',
        defaults={
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'donor'
        }
    )
    if created:
        donor1.set_password('password123')
        donor1.save()
        Profile.objects.create(
            user=donor1,
            role='donor',
            bio='Passionate about supporting innovative projects',
            location='New York, NY'
        )
        print(f"Created donor user: {donor1.username}")
    
    donor2, created = User.objects.get_or_create(
        username='janedoe',
        defaults={
            'email': 'jane@example.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'role': 'donor'
        }
    )
    if created:
        donor2.set_password('password123')
        donor2.save()
        Profile.objects.create(
            user=donor2,
            role='donor',
            bio='Supporting education and healthcare initiatives',
            location='Los Angeles, CA'
        )
        print(f"Created donor user: {donor2.username}")
    
    # Create sample organization users
    org1, created = User.objects.get_or_create(
        username='techforgood',
        defaults={
            'email': 'contact@techforgood.org',
            'first_name': 'Tech',
            'last_name': 'ForGood',
            'role': 'organization'
        }
    )
    if created:
        org1.set_password('password123')
        org1.save()
        Profile.objects.create(
            user=org1,
            role='organization',
            bio='Technology organization focused on social impact',
            location='San Francisco, CA'
        )
        print(f"Created organization user: {org1.username}")
    
    org2, created = User.objects.get_or_create(
        username='greenearth',
        defaults={
            'email': 'info@greenearth.org',
            'first_name': 'Green',
            'last_name': 'Earth',
            'role': 'organization'
        }
    )
    if created:
        org2.set_password('password123')
        org2.save()
        Profile.objects.create(
            user=org2,
            role='organization',
            bio='Environmental organization protecting our planet',
            location='Seattle, WA'
        )
        print(f"Created organization user: {org2.username}")
      # Create sample organizations
    tech_org, created = Organization.objects.get_or_create(
        name='Tech for Good Foundation',
        defaults={
            'description': 'We leverage technology to solve social problems',
            'website': 'https://techforgood.org',
            'contact_email': 'contact@techforgood.org',
            'address': '123 Innovation St, San Francisco, CA 94105'
        }
    )
    if created:
        print(f"Created organization: {tech_org.name}")
    
    green_org, created = Organization.objects.get_or_create(
        name='Green Earth Initiative',
        defaults={
            'description': 'Protecting and preserving our environment for future generations',
            'website': 'https://greenearth.org',
            'contact_email': 'info@greenearth.org',
            'address': '456 Forest Ave, Seattle, WA 98101'
        }
    )
    if created:
        print(f"Created organization: {green_org.name}")
      # Create sample campaigns
    campaign1, created = Campaign.objects.get_or_create(
        title='Clean Water for Rural Communities',
        defaults={
            'organization': green_org,
            'slug': 'clean-water-rural-communities',
            'brief_description': 'Providing clean, safe drinking water to rural communities in developing countries.',
            'text': '''
            Access to clean water is a fundamental human right, yet millions of people worldwide lack this basic necessity. 
            Our Clean Water for Rural Communities project aims to install water purification systems in remote villages, 
            providing sustainable access to safe drinking water.
            
            Your donation will help us:
            - Install water purification systems
            - Train local technicians for maintenance
            - Provide ongoing support and monitoring
            - Ensure long-term sustainability
            ''',
            'goal_amount': Decimal('50000.00'),
            'current_amount': Decimal('15750.00'),
            'start_date': datetime.now().date() - timedelta(days=30),
            'end_date': datetime.now().date() + timedelta(days=60),
            'status': 'active',
            'country': 'Global',
            'currency_campaign': 'USD'
        }
    )
    if created:
        print(f"Created campaign: {campaign1.title}")
    
    campaign2, created = Campaign.objects.get_or_create(
        title='AI for Healthcare Research',
        defaults={
            'organization': tech_org,
            'slug': 'ai-healthcare-research',
            'brief_description': 'Developing AI solutions to accelerate medical research and improve patient outcomes.',
            'text': '''
            Artificial Intelligence has the potential to revolutionize healthcare by accelerating research, 
            improving diagnostic accuracy, and personalizing treatment plans. Our AI for Healthcare Research 
            project focuses on developing cutting-edge AI tools for medical professionals.
            
            Project Goals:
            - Develop AI diagnostic tools
            - Create predictive models for disease prevention
            - Improve treatment recommendation systems
            - Make healthcare more accessible and affordable
            ''',
            'goal_amount': Decimal('100000.00'),
            'current_amount': Decimal('67500.00'),
            'start_date': datetime.now().date() - timedelta(days=45),
            'end_date': datetime.now().date() + timedelta(days=45),
            'status': 'active',
            'country': 'USA',
            'currency_campaign': 'USD'
        }
    )
    if created:
        print(f"Created campaign: {campaign2.title}")
    
    campaign3, created = Campaign.objects.get_or_create(
        title='Education Technology for Underprivileged Students',
        defaults={
            'organization': tech_org,
            'slug': 'education-technology-students',
            'brief_description': 'Providing tablets and educational software to students in underserved communities.',
            'text': '''
            Education is the key to breaking the cycle of poverty. Our Education Technology project aims to 
            provide tablets loaded with educational software to students in underserved communities, giving 
            them access to quality learning resources.
            
            What we provide:
            - Tablets with educational content
            - Internet connectivity solutions
            - Teacher training programs
            - Ongoing technical support
            ''',
            'goal_amount': Decimal('75000.00'),
            'current_amount': Decimal('32100.00'),
            'start_date': datetime.now().date() - timedelta(days=20),
            'end_date': datetime.now().date() + timedelta(days=70),
            'status': 'active',
            'country': 'Global',
            'currency_campaign': 'USD'
        }
    )
    if created:
        print(f"Created campaign: {campaign3.title}")
      # Create sample donations
    donations_data = [
        {'user': donor1, 'campaign': campaign1, 'amount': Decimal('250.00')},
        {'user': donor1, 'campaign': campaign2, 'amount': Decimal('500.00')},
        {'user': donor1, 'campaign': campaign3, 'amount': Decimal('150.00')},
        {'user': donor2, 'campaign': campaign1, 'amount': Decimal('100.00')},
        {'user': donor2, 'campaign': campaign2, 'amount': Decimal('300.00')},
        {'user': donor2, 'campaign': campaign3, 'amount': Decimal('200.00')},
    ]
    
    for donation_data in donations_data:
        donation, created = Donation.objects.get_or_create(
            user=donation_data['user'],
            campaign=donation_data['campaign'],
            amount=donation_data['amount'],
            defaults={
                'currency_donation': 'USD',
                'status': 'confirmed',
                'payment_reference': f'PAY-{donation_data["amount"]}-{donation_data["user"].username[:3].upper()}',
                'confirmed_at': timezone.now() - timedelta(days=10)
            }
        )
        if created:
            print(f"Created donation: ${donation.amount} from {donation.user.username} to {donation.campaign.title}")
    
    # Create sample bookmarks
    bookmarks_data = [
        {'user': donor1, 'campaign': campaign2},
        {'user': donor1, 'campaign': campaign3},
        {'user': donor2, 'campaign': campaign1},
        {'user': donor2, 'campaign': campaign3},
    ]
    
    for bookmark_data in bookmarks_data:
        bookmark, created = Bookmark.objects.get_or_create(
            user=bookmark_data['user'],
            campaign=bookmark_data['campaign']
        )
        if created:
            print(f"Created bookmark: {bookmark.user.username} bookmarked {bookmark.campaign.title}")
      # Create sample notifications
    notifications_data = [
        {
            'user': donor1,
            'message': 'Your donation to Clean Water for Rural Communities has been received.',
            'notification_type': 'donation'
        },
        {
            'user': donor1,
            'message': 'AI for Healthcare Research has reached 67% of its funding goal!',
            'notification_type': 'campaign_update'
        },
        {
            'user': donor2,
            'message': 'A new education campaign matches your interests.',
            'notification_type': 'general'
        },
        {
            'user': org1,
            'message': 'Your AI for Healthcare Research campaign has reached $67,500!',
            'notification_type': 'milestone'
        },
        {
            'user': org2,
            'message': 'You received a new donation of $250 for Clean Water project.',
            'notification_type': 'donation'        }
    ]
    
    for notif_data in notifications_data:
        notification, created = Notification.objects.get_or_create(
            user=notif_data['user'],
            message=notif_data['message'],
            type=notif_data['notification_type'],
            defaults={
                'is_read': False,
                'created_at': timezone.now() - timedelta(hours=2)
            }
        )
        if created:
            print(f"Created notification for {notification.user.username}: {notification.type}")
    
    print("\n✅ Sample data creation completed successfully!")
    print("\nTest users created:")
    print("- Donors: johndoe, janedoe (password: password123)")
    print("- Organizations: techforgood, greenearth (password: password123)")
    print("- Admin: admin (password: admin123)")
    print("\nYou can now test the dashboard with realistic data!")

if __name__ == '__main__':
    create_sample_data()
