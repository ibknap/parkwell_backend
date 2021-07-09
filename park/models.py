from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from account.models import ParkAdminProfile
from company.models import Company
from django.urls import reverse
from django.db import models

# mobile number regex
mobile_num_regex = RegexValidator(regex="^\+?1?\d{9,15}$", message="Invalid mobile number!")

class Park(models.Model):
    company = models.ForeignKey(Company, related_name="park", verbose_name=_("Park's company"), on_delete=models.CASCADE)
    admin = models.OneToOneField(ParkAdminProfile, related_name="parkadmin", verbose_name=_("Park's admin"), on_delete=models.CASCADE)
    park_name = models.CharField(_("Park's name"), max_length=255)
    park_email = models.EmailField(_("Park's email"), max_length=255)
    total_parking_space = models.PositiveIntegerField(_("Total parking space"))
    occupied_space = models.PositiveIntegerField(_("Occupied space"))
    park_number = models.CharField(_("Park's mobile number"), validators=[mobile_num_regex], max_length=20)
    park_address = models.CharField(_("Park's address"), max_length=255)
    park_coordinates = models.CharField(_("Park's Coordinates"), max_length=255)
    park_about = models.TextField(_("About Park"), max_length=500)
    # timestamp
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Park")
        verbose_name_plural = _("Parks")

    def __str__(self):
        return f'{self.park_name}'

    def get_absolute_url(self):
        return reverse("Park_detail", kwargs={"pk": self.pk})

class ParkImage(models.Model):
    park = models.ForeignKey(Park, verbose_name=_("Park"), on_delete=models.CASCADE)
    park_images = models.FileField(_("Park's images(optional)"), upload_to='park_images/')

    class Meta:
        verbose_name = _("ParkImage")
        verbose_name_plural = _("ParkImages")

    def __str__(self):
        return f'{self.park}'

    def get_absolute_url(self):
        return reverse("ParkImage_detail", kwargs={"pk": self.pk})

class ParkOtherService(models.Model):
    park = models.ForeignKey(Park, verbose_name=_("Park"), on_delete=models.CASCADE)
    park_service = models.CharField(_("Park's other service(Optional)"), max_length=255)

    class Meta:
        verbose_name = _("ParkOtherService")
        verbose_name_plural = _("ParkOtherServices")

    def __str__(self):
        return f'{self.park}'

    def get_absolute_url(self):
        return reverse("ParkOtherService_detail", kwargs={"pk": self.pk})
