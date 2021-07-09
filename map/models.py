from django.utils.translation import gettext as _
from django.db import models

class Map(models.Model):
    # address = map_fields.AddressField(max_length=200)
    # geolocation = map_fields.GeoLocationField(max_length=100)

    class Meta:
        verbose_name = _("Map")
        verbose_name_plural = _("Maps")

    def __str__(self):
        return str(self.address)
