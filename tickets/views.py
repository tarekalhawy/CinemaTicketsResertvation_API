from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Reservation, Movie
from rest_framework.decorators import api_view
from .serializers import GuestSeriailzer, ReservationSeriailzer, MovieSeriailzer
from rest_framework.response import Response
from rest_framework import response, status, filters
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

#1 without rest and no model query   FBV
def no_rest_no_model(request):
    guests = [
        {
            'id' : 1,
            'Name' :'Omar', 
            'mobile' : 455555554
        },
        {
            'id' : 2,
            'Name' :'Nader', 
            'mobile' : 455632874
        }
    ]
    return JsonResponse(guests, safe=False)


#2 model data default django without rest
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guests' : list(data.values('name', 'mobile'))
    }
    return JsonResponse(response) 


#3 function basid views
#3.1 GET , POST
@api_view(['GET', 'POST'])
def FBV_list(request):
    #GET
    if request.method == 'GET' :
        guests = Guest.objects.all()
        serializer = GuestSeriailzer(guests, many=True)    
        return Response(serializer.data)  
    # POST
    elif request.method == 'POST':
        serializer = GuestSeriailzer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED )
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)   

#3.2 GET , PUT, DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):
    try:
        guests = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    # GET
    if request.method == 'GET' :
        serializer = GuestSeriailzer(guests)    
        return Response(serializer.data)  
    # PUT
    elif request.method == 'PUT':
        serializer = GuestSeriailzer(guests, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
    # DELETE
    elif request.method == 'DELETE':
       guests.delete()
       return Response(status=status.HTTP_204_NO_CONTENT)
   
#4 CBV Class Basid View   
#4.1 list and create == POST and GET
class CBV_list(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        query = GuestSeriailzer(guests, many=True)    
        return Response(query.data) 
    
    def post(self, request):
        serializer = GuestSeriailzer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    
#4.2  GET and PUT and DELETE Class Basid View   
class CBV_pk(APIView):
    def get_objecet(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
                    
    def get(self, request, pk):
        guests = self.get_objecet(pk)
        serializer = GuestSeriailzer(guests)    
        return Response(serializer.data) 
        
    
    def put(self, request, pk):
        guests = self.get_objecet(pk)
        serializer = GuestSeriailzer(guests, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
    def delete(self, request, pk):
        guests = self.get_objecet(pk)
        guests.delete()
        return Response(status=status.HTTP_204_NO_CONTENT )    


#5 Mixinis
#5.1 mixinis list    
class mixinis_list(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSeriailzer
    
    def get(self , request):
        return self.list(request)
    
    def post(self , request):
        return self.create(request)
    
    
#5.2 mixinis get put delete 
class mixinis_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSeriailzer
    
    def get(self , request, pk):
        return self.retrieve(request)
    
    def put(self , request, pk):
        return self.update(request)
    
    def delete(self , request, pk):
        return self.destroy(request)
    
#6 generics  
#6.1 list get and post
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSeriailzer
    authentication_classes = [TokenAuthentication]
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


#6.2 get and put and delete
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSeriailzer
    

#7 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSeriailzer
        
    
class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSeriailzer
    filter_backends = [filters.SearchFilter]
    search_filed = ['movie']
    
    
class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSeriailzer
       
        
#8 find movie    
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie']
    )    
    serializer = MovieSeriailzer(movies, many=True)
    return Response(serializer.data)
    

#9 new reservation
@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        hall = request.data['hall']
,        movie = request.data['movie']
    )    
    
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()
    
    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    
    return Response(status=status.HTTP_201_CREATED)
    
    
    