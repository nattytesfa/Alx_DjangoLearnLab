from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image


class CustomUser(AbstractUser):
    """Custom User Model with additional fields for social media."""
    
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    profile_picture = models.ImageField(
        _('profile picture'),
        upload_to='profile_pics/',
        default='profile_pics/default.jpg'
    )
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )
    website = models.URLField(_('website'), blank=True)
    location = models.CharField(_('location'), max_length=100, blank=True)
    
    # Override default fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        """Override save to resize profile picture."""
        super().save(*args, **kwargs)
        
        if self.profile_picture:
            img = Image.open(self.profile_picture.path)
            
            # Resize image if larger than 300x300
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)
    
    @property
    def follower_count(self):
        """Return number of followers."""
        return self.followers.count()
    
    @property
    def following_count(self):
        """Return number of users being followed."""
        return self.following.count()
