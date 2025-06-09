from django.shortcuts import render, redirect
from .forms import ShareForm, BookmarkForm

def share_campaign(request):
    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            share = form.save(commit=False)
            share.user = request.user
            share.save()
            # Redirect to campaign detail with a success message
    else:
        form = ShareForm()
    return render(request, 'sharing/share.html', {'form': form})

def bookmark_campaign(request):
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.save()
            # Redirect as needed
    else:
        form = BookmarkForm()
    return render(request, 'sharing/bookmark.html', {'form': form})