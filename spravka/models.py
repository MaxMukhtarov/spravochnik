from django.db import models
from django.conf import settings

class Section(models.Model):
    section_name = models.CharField(max_length=128)

    def __str__(self):
        return self.section_name

class User(models.Model):
    full_name = models.CharField(max_length=300)
    mail_address = models.EmailField(blank=True, null=True)
    contact = models.CharField(max_length=4, blank=True, null=True)
    role = models.CharField(max_length=128)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='members')
    image = models.ImageField(upload_to='user_images/', blank=True, null=True, default='img/users/default.png')  # Default image

    def __str__(self):
        return self.full_name
