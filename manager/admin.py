from django.contrib import admin
from .models import User, apartments, Utilities, Bookings, Announcement, Tenantrequest 
# Register your models here.

admin.site.register(User)
admin.site.register(apartments)
admin.site.register(Utilities)
admin.site.register(Bookings)
admin.site.register(Announcement)
admin.site.register(Tenantrequest)