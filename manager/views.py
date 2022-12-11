from sqlite3 import IntegrityError
from django.shortcuts import render
from .models import User, apartments, Utilities, Bookings, Announcement, Tenantrequest
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
import datetime
from .forms import AnnouncementForm


# Create your views here.

def index(request):

    all_apartments = apartments.objects.all()
    return render(request, "manager/index.html", { 'apartments' : all_apartments })


def register(request):
    if request.method == "POST":
        name = request.POST["username"]
        ph = request.POST["phno"]
        password = request.POST["password"]
        password2 = request.POST["cpassword"]

        if password == password2:
            user = User.objects.create_user(name,password=password,phnumber=ph,user_type="ten")
            user.save()
            user = authenticate(request, username=name, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, 'manager/register.html', {'message': 'Passwords do not match'})


    return render(request, 'manager/register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'manager/login.html', {'message': 'Invalid Credentials'})

    return render(request, 'manager/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required(login_url='login')
def utilities(request):
    if request.user.user_type == 'ten':
        utilities = Utilities.objects.all()
        return render(request, "manager/utilities.html", { 'utilities' : utilities })
    elif request.user.user_type == 'emp':
        bookings = Bookings.objects.all()
        return render(request, 'manager/utilities.html', {"bookings": bookings})

@login_required(login_url='login')
def requestutil(request, util_code):
    """Create an instance of bookings with the utility code and the user"""
    user = request.user
    if user.user_type != "ten":
        return HttpResponseRedirect(reverse("utilities"))
    util = Utilities.objects.get(pk=util_code)
    utilities = Utilities.objects.all()
    try:
        booking = Bookings.objects.create(req_user=user, util=util)
        booking.save()
        return render(request, "manager/utilities.html", {
            'message': "Request Sent, Please wait till somebody accepts your request", 
            'utilities' : utilities
            })
    except Exception:
        return render(request, "manager/utilities.html", {
            "error": "You have already requested this utility", 
            'utilities' : utilities
            })
    
    
@login_required(login_url='login')
def jobs(request):
    """Return all the bookings for the current user as a JSON response"""
    user = request.user
    bookings = Bookings.objects.filter(req_user=user)
    
    data = []

    for booking in bookings:
        if booking.assigned:
            data.append({
                "util": booking.util.name,
                "assigned": booking.assigned.username,
                "date": booking.date,
                "time": booking.time,
                
            })

        else:
            data.append({
                "util": booking.util.name,
                "assigned": "Not Assigned",
                "date": booking.date or "Not Assigned",
                "time": booking.time or "Not Assigned",
                
            })
    return JsonResponse({"data": data})

@login_required(login_url='login')
def announcements(request):
    """Return all the announcements"""
    if request.user.user_type != "adm":
        announcements = Announcement.objects.filter(apartment = request.user.apartment)
    else:
        announcements = Announcement.objects.all()
    return render(request, "manager/announcements.html", {
        "announcements": announcements
        })

@login_required(login_url='login')
def viewapartment(request, code):
    requests = Tenantrequest.objects.filter(user=request.user)
    apartment = apartments.objects.get(id=code)
    if request.user.apartment == None and len(requests) == 0:
        user_status = "available"

    elif request.user.apartment == apartment:
        user_status = "tenant"
    else:
        user_status = "other"
    return render(request, 'manager/viewapartment.html', { 
        "apartment" : apartment, 
        "status": user_status })

@login_required(login_url='login')
def maketenant(request, code):
    """Make the user a tenant of the apartment"""
    apartment = apartments.objects.get(id=code)
    user = request.user
    
    message = "Your apllication is being processed"
    ten_request = Tenantrequest.objects.create(user=user, apartment=apartment)
    ten_request.save()
    

    return render(request, 'manager/viewapartment.html', { 
        "apartment" : apartment,
        "message": message,
    })

@login_required(login_url='login')
def addapartment(request):
    """Add an apartment to the database"""
    if request.method == "POST":
        name = request.POST["name"]
        contact = request.POST["contact"]
        desc = request.POST["description"]
        bhk = request.POST["bhk"]
        address = request.POST["address"]
        image = request.FILES["image"]

        try:
            apartment = apartments.objects.create(name=name, contact=contact, apartment_desc=desc, bhk=bhk, location=address, image=image)
            apartment.save()
            return render(request, 'manager/addapartment.html', { 
                "message": "Apartment added successfully" 
                })
        except IntegrityError:
            return render(request, 'manager/addapartment.html', { 
                "message": "Apartment already exists" 
                })

    return render(request, 'manager/addapartment.html')


@login_required(login_url='login')
def addannouncement(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            apartment = form.cleaned_data["apartment"]

            announcement = Announcement.objects.create(title=title, description=description, apartment=apartment)
            announcement.save()
            return render(request, 'manager/addannouncement.html', { 
                "message": "Announcement added successfully" ,
                "form": AnnouncementForm()
                })
    return render(request, 'manager/addannouncement.html', {"form":AnnouncementForm()} )



@login_required(login_url='login')
def close(request, code):
    job = Bookings.objects.get(id=code)
    job.delete()
    bookings = Bookings.objects.all()
    return render(request, 'manager/utilities.html', { 
                "message": "Job closed", 
                "bookings": bookings
                })

@login_required(login_url='login')
def assign(request, code):
    user = request.user
    bookings = Bookings.objects.all()
    job = Bookings.objects.get(id=code)
    job.assigned = user
    tomorrow = datetime.datetime.now() + datetime.timedelta(1)
    job.date = tomorrow.strftime("%Y-%m-%d")
    job.time = datetime.datetime.now().strftime("%H:%M:%S")
    job.save()

    return render(request, 'manager/utilities.html', { 
                "message": "Successfully assigned to yourself. Close the job once done.",
                "bookings": bookings
                })

@login_required(login_url='login')
def mod(request):
    """List all the users in the database"""
    users = User.objects.all()
    return render(request, 'manager/mod.html', { 
                "users": users
                })

@login_required(login_url='login')
def addemployee(request, code):
    """Add an employee to the database"""
    user = User.objects.get(id=code)
    user.user_type = "emp"
    user.save()
    return HttpResponseRedirect(reverse("mod"))


@login_required(login_url='login')
def viewapplications(request):
    """View all the applications for the apartment"""

    applications = Tenantrequest.objects.all()
    return render(request, 'manager/viewapplications.html', { 
                "applications": applications
                })

@login_required(login_url='login')
def approve(request, code, usercode):
    if request.user.user_type != "adm":
        return HttpResponseRedirect(reverse("index"))

    user_ = User.objects.get(id=usercode)   
    user_.apartment = Tenantrequest.objects.get(id=code).apartment
    user_.approved = True
    user_.save()

    Tenantrequest.objects.get(id=code).delete()
    

    return HttpResponseRedirect(reverse("viewapplications"))