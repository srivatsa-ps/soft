from django.shortcuts import render
from django.http import HttpResponse
from .models import eventhall
from .forms import eventform


def index(request):
    if request.method == "POST":
        form = eventform(request.POST)

        if form.is_valid():
            #fields = ['firstname', 'apartment', 'purp','edate','stime']
            firstname = form.cleaned_data["firstname"]
            apartment = form.cleaned_data["apartment"]
            purp = form.cleaned_data["purpose"]
            edate = form.cleaned_data["edate"]
            stime = form.cleaned_data["stime"]


            event = eventhall.objects.create(firstname=firstname, purp=purp, apartment=apartment,edate=edate,stime=stime)
            event.save()
            return render(request, 'event/index.html', { 
                "message": "request added successfully" ,
                "form": eventform()
                })
    return render(request, 'event/index.html', {"form":eventform()} )

# Create your views here.
