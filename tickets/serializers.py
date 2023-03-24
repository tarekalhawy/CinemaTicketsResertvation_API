from rest_framework import serializers
from .models import Guest, Movie, Reservation


class MovieSeriailzer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class ReservationSeriailzer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class GuestSeriailzer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['pk','reservation', 'name', 'mobile']