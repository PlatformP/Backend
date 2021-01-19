from django.db import models

from Backend.settings import US_GEO_CONFIG
from Scripts.HelperMethods import get_key_from_state

class ZipCode(models.Model):
    zipcode = models.IntegerField()

    country_code = models.CharField(max_length=50, editable=False, blank=True, null=True)
    place_name = models.CharField(max_length=50, editable=False, blank=True, null=True)
    state_name = models.CharField(max_length=50, editable=False, blank=True, null=True)
    state_code = models.CharField(max_length=50, editable=False, blank=True, null=True)
    state_key = models.IntegerField(editable=False, blank=True, null=True)
    county_name = models.CharField(max_length=50, editable=False, blank=True, null=True)
    county_code = models.IntegerField(editable=False, blank=True, null=True)

    def __str__(self):
        return str(self.zipcode)

    def save(self, *args, **kwargs):
        df = US_GEO_CONFIG.query_postal_code(self.zipcode)
        self.country_code = df.country_code
        self.place_name = df.place_name
        self.state_name = df.state_name
        self.state_code = df.state_code
        self.state_key = get_key_from_state(self.state_code)
        self.county_name = df.county_name
        self.county_code = df.county_code

        super(ZipCode, self).save(*args, **kwargs)