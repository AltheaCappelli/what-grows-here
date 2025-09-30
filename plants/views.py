from django.shortcuts import render
import json
# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import Plants
from .models import ClimateData
from .models import cities
import numpy as np

#first define plant city class (like dictionary basically, with attributes)
class city_plants:
    
    def __init__(self, name, latitude, longitude, zone, average_month):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.zone = zone
        self.average_month = average_month
        veg_dict = {"vegetable": [], "fruit": [], "herb": [], "flower": []}
        self.plants = {"jun": veg_dict.copy(), 
                        "jul" : veg_dict.copy(),
                        "aug" : veg_dict.copy()} #dict of plants by category

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude}) - Zone: {self.zone}, Avg monthly Sun: {self.average_month}h, Plants: {self.plants}"

#add dictionary for the json response
    def to_dict(self):

        return {
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "zone": self.zone,
            "average_month": self.average_month,
            "plants": self.plants,
        }

def map(request):

    with open("precomputed_cities.json", "r") as f:
        precomputed_info = json.load(f) #load precomputed plants
    context = { 
        'cities': precomputed_info,
    }

    return render(request, 'map.html', context)

def theory(request):

    template = loader.get_template('theory.html')
    context = {
        'plants': Plants.objects.all(),
    }

    return HttpResponse(template.render(context, request))

def about(request):

    template = loader.get_template('about.html')

    return render(request, 'about.html')