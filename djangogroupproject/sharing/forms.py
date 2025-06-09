from django import forms
from .models import Share, Bookmark

class ShareForm(forms.ModelForm):
    class Meta:
        model = Share
        fields = ('campaign', 'platform')

class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ('campaign',)