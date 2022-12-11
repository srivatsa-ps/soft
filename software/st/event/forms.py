from django import forms
from django.forms import ModelForm
from .models import eventhall

class eventform(ModelForm):
    firstname= forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
    apartment= forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))    
    purp= forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))   
    edate=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control'}))
    stime=forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control'}))
    class Meta:
        model = eventhall
        fields = ['firstname', 'apartment', 'purp','edate','stime']