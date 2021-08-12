from company.models import Company
from django.db.models.fields import DateTimeField
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from park.models import Park
from django.db import models

# mobile number regex
mobile_num_regex = RegexValidator(regex="^\+?1?\d{9,15}$", message="Invalid mobile number!")

class Booking(models.Model):
    full_name = models.CharField(_("Full name"), max_length=255)
    email = models.EmailField(_("Email"), max_length=255)
    park = models.ForeignKey(Park, on_delete=models.CASCADE)
    mobile_number = models.CharField(_("Mobile number"), validators=[mobile_num_regex], max_length=20)
    arrival_time = DateTimeField(blank=False, null=False)
    departure_time = DateTimeField(blank=False, null=False)
    # timestamp
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")

    def __str__(self):
        return str(self.full_name)

class Waitlist(models.Model):
    email = models.EmailField(_("Email"), max_length=255)
    # timestamp
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Listing")
        verbose_name_plural = _("Listings")

    def __str__(self):
        return str(self.email)

class Navigate(models.Model):
    park = models.ForeignKey(Park, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # timestamp
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Navigate")
        verbose_name_plural = _("Navigates")

    def __str__(self):
        return str(self.park)