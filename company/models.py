from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from account.models import Administrator
from django.urls import reverse
from django.db import models

# mobile number regex
mobile_num_regex = RegexValidator(regex="^\+?1?\d{9,15}$", message="Invalid mobile number!")

class Company(models.Model):
    administrator = models.OneToOneField(Administrator, on_delete=models.CASCADE)
    verification = models.BooleanField(_("verification"), default=False)
    company_logo = models.ImageField(_("Company's logo"), upload_to='company_logos/')
    company_name = models.CharField(_("Company's name"), max_length=255)
    company_email = models.EmailField(_("Company's email"), max_length=255)
    company_number = models.CharField(_("Company's mobile number"), validators=[mobile_num_regex], max_length=20)
    company_about = models.TextField(_("About Company"), max_length=500)
    # timestamp
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return str(self.company_name)

    def get_absolute_url(self):
        return reverse("Company_detail", kwargs={"pk": self.pk})