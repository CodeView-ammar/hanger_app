from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Users(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('laundry_owner', 'Laundry Owner'),
        ('carriers', 'Carriers'),
    ]
    
    # username = models.CharField(max_length=50, unique=True)
    # password = models.CharField(max_length=255)
    # email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_laundry_owner = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change this to something unique
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Change this to something unique
        blank=True,
    )

    def __str__(self):
        return self.name
    
class Address(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    address_line = models.CharField(max_length=255)
    x_map = models.CharField(max_length=100)
    y_map = models.CharField(max_length=100)
    city = models.CharField(max_length=100,blank=True,null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100,blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Address for {self.user.username}'