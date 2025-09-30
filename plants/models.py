from django.db import models

# Create your models here.
USDA_CHOICES = [(i, str(i)) for i in range(1, 13)]


class Plants(models.Model):

    name = models.CharField(max_length=50)
    wind = models.CharField(max_length=20, blank=True, null=True,) #can be empty
    water_need = models.CharField(max_length = 20, blank=True, null=True,) #can be empty
    usda_min = models.IntegerField(blank=True, null=True,) #can be empty
    usda_max = models.IntegerField(blank=True, null=True,) #can be empty
    height = models.FloatField(blank=True, null=True) #can be empty
    width = models.FloatField(blank=True, null=True) #can be empty
    shade = models.CharField(max_length = 20, blank=True, null=True,) #can be empty
    sunlight_max = models.IntegerField(blank=True, null=True) #can be empty
    sunlight_min = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True,) #can be empty
    #watering_frequency = models.CharField(max_length=50, blank=True, null=True)
    #image_url = models.URLField(blank=True, null=True)
    #description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name


class ClimateData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    usda_zone = models.IntegerField(null=True, blank=True,)
    average_sunshine_hours_jan = models.FloatField(null=True, blank=True)
    average_sunshine_hours_feb = models.FloatField(null=True, blank=True)
    average_sunshine_hours_mar = models.FloatField(null=True, blank=True)
    average_sunshine_hours_apr = models.FloatField(null=True, blank=True)
    average_sunshine_hours_may = models.FloatField(null=True, blank=True)
    average_sunshine_hours_jun = models.FloatField(null=True, blank=True)
    average_sunshine_hours_jul = models.FloatField(null=True, blank=True)
    average_sunshine_hours_aug = models.FloatField(null=True, blank=True)
    average_sunshine_hours_sep = models.FloatField(null=True, blank=True)
    average_sunshine_hours_oct = models.FloatField(null=True, blank=True)
    average_sunshine_hours_nov = models.FloatField(null=True, blank=True)
    average_sunshine_hours_dec = models.FloatField(null=True, blank=True)
    #average_cloud_cover = models.FloatField(null=True, blank=True)
#    average_wind_jan = models.FloatField(null=True, blank=True)
#    average_wind_feb = models.FloatField(null=True, blank=True)
#    average_wind_mar = models.FloatField(null=True, blank=True)
#    average_wind_apr = models.FloatField(null=True, blank=True)
#    average_wind_may = models.FloatField(null=True, blank=True)
#    average_wind_jun = models.FloatField(null=True, blank=True)
#    average_wind_jul = models.FloatField(null=True, blank=True)
#    average_wind_aug = models.FloatField(null=True, blank=True)
#    average_wind_sep = models.FloatField(null=True, blank=True)
#    average_wind_oct = models.FloatField(null=True, blank=True)
#    average_wind_nov = models.FloatField(null=True, blank=True)
#    average_wind_dec = models.FloatField(null=True, blank=True)
#    average_rainfall_jan = models.FloatField(null=True, blank=True)
#    average_rainfall_feb = models.FloatField(null=True, blank=True)
#    average_rainfall_mar = models.FloatField(null=True, blank=True)
#    average_rainfall_apr = models.FloatField(null=True, blank=True)
#    average_rainfall_may = models.FloatField(null=True, blank=True)
#    average_rainfall_jun = models.FloatField(null=True, blank=True)
#    average_rainfall_jul = models.FloatField(null=True, blank=True)
#    average_rainfall_aug = models.FloatField(null=True, blank=True)
#    average_rainfall_sep = models.FloatField(null=True, blank=True)
#    average_rainfall_oct = models.FloatField(null=True, blank=True)
#    average_rainfall_nov = models.FloatField(null=True, blank=True)
#    average_rainfall_dec = models.FloatField(null=True, blank=True)
#    average_wind = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"

class Balcony(models.Model):
    BALCONY_CHOICES = [
        ('south', 'South facing'),
        ('north', 'North facing'),
        ('east', 'East facing'),
        ('west', 'West facing'),
    ]
    balcony_direction = models.CharField(max_length=10, choices=BALCONY_CHOICES, default='south')
    balcony_size = models.FloatField(help_text="Size in square meters")

    def __str__(self):
        return f"{self.balcony_direction} balcony ({self.balcony_size} m²)"
        
class cities(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name