from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from .managers import UserManager  # Assuming you have a custom UserManager


class User(AbstractUser):
    username = None

    # User roles
    CUSTOMER = 'CUSTOMER'
    WAREHOUSE_MANAGER = 'WAREHOUSE_MANAGER'
    SALES_MANAGER = 'SALES_MANAGER'
    ADMIN = 'ADMIN'
    DELIVERY_TEAM = 'DELIVERY TEAM'

    USER_TYPE_CHOICES = (
        (CUSTOMER, 'Customer'),
        (WAREHOUSE_MANAGER, 'Warehouse Manager'),
        (SALES_MANAGER, 'Sales Manager'),
        (ADMIN, 'Admin'),
        (DELIVERY_TEAM, 'Delivery Team'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=CUSTOMER)
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )

    # Social media handles
    instagram_handle = models.CharField(max_length=50, blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)

    # Email as the primary login identifier
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={"unique": "A user with that email already exists."}
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    # Custom manager
    objects = UserManager()

    # Password validation and setting
    def set_password(self, raw_password):
        validate_password(raw_password)
        self.password = make_password(raw_password)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_user_type_display()})"

    def is_customer(self):
        return self.user_type == self.CUSTOMER

    def is_warehouse_manager(self):
        return self.user_type == self.WAREHOUSE_MANAGER

    def is_sales_manager(self):
        return self.user_type == self.SALES_MANAGER

    def is_admin(self):
        return self.user_type == self.ADMIN

    def is_delivery_team(self):
        return self.user_type == self.DELIVERY_TEAM

