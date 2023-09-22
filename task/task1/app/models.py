from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
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
    GOLD = 'GOLD'
    BRONZE = 'BRONZE'
    SILVER = 'SILVER'
    GROUP_CHOICES = [
        (GOLD, 'GOLD'),
        (BRONZE, 'BRONZE'),
        (SILVER, 'SILVER'),
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    count = models.IntegerField(editable=False,default=0)
    ip_address = models.CharField(editable=False,max_length=50)
    updated_time = models.DateTimeField(default=timezone.now)
    def set_ip(request):
        client_ip = request.META.get('REMOTE_ADDR')
        ip_object = CustomUser(ip_address=client_ip)
        ip_object.save()
    group_type = models.CharField(
        max_length=10,
        choices=GROUP_CHOICES,
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