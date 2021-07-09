from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django.db import models

# mobile number regex
mobile_num_regex = RegexValidator(regex="^\+?1?\d{9,15}$", message="Invalid mobile number!")

class CompanyAdminProfile(models.Model):
    admin = models.OneToOneField(User, related_name="companyadminprofile", verbose_name=_("Company admin"), on_delete=models.CASCADE)
    company_admin_photo = models.ImageField(_("Company's admin photo(optional)"), upload_to='company_admin_photos/', blank=True, null=True)
    company_admin_number = models.CharField(_("Company's admin mobile number"), validators=[mobile_num_regex], max_length=20)
    # timestamp
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("CompanyAdminProfile")
        verbose_name_plural = _("CompanyAdminProfiles")

    def __str__(self):
        return f'{self.admin}'

    def get_absolute_url(self):
        return reverse("CompanyAdminProfile_detail", kwargs={"pk": self.pk})


class ParkAdminProfile(models.Model):
    admin = models.OneToOneField(User, related_name="parkadminprofile", verbose_name=_("Park admin"), on_delete=models.CASCADE)
    company_admin = models.ForeignKey(CompanyAdminProfile, related_name="parkadminprofilecompanyadmin", verbose_name=_("Park admin's company admin"), on_delete=models.CASCADE)
    park_admin_photo = models.ImageField(_("park's admin photo(optional)"), upload_to='park_admin_photos/', blank=True, null=True)
    park_admin_number = models.CharField(_("park's admin mobile number"), validators=[mobile_num_regex], max_length=20)
    # timestamp
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("ParkAdminProfile")
        verbose_name_plural = _("ParkAdminProfiles")

    def __str__(self):
        return f'{self.admin}'

    def get_absolute_url(self):
        return reverse("ParkAdminProfile_detail", kwargs={"pk": self.pk})

# token creation
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
