from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
import json
from campaigns.models import Campaign
from donations.models import Donation
from organizations.models import Organization
from sharing.models import Bookmark, Share
from notifications.models import Notification

@login_required
def dashboard_home(request):
    """Main dashboard view with overview statistics"""
    user = request.user
    context = {
        'user': user,
        'current_page': 'dashboard'
    }
    
    # Get user-specific data based on role
    if user.role == 'donor':
        context.update(get_donor_dashboard_data(user))
    elif user.role == 'organization':
        context.update(get_organization_dashboard_data(user))
    elif user.role == 'manager':
        context.update(get_manager_dashboard_data(user))
    elif user.role == 'admin':
        context.update(get_admin_dashboard_data(user))
    
    return render(request, 'dashboard/home.html', context)

def get_donor_dashboard_data(user):
    """Get dashboard data specific to donors"""
    # Get donation statistics
    donations = Donation.objects.filter(user=user)
    total_donated = donations.aggregate(Sum('amount'))['amount__sum'] or 0
    donation_count = donations.count()
    
    # Get recent donations
    recent_donations = donations.order_by('-created_at')[:5]
    
    # Get bookmarked campaigns
    bookmarks = Bookmark.objects.filter(user=user).select_related('campaign')[:5]
    
    # Get recommended campaigns (based on previous donations)
    donated_campaigns = donations.values_list('campaign', flat=True)
    recommended_campaigns = Campaign.objects.filter(
        status='active'
    ).exclude(id__in=donated_campaigns)[:6]
    
    # Get monthly donation data for chart
    monthly_donations = []
    for i in range(6):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        month_total = donations.filter(
            created_at__gte=month_start,
            created_at__lt=month_end
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_donations.append({
            'month': month_start.strftime('%b %Y'),
            'amount': float(month_total)
        })
    monthly_donations.reverse()
    
    # Get favorite categories
    category_donations = donations.values('campaign__category').annotate(
        total=Sum('amount')
    ).order_by('-total')[:5]
    
    return {
        'total_donated': total_donated,
        'donation_count': donation_count,
        'recent_donations': recent_donations,
        'bookmarks': bookmarks,
        'recommended_campaigns': recommended_campaigns,
        'monthly_donations': json.dumps(monthly_donations),
        'category_donations': json.dumps(list(category_donations)),
        'dashboard_type': 'donor'
    }
    
    return {
        'total_donated': total_donated,
        'donation_count': donation_count,
        'recent_donations': recent_donations,
        'bookmarks': bookmarks,
        'recommended_campaigns': recommended_campaigns,
        'dashboard_type': 'donor'
    }

def get_organization_dashboard_data(user):
    """Get dashboard data specific to organizations"""
    try:
        # Get the organization associated with this user
        organization = Organization.objects.get(contact_email=user.email)
        
        # Get campaigns for this organization
        campaigns = Campaign.objects.filter(organization=organization)
        active_campaigns = campaigns.filter(status='active')
        
        # Get funding statistics
        total_raised = campaigns.aggregate(Sum('current_amount'))['current_amount__sum'] or 0
        total_goal = campaigns.aggregate(Sum('goal_amount'))['goal_amount__sum'] or 0
        
        # Get donation statistics
        donations = Donation.objects.filter(campaign__organization=organization)
        total_donations = donations.count()
        recent_donations = donations.order_by('-created_at')[:5]
        
        # Get monthly fundraising data for chart
        monthly_raised = []
        for i in range(6):
            month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            month_total = donations.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            monthly_raised.append({
                'month': month_start.strftime('%b %Y'),
                'amount': float(month_total)
            })
        monthly_raised.reverse()
        
        # Campaign status breakdown
        status_breakdown = campaigns.values('status').annotate(
            count=Count('id')
        )
        
        return {
            'organization': organization,
            'total_campaigns': campaigns.count(),
            'active_campaigns': active_campaigns.count(),
            'total_raised': total_raised,
            'total_goal': total_goal,
            'total_donations': total_donations,
            'recent_donations': recent_donations,
            'campaigns': campaigns[:5],
            'monthly_raised': json.dumps(monthly_raised),
            'status_breakdown': json.dumps(list(status_breakdown)),
            'dashboard_type': 'organization'
        }
    except Organization.DoesNotExist:
        return {
            'organization': None,
            'monthly_raised': json.dumps([]),
            'status_breakdown': json.dumps([]),
            'dashboard_type': 'organization'
        }

def get_manager_dashboard_data(user):
    """Get dashboard data specific to campaign managers"""
    from users.models import CampaignManagerAssignment
    
    # Get assigned campaigns
    assignments = CampaignManagerAssignment.objects.filter(user=user)
    campaigns = Campaign.objects.filter(managers__user=user)
    
    # Get performance metrics
    total_raised = campaigns.aggregate(Sum('current_amount'))['current_amount__sum'] or 0
    donations = Donation.objects.filter(campaign__in=campaigns)
    
    return {
        'assigned_campaigns': campaigns.count(),
        'total_raised': total_raised,
        'total_donations': donations.count(),
        'campaigns': campaigns[:5],
        'dashboard_type': 'manager'
    }

def get_admin_dashboard_data(user):
    """Get dashboard data specific to admins"""
    # Platform-wide statistics
    total_campaigns = Campaign.objects.count()
    active_campaigns = Campaign.objects.filter(status='active').count()
    total_organizations = Organization.objects.count()
    total_users = user.__class__.objects.count()
    
    # Financial statistics
    total_platform_raised = Campaign.objects.aggregate(Sum('current_amount'))['current_amount__sum'] or 0
    total_donations = Donation.objects.count()
    
    # Recent activity
    recent_campaigns = Campaign.objects.order_by('-created_at')[:5]
    recent_organizations = Organization.objects.order_by('-created_at')[:5]
    
    # Monthly platform stats for chart
    monthly_stats = []
    for i in range(6):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        
        month_donations = Donation.objects.filter(
            created_at__gte=month_start,
            created_at__lt=month_end
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        month_campaigns = Campaign.objects.filter(
            created_at__gte=month_start,
            created_at__lt=month_end
        ).count()
        
        monthly_stats.append({
            'month': month_start.strftime('%b %Y'),
            'donations': float(month_donations),
            'campaigns': month_campaigns
        })
    monthly_stats.reverse()
    
    # User role breakdown
    user_roles = user.__class__.objects.values('role').annotate(
        count=Count('id')
    )
    
    return {
        'total_campaigns': total_campaigns,
        'active_campaigns': active_campaigns,
        'total_organizations': total_organizations,
        'total_users': total_users,
        'total_platform_raised': total_platform_raised,
        'total_donations': total_donations,
        'recent_campaigns': recent_campaigns,
        'recent_organizations': recent_organizations,
        'monthly_stats': json.dumps(monthly_stats),
        'user_roles': json.dumps(list(user_roles)),
        'dashboard_type': 'admin'
    }

@login_required
def dashboard_donations(request):
    """View for detailed donation history"""
    user = request.user
    donations = Donation.objects.filter(user=user).order_by('-created_at')
    
    # Calculate statistics
    stats = donations.aggregate(
        total_amount=Sum('amount'),
        total_count=Count('id')
    )
    
    context = {
        'donations': donations,
        'stats': stats,
        'current_page': 'donations'
    }
    
    return render(request, 'dashboard/donations.html', context)

@login_required
def dashboard_campaigns(request):
    """View for managing user's campaigns (for organizations/managers)"""
    user = request.user
    
    if user.role == 'organization':
        try:
            organization = Organization.objects.get(contact_email=user.email)
            campaigns = Campaign.objects.filter(organization=organization)
        except Organization.DoesNotExist:
            campaigns = Campaign.objects.none()
    elif user.role == 'manager':
        campaigns = Campaign.objects.filter(managers__user=user)
    else:
        campaigns = Campaign.objects.none()
    
    context = {
        'campaigns': campaigns,
        'current_page': 'campaigns'
    }
    
    return render(request, 'dashboard/campaigns.html', context)

@login_required 
def dashboard_bookmarks(request):
    """View for managing bookmarked campaigns"""
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('campaign')
    
    context = {
        'bookmarks': bookmarks,
        'current_page': 'bookmarks'
    }
    
    return render(request, 'dashboard/bookmarks.html', context)

@login_required
def dashboard_notifications(request):
    """View for managing notifications"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark notifications as read when viewed
    notifications.filter(is_read=False).update(is_read=True)
    
    context = {
        'notifications': notifications,
        'current_page': 'notifications'
    }
    
    return render(request, 'dashboard/notifications.html', context)
