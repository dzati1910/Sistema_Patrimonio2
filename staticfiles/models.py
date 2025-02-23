from django.contrib.auth.models import AbstractUser
from django.db import models
from assets.models import Department

# models do app core

class User(AbstractUser):
    tax_id = models.CharField(max_length=11, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username

    def is_department_responsible(self):
        """Check if user is responsible for any department"""
        return Department.objects.filter(responsible_person=self).exists()