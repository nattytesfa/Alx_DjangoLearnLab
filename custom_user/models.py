from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(_('Date of Birth'), null=True, blank=True)
    profile_photo = models.ImageField(
        _('Profile Photo'), 
        upload_to='profile_photos/',
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return self.username
