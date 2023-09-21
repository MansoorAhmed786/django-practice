from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.http import HttpRequest
# from ipware import get_client_ip
# from .views import print_mansoor
# import requests as req
# from .views import get_ip

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    GOLD = 'gold'
    BRONZE = 'bronze'
    SILVER = 'silver'

    GROUP_CHOICES = [
        (GOLD, 'Gold'),
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # ip_address = models.GenericIPAddressField(protocol='both', null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    # ip_address = models.GenericIPAddressField()
    count = models.IntegerField(editable=False,default=0)


    
    group_type = models.CharField(
        max_length=10,
        choices=GROUP_CHOICES,
        default=GOLD,  # You can set a default value if needed
    )

    objects = CustomUserManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name