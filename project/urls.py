"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tickets.models import Guest, Reservation, Movie
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register('guests', views.viewsets_guest)
router.register('movies', views.viewsets_movie)
router.register('reservations', views.viewsets_reservation)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #1
    path('django/jsonresponsemodel/', views.no_rest_no_model),
    
    #2
    path('django/jsonresponsefrommodel/', views.no_rest_from_model),
    
    #3
    #3.1  GET and POST from rest framwork  function Basid View  (@api_view)
    path('rest/fbv/', views.FBV_list),
    #3.2  GET and PUT and DELETE from rest framwork  function Basid View  (@api_view)
    path('rest/fbv/<int:pk>', views.FBV_pk),

    #4
    #4.1  GET and POST from rest framwork  Class Basid View  (APIView)
    path('rest/cbv/', views.CBV_list.as_view()),
    #4.2  GET and PUT and DELETE from rest framwork  Class Basid View  (APIView)
    path('rest/cbv/<int:pk>', views.CBV_pk.as_view()),


    #5
    #5.1  GET and POST from rest framwork  Class Basid View  (mixinis)
    path('rest/mixinis/', views.mixinis_list.as_view()),
    #5.2  GET and PUT and DELETE from rest framwork  Class Basid View  (mixinis)
    path('rest/mixinis/<int:pk>', views.mixinis_pk.as_view()),


    #6
    #6.1  GET and POST from rest framwork  Class Basid View  (generics)
    path('rest/generics/', views.generics_list.as_view()),
    #5.2  GET and PUT and DELETE from rest framwork  Class Basid View  (generics)
    path('rest/generics/<int:pk>', views.generics_pk.as_view()),
    
    
    #7
    #  GET and POST and PUT and DELETE from rest framwork  Class Basid View  (viewsets)
    path('rest/viewsets/', include(router.urls)),
    
    #8 find movie
    path('fbv/findmovie/', views.find_movie), 
    
    #9 new reservation
    path('fbv/newreservation/', views.new_reservation),
    
    #9 rest auth url
    path('api_auth/', include('rest_framework.urls')),
    
    #10 token authentication
    path('api_token_auth', obtain_auth_token),
]
 