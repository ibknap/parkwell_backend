from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models

# mobile number regex
mobile_num_regex = RegexValidator(regex="^\+?1?\d{9,15}$", message="Invalid mobile number!")

class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification = models.BooleanField(_("verification"), default=False)
    is_company_admin = models.BooleanField(_("Company admin"), default=False)
    is_park_admin = models.BooleanField(_("Park admin"), default=False)
    photo = models.ImageField(_("Administrator's photo(optional)"), upload_to='administrator_photos/', default="../static/images/avatar.png", blank=True, null=True)
    mobile_number = models.CharField(_("Administrator's mobile number"), validators=[mobile_num_regex], max_length=20)
    # timestamp
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Administrator")
        verbose_name_plural = _("Administrators")

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("Administrator_detail", kwargs={"pk": self.pk})