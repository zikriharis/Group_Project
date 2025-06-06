from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import TagForm
from .models import Tag

# Create your views here.
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tags/list.html', {'tags': tags})

# For admin
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'tags/create.html', {'form': form})