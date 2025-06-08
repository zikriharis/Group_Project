from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Campaign


def campaign_list(request):
    """Display all active campaigns for browsing"""
    campaigns = Campaign.objects.filter(status="active").select_related("organization")

    # Add progress calculation for each campaign
    for campaign in campaigns:
        total_raised = (
            campaign.donations.filter(status="confirmed").aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )
        campaign.progress_percentage = (
            min((total_raised / campaign.goal_amount) * 100, 100)
            if campaign.goal_amount > 0
            else 0
        )
        campaign.total_raised = total_raised

    context = {"campaigns": campaigns}
    return render(request, "campaigns/list.html", context)


def campaign_detail(request, campaign_id):
    """Display detailed view of a single campaign"""
    campaign = get_object_or_404(Campaign, id=campaign_id)

    # Calculate campaign progress
    total_raised = (
        campaign.donations.filter(status="confirmed").aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )
    progress_percentage = (
        min((total_raised / campaign.goal_amount) * 100, 100)
        if campaign.goal_amount > 0
        else 0
    )

    # Get recent donations for social proof
    recent_donations = (
        campaign.donations.filter(status="confirmed")
        .exclude(is_anonymous=True)
        .order_by("-created_at")[:10]
    )

    context = {
        "campaign": campaign,
        "total_raised": total_raised,
        "progress_percentage": progress_percentage,
        "recent_donations": recent_donations,
    }
    return render(request, "campaigns/detail.html", context)
