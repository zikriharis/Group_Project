""""
redirect: use to redirects to another URL/view
get_object_or_404: Tries to fetch an object, raises 404 error if not found
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CampaignForm, CampaignPageBlockForm, CampaignDocumentForm, FraudReportForm
from .models import Campaign

# Create your views here.
# Fetches all campaign list
def campaign_list(request):
    campaigns = Campaign.objects.filter(status='active')
    return render(request, 'campaigns/list.html', {'campaigns': campaigns})

# Fetches campaign using slug, gets all related blocks and documents, counts likes via reverse relationship like_set
def campaign_detail(request, slug):
    campaign = get_object_or_404(Campaign, slug = slug)
    blocks = campaign.blocks.all()
    documents = campaign.documents.all()
    likes = campaign.like_set.count()
    # Like.objects.filter(campaign=campaign, user=request.user)
    return render (request, 'campaigns/detail.html', {
        'campaign':campaign, 'blocks':blocks, 'documents':documents, 'likes':likes})

# If form submitted, create form instance using data and files, save campaign if valid, if not POST render empty form
@login_required
def campaign_create(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('campaign_list') # NEED TO CHANGE THIS to redirect to the campaign's detail page
    else:
        form = CampaignForm()
    return render(request, 'campaign/create.html', {'form':form})

# Find campaign-id, bind new block to campaign before saving, r
def campaign_block_add(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.method == 'POST':
        form = CampaignPageBlockForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a model instance from this form but don't save it to the database yet, useful when set additional
            # field, modify instance or assign foreignkey or current user
            block = form.save(commit=False)
            block.campaign = campaign
            block.save()
            return redirect('campaign_detail', slug=campaign.slug) # RECHECK
    else:
        form = CampaignPageBlockForm() # () make sure to include () so that reference point to instance and not class
    return render(request, 'campaigns/block_add.html', {'form':form})

# Same logic as blocks, but for documents
def campaign_document_add(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.method == 'POST':
        form = CampaignDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.campaign = campaign
            doc.save()
            return redirect('campaign_detail', slug=campaign.slug)
    else:
        form = CampaignDocumentForm()
    return render(request, 'campaigns/document_add.html', {'form':form})

'''
Gets the campaign being report, bind the fraud report to the campaign and current user, saves and redirects
'''
def fraud_report(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.method == 'POST':
        form = FraudReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.campaign = campaign
            report.reporter = request.user
            report.save()
            return redirect('campaign_detail', slug=campaign.slug)
    else:
        form = FraudReportForm()
    return render(request, 'campaigns/fraud_report.html', {'form':form, 'campaign':campaign,})
