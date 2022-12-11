from django import forms
from django.forms import ModelForm
from .models import Announcement, apartments

class AnnouncementForm(ModelForm):

    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    apartment = forms.ModelChoiceField(queryset=apartments.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Announcement
        fields = ['title', 'description', 'apartment']