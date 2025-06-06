from django import forms
from .models import Tag

'''
forms module provides tools to create and handle HTML forms in a Pythonic way (with built-in validation, 
error handling, etc.
Defines a form class named TagForm, which inherits from forms.ModelForm
ModelForm automatically builds form fields based on a Django model (Tag in this case).
This means you don't need to manually declare each field — Django does it for you based on the model.
The Meta class provides metadata to the ModelForm
model = Tag: Tells the form to use the Tag model
Fields = (...): Specifies which fields from the model should be included in the form (name, category, and slug), which
means that the model will build from the included field only
Forms provide: Validation (e.g., checking if the slug is unique),Data cleaning (e.g., trimming whitespace or 
formatting fields), Easy saving to the database via .save()
Using a form (instead of writing manual model logic) avoids code duplication and errors.
'''

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', 'category', 'slug')
