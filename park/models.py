from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from company.models import Company
from django.urls import reverse
from django.db import models

# mobile number regex
mobile_num_regex = RegexValidator(regex="^\+?1?\d{9,15}$", message="Invalid mobile number!")

TIME = [
        ('1am', '1am'),
        ('2am', '2am'),
        ('3am', '3am'),
        ('4am', '4am'),
        ('5am', '5am'),
        ('6am', '6am'),
        ('7am', '7am'),
        ('8am', '8am'),
        ('9am', '9am'),
        ('10am', '10am'),
        ('11am', '11am'),
        ('12am', '12am'),
        ('1pm', '1pm'),
        ('2pm', '2pm'),
        ('3pm', '3pm'),
        ('4pm', '4pm'),
        ('5pm', '5pm'),
        ('6pm', '6pm'),
        ('7pm', '7pm'),
        ('8pm', '8pm'),
        ('9pm', '9pm'),
        ('10pm', '10pm'),
        ('11pm', '11pm'),
        ('12pm', '12pm'),
    ]

class Park(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    park_name = models.CharField(_("Park's name"), max_length=255)
    park_email = models.EmailField(_("Park's email"), max_length=255)
    total_parking_space = models.PositiveIntegerField(_("Total parking space"))
    park_number = models.CharField(_("Park's mobile number"), validators=[mobile_num_regex], max_length=20)
    park_address = models.CharField(_("Park's address"), max_length=255)
    park_lon = models.CharField(_("Park's longitude"), max_length=255)
    park_lat = models.CharField(_("Park's latitude"), max_length=255)
    # park_opening_time = models.CharField(_("Park's closing time"),choices=TIME, max_length=255)
    # park_closing_time = models.CharField(_("Park's closing time"),choices=TIME, max_length=255)
    park_about = models.TextField(_("About Park"), max_length=500)
    # timestamp
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Park")
        verbose_name_plural = _("Parks")

    def __str__(self):
        return str(self.park_name)

    def get_absolute_url(self):
        return reverse("Park_detail", kwargs={"pk": self.pk})

class ParkImage(models.Model):
    park = models.ForeignKey(Park, on_delete=models.CASCADE)
    park_images = models.FileField(_("Park's images(optional)"), upload_to='park_images/')

    class Meta:
        verbose_name = _("ParkImage")
        verbose_name_plural = _("ParkImages")

    def __str__(self):
        return f'{self.park}'

    def get_absolute_url(self):
        return reverse("ParkImage_detail", kwargs={"pk": self.pk})

class ParkOtherService(models.Model):
    park = models.ForeignKey(Park, on_delete=models.CASCADE)
    park_service = models.CharField(_("Park's other service(Optional)"), max_length=255)

    class Meta:
        verbose_name = _("ParkOtherService")
        verbose_name_plural = _("ParkOtherServices")

    def __str__(self):
        return f'{self.park}'

    def get_absolute_url(self):
        return reverse("ParkOtherService_detail", kwargs={"pk": self.pk})
