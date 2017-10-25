from django.db import models


class Country(models.Model):
    country_name = models.CharField(max_length=255)
    continent_name = models.CharField(max_length=255)
    capital = models.CharField(max_length=255)
    languages = models.CharField(max_length=255)
    continent = models.CharField(max_length=4)
    geoname_id = models.IntegerField()
    north = models.FloatField()
    south = models.FloatField()
    east = models.FloatField()
    west = models.FloatField()
    iso_alpha_3 = models.CharField(max_length=3)
    fips_code = models.CharField(max_length=3)
    population = models.CharField(max_length=255)
    iso_numeric = models.CharField(max_length=255)
    area_in_sq_km = models.CharField(max_length=255)
    country_code = models.CharField(max_length=2)
    currency_code = models.CharField(max_length=4)

    class Meta:
        ordering = ['country_name']
