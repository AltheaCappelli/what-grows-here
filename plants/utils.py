import json
import copy
from .models import Plants, ClimateData, cities

class city_plants:
    def __init__(self, name, latitude, longitude, zone=None, average_month=None):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.zone = zone
        self.average_month = average_month
        veg_dict = {"vegetable": [], "fruit": [], "herb": [], "flower": []}
        self.plants = {
                       "mar": copy.deepcopy(veg_dict),
                       "apr": copy.deepcopy(veg_dict),
                       "may": copy.deepcopy(veg_dict),
                       "jun": copy.deepcopy(veg_dict), #safe way of copying without having problems
                       "jul": copy.deepcopy(veg_dict),
                       "aug": copy.deepcopy(veg_dict),
                       "sep": copy.deepcopy(veg_dict)
                       }

    def to_dict(self):
        return {
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "zone": self.zone,
            "average_month": self.average_month,
            "plants": self.plants,
        }

month_list = ['mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep']
#precompute plants to show on map for each city
def precompute_city_plants():
   
    plants_list = Plants.objects.all().values()
    climate_list = ClimateData.objects.all().values()
    cities_lst = cities.objects.all().values() #get all cities from database:
                                               #[{"id"}:1, "name":"Athens", "latitude":37.9838, "longitude":23.7275}, {...}, {...}]
    
    cities_dict = {city['name']: 
                city_plants(
                    city['name'], 
                    city['latitude'], 
                    city['longitude']
                    )
                for city in cities_lst}

#define function to find nearest coords from city
    def find_zone(city_obj):
        
        nearest_point = None
        min_distance = float('inf') #set initial distance to inf
        for point in climate_list:
            distance = ((point['latitude'] - city_obj.latitude) ** 2 +
                        (point['longitude'] - city_obj.longitude) ** 2) ** 0.5 #calculate distance
            if distance < min_distance:
                min_distance = distance #if distance is less than min_distance, set it to distance
                nearest_point = point #set nearest point to current point, do this until nearest point found
        
        return nearest_point

    def find_average_sunlight(city_obj, month):

        zone_info = find_zone(city_obj)
        
        return zone_info[f'average_sunshine_hours_{month}']

#fill in zone and average sunlight for each city
    for city_obj in cities_dict.values(): #go through each city object in cities_dict
        nearest = find_zone(city_obj)
        city_obj.zone = nearest['usda_zone']
        city_obj.average_month = {month: find_average_sunlight(city_obj, month) for month in month_list}

#function to find plants for each city
    def find_plants(city_obj):

        for plant in plants_list:
            min_sun = plant['sunlight_min']
            max_sun = plant['sunlight_max']
            category = [cat.strip() for cat in plant['category'].split(',')]
            exposure = [exp.strip().lower() for exp in plant["wind"].split(',')]
            
            if min_sun == "": #check if plants have min/max sunlight
               min_sun = 0
            elif max_sun == "" or max_sun >= 8: #if more than 8 hours, set to 24 to avoid exclusion
               max_sun = 24

            usda_min = plant["usda_min"]
            usda_max = plant["usda_max"]
            if not (usda_min <= city_obj.zone <= usda_max):
                continue #cut out plants which are not in the zone: faster, as less plants

            for month in month_list:
                avg = city_obj.average_month[month]
                if not (min_sun <= avg <= max_sun):
                    continue #cut out plants which do not fit sunlight criteria for the month
                directions = set() #avoid duplicates
                for exp in exposure:
                    if "full sun" in exp: directions.add("south")
                    if "partial sun" in exp: directions.update(["east", "west", "south"])
                    if "spring" in exp or "partial shade" in exp: directions.update(["east", "west", "north"]) #if contains "tolerates sun in spring and fall"
                    if "shade" in exp and "partial" not in exp: directions.add("north") #full shade or tolerates shade

                for cat in category:
                    for d in directions:
                        city_obj.plants[month][cat].append((plant['name'], d))
       
        return city_obj.plants

    precomputed_info = {} #dictionary to hold all precomputed info for each city
    #fill in with plants
    for city_obj in cities_dict.values():
        find_plants(city_obj)
        precomputed_info[city_obj.name] = city_obj.to_dict() #dictionary of city name to city object as dictionary

    #save JSON file
    with open("precomputed_cities.json", "w") as f:
        json.dump(precomputed_info, f, indent=2)
    
    print("Precompute done! JSON saved.")
