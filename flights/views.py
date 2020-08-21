from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Flight, Passengers


def home(request):
    return render(request, "flights/home.html", context = {"flights": Flight.objects.all(), "user": request.user})   

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
          login(request, user)
          return HttpResponseRedirect(reverse("home"))
    else:
          return render(request, "flights/login.html", {"message": "Invalid credentials."})

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)

    except Flight.DoesNotExist:
        raise Http404("Flight does not exist")
    
    context = {
      #sending only the flight at "Flight.objects.get(id=flight_id)" 
      "flight": flight,
      #sending only the passengers of the flight "Flight.objects.get(id=flight_id)" 
      "passengers": flight.passengers.all(),
      #all passengers on the current flight are excluded. 
      "non_passengers": Passengers.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)
        
def book(request, flight_id):
    try:
        passenger_id =  int(request.POST["passenger"])
        flight = Flight.objects.get(id=flight_id)
        passenger =  Passengers.objects.get(id=passenger_id)

    except KeyError:
        render(request, "flights/errors.html", {"message": "No selection."})
    except Flight.DoseNotExist:
        render(request, "flights/errors.html", {"message": "No Flight."})
    except Passengers.DoseNotExist:
        render(request, "flights/errors.html", {"message": "No Passenger."})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))

def logout_view(request):
      logout(request)
      return render(request, "flights/login.html", {"message": "Logged out."})