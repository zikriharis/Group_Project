from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
import json

from campaigns.models import Campaign
from sharing.models import Bookmark
from notifications.models import Notification

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def toggle_bookmark(request):
    """Toggle bookmark status for a campaign"""
    try:
        data = json.loads(request.body)
        campaign_id = data.get('campaign_id')
        
        if not campaign_id:
            return JsonResponse({'error': 'Campaign ID is required'}, status=400)
        
        campaign = get_object_or_404(Campaign, id=campaign_id)
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            campaign=campaign
        )
        
        if not created:
            bookmark.delete()
            bookmarked = False
            message = 'Campaign removed from bookmarks'
        else:
            bookmarked = True
            message = 'Campaign bookmarked successfully'
        
        return JsonResponse({
            'bookmarked': bookmarked,
            'message': message,
            'bookmark_count': Bookmark.objects.filter(campaign=campaign).count()
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def mark_notification_read(request):
    """Mark a notification as read"""
    try:
        data = json.loads(request.body)
        notification_id = data.get('notification_id')
        
        if not notification_id:
            return JsonResponse({'error': 'Notification ID is required'}, status=400)
        
        notification = get_object_or_404(
            Notification, 
            id=notification_id, 
            user=request.user
        )
        
        notification.is_read = True
        notification.save()
        
        # Get updated unread count
        unread_count = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).count()
        
        return JsonResponse({
            'success': True,
            'message': 'Notification marked as read',
            'unread_count': unread_count
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def mark_all_notifications_read(request):
    """Mark all notifications as read for the current user"""
    try:
        updated_count = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).update(is_read=True)
        
        return JsonResponse({
            'success': True,
            'message': f'Marked {updated_count} notifications as read',
            'unread_count': 0
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_notifications(request):
    """Get notifications for the current user"""
    try:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:20]
        
        notifications_data = []
        for notification in notifications:
            notifications_data.append({
                'id': str(notification.id),
                'title': notification.title,
                'message': notification.message,
                'type': notification.notification_type,
                'is_read': notification.is_read,
                'created_at': notification.created_at.isoformat(),
                'related_url': notification.related_url or '#'
            })
        
        unread_count = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).count()
        
        return JsonResponse({
            'notifications': notifications_data,
            'unread_count': unread_count
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_dashboard_stats(request):
    """Get dashboard statistics for the current user"""
    try:
        user = request.user
        stats = {}
        
        if user.profile.role == 'donor':
            from donations.models import Donation
            from django.db.models import Sum
            
            donations = Donation.objects.filter(user=user)
            stats.update({
                'total_donations': donations.count(),
                'total_amount_donated': donations.aggregate(
                    total=Sum('amount')
                )['total'] or 0,
                'bookmarked_campaigns': Bookmark.objects.filter(user=user).count(),
                'active_campaigns_supported': donations.values('campaign').distinct().count()
            })
            
        elif user.profile.role == 'organization':
            from django.db.models import Sum, Count
            
            campaigns = Campaign.objects.filter(organization__user=user)
            stats.update({
                'total_campaigns': campaigns.count(),
                'active_campaigns': campaigns.filter(status='active').count(),
                'total_raised': campaigns.aggregate(
                    total=Sum('current_amount')
                )['total'] or 0,
                'total_donors': campaigns.aggregate(
                    donors=Count('donations__user', distinct=True)
                )['donors'] or 0
            })
        
        # Common stats
        stats.update({
            'unread_notifications': Notification.objects.filter(
                user=user, is_read=False
            ).count(),
            'profile_completion': calculate_profile_completion(user)
        })
        
        return JsonResponse({'stats': stats})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def calculate_profile_completion(user):
    """Calculate profile completion percentage"""
    fields_to_check = [
        user.first_name,
        user.last_name,
        user.email,
        user.profile.bio,
        user.profile.location,
        user.profile.phone_number
    ]
    
    completed_fields = sum(1 for field in fields_to_check if field)
    return int((completed_fields / len(fields_to_check)) * 100)

@login_required
def get_recent_activity(request):
    """Get recent activity for the current user"""
    try:
        activities = []
        
        # Get recent donations
        if hasattr(request.user, 'donations'):
            from donations.models import Donation
            recent_donations = Donation.objects.filter(
                user=request.user
            ).order_by('-created_at')[:5]
            
            for donation in recent_donations:
                activities.append({
                    'type': 'donation',
                    'title': f'Donated ${donation.amount}',
                    'description': f'to {donation.campaign.title}',
                    'date': donation.created_at.isoformat(),
                    'url': f'/campaigns/{donation.campaign.id}/'
                })
        
        # Get recent campaigns (for organizations)
        if request.user.profile.role == 'organization':
            recent_campaigns = Campaign.objects.filter(
                organization__user=request.user
            ).order_by('-created_at')[:5]
            
            for campaign in recent_campaigns:
                activities.append({
                    'type': 'campaign',
                    'title': f'Campaign: {campaign.title}',
                    'description': f'Status: {campaign.status}',
                    'date': campaign.created_at.isoformat(),
                    'url': f'/campaigns/{campaign.id}/'
                })
        
        # Sort activities by date
        activities.sort(key=lambda x: x['date'], reverse=True)
        
        return JsonResponse({'activities': activities[:10]})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["GET"])
def real_time_dashboard_data(request):
    """Get real-time dashboard data for updates"""
    try:
        user = request.user
        
        # Import the dashboard data functions
        from .views import get_donor_dashboard_data, get_organization_dashboard_data, get_manager_dashboard_data, get_admin_dashboard_data
        
        # Get updated data based on user role
        if user.role == 'donor':
            data = get_donor_dashboard_data(user)
        elif user.role == 'organization':
            data = get_organization_dashboard_data(user)
        elif user.role == 'manager':
            data = get_manager_dashboard_data(user)
        elif user.role == 'admin':
            data = get_admin_dashboard_data(user)
        else:
            return JsonResponse({'error': 'Invalid user role'}, status=400)
        
        # Extract relevant statistics for real-time updates
        stats = {}
        charts = {}
        
        if user.role == 'donor':
            stats = {
                'total_donated': data.get('total_donated', 0),
                'donation_count': data.get('donation_count', 0),
                'bookmarks_count': len(data.get('bookmarks', []))
            }
            charts = {
                'monthly_donations': data.get('monthly_donations'),
                'category_donations': data.get('category_donations')
            }
        elif user.role == 'organization':
            stats = {
                'total_campaigns': data.get('total_campaigns', 0),
                'active_campaigns': data.get('active_campaigns', 0),
                'total_raised': data.get('total_raised', 0),
                'total_donations': data.get('total_donations', 0)
            }
            charts = {
                'monthly_raised': data.get('monthly_raised'),
                'status_breakdown': data.get('status_breakdown')
            }
        elif user.role == 'admin':
            stats = {
                'total_campaigns': data.get('total_campaigns', 0),
                'total_organizations': data.get('total_organizations', 0),
                'total_users': data.get('total_users', 0),
                'total_platform_raised': data.get('total_platform_raised', 0)
            }
            charts = {
                'monthly_stats': data.get('monthly_stats'),
                'user_roles': data.get('user_roles')
            }
        
        return JsonResponse({
            'success': True,
            'stats': stats,
            'charts': charts,
            'timestamp': timezone.now().isoformat()
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
