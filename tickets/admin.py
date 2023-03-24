from django.contrib import admin
from .models import Guest, Reservation, Movie

# Register your models here.

class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile')
    

admin.site.register(Guest, GuestAdmin)
admin.site.register(Movie)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('guest', 'movie')
    
admin.site.register(Reservation, ReservationAdmin)