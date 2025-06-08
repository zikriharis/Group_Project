from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Donation, DonationBadge
from campaigns.models import Campaign
import uuid


def make_donation(request, campaign_id):
    """Handle donation form and processing"""
    campaign = get_object_or_404(Campaign, id=campaign_id)

    # Calculate how much has been raised so far
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
    remaining_amount = max(campaign.goal_amount - total_raised, 0)

    if request.method == "POST":
        amount = float(request.POST.get("amount", 0))
        donor_name = request.POST.get("donor_name", "")
        is_anonymous = request.POST.get("is_anonymous") == "on"

        # Basic validation
        if amount < 5:
            messages.error(request, "Minimum donation amount is RM 5.00")
        else:
            # Create the donation record
            donation = Donation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                campaign=campaign,
                amount=amount,
                donor_name=(
                    donor_name
                    if donor_name
                    else (
                        request.user.get_full_name()
                        if request.user.is_authenticated
                        else "Anonymous"
                    )
                ),
                is_anonymous=is_anonymous,
                status="confirmed",  # Skip payment processing for now
                payment_reference=f'DON-{timezone.now().strftime("%Y%m%d%H%M%S")}-{str(uuid.uuid4())[:8]}',
                confirmed_at=timezone.now(),
            )

            # Check if user deserves any badges
            if request.user.is_authenticated:
                total_donated = (
                    Donation.objects.filter(
                        user=request.user, status="confirmed"
                    ).aggregate(Sum("amount"))["amount__sum"]
                    or 0
                )

                # Award badges based on total donations
                if (
                    total_donated >= 1000
                    and not DonationBadge.objects.filter(
                        user=request.user, badge_type="generous_donor"
                    ).exists()
                ):
                    DonationBadge.objects.create(
                        user=request.user, badge_type="generous_donor"
                    )
                elif (
                    total_donated >= 5000
                    and not DonationBadge.objects.filter(
                        user=request.user, badge_type="champion"
                    ).exists()
                ):
                    DonationBadge.objects.create(
                        user=request.user, badge_type="champion"
                    )
                elif (
                    Donation.objects.filter(
                        user=request.user, status="confirmed"
                    ).count()
                    == 1
                ):
                    # First donation badge
                    DonationBadge.objects.create(
                        user=request.user, badge_type="first_donation"
                    )

            messages.success(
                request,
                f"Thank you! Your donation of RM {amount:.2f} has been confirmed.",
            )
            return redirect("donations:donation_success", donation_id=donation.id)

    # Show recent donations for social proof
    recent_donations = (
        campaign.donations.filter(status="confirmed")
        .exclude(is_anonymous=True)
        .order_by("-created_at")[:5]
    )

    context = {
        "campaign": campaign,
        "total_raised": total_raised,
        "progress_percentage": progress_percentage,
        "remaining_amount": remaining_amount,
        "recent_donations": recent_donations,
    }
    return render(request, "donations/make_donation.html", context)


def donation_success(request, donation_id):
    """Thank you page after successful donation"""
    donation = get_object_or_404(Donation, id=donation_id)

    # Update campaign totals for display
    total_raised = (
        donation.campaign.donations.filter(status="confirmed").aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )
    progress_percentage = min((total_raised / donation.campaign.goal_amount) * 100, 100)

    context = {
        "donation": donation,
        "total_raised": total_raised,
        "progress_percentage": progress_percentage,
    }
    return render(request, "donations/success.html", context)


@login_required
def my_donations(request):
    """User's donation history and stats"""
    donations = (
        Donation.objects.filter(user=request.user)
        .select_related("campaign")
        .order_by("-created_at")
    )

    # Calculate user statistics
    total_donated = (
        donations.filter(status="confirmed").aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    donation_count = donations.filter(status="confirmed").count()
    campaigns_supported = (
        donations.filter(status="confirmed").values("campaign").distinct().count()
    )
    badges = DonationBadge.objects.filter(user=request.user).order_by("-awarded_at")

    # Get monthly totals for the last 6 months
    from datetime import datetime, timedelta

    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_donations = (
        donations.filter(status="confirmed", created_at__gte=six_months_ago)
        .extra(select={"month": 'strftime("%%Y-%%m", created_at)'})
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    context = {
        "donations": donations,
        "total_donated": total_donated,
        "donation_count": donation_count,
        "campaigns_supported": campaigns_supported,
        "badges": badges,
        "monthly_donations": monthly_donations,
    }
    return render(request, "donations/my_donations.html", context)


@login_required
def manage_recurring(request):
    """Manage user's recurring donations"""
    from .models import RecurringDonation

    recurring_donations = RecurringDonation.objects.filter(
        user=request.user
    ).select_related("campaign")

    context = {"recurring_donations": recurring_donations}
    return render(request, "donations/manage_recurring.html", context)
