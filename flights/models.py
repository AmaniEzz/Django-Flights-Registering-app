from django.db import models

# Create your models here.
#on_delete=models.CASCADE means that if an airport is deleted,
#all flights with that airport as an origin or destination will be deleted as well.

class Airport(models.Model):
      code = models.CharField(max_length=3)
      city = models.CharField(max_length=64)

      def __str__(self):
          return f"{self.city} ({self.code})"
    
class Flight(models.Model):

    duration = models.IntegerField()
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")

    def __str__(self):
         return f"{self.id} - {self.origin} to {self.destination}"


class Passengers(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")
    
    def __str__(self):
          return f"{self.first} {self.last}"


