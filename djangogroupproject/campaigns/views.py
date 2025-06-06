from django.shortcuts import render, redirect, get_object_or_404
from .forms import CampaignForm, CampaignPageBlockForm, CampaignDocumentForm, FraudReportForm
from .models import Campaign, CampaignPageBlock, CampaignDocument, FraudReport, Like
# maybe because of access by related name?
# Create your views here.
def campaign_list(request):
    campaigns = Campaign.objects.filter(status='active')
    return render(request, 'campaigns/list.html', {'campaigns': campaigns})

def campaign_detail(request, slug):
    campaign = get_object_or_404(Campaign, slug = slug)
    blocks = campaign.blocks.all()
    documents = campaign.documents.all()
    likes = campaign.like_set.count()
    return render (request, 'campaigns/detail.html', {
        'campaign':campaign, 'blocks':blocks, 'documents':documents, 'likes':likes})

def campaign_create(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('campaign_list') # NEED TO CHANGE THIS
    else:
        form = CampaignForm()
    return render(request, 'campaign/create.html', {'form':form})

def campaign_block_add(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.method == 'POST':
        form = CampaignPageBlockForm(request.POST, request.FILES)
        if form.is_valid():
            block = form.save(commit=False)
            block.campaign = campaign
            block.save()
            return redirect('campaign_detail', slug=campaign.slug) # RECHECK
    else:
        form = CampaignPageBlockForm
    return render(request, 'campaigns/block_add.html', {'form':form})

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
