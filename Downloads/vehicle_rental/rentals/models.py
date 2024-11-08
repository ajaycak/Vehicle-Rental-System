from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User  # For extending the User model

# 1. Vehicle Type Model
class VehicleType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# 2. Vehicle Model
class Vehicle(models.Model):
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.vehicle_type.name} - {self.model}"

# 3. User Profile Model (extending the Django User model)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

# 4. Booking Model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    booking_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle.model}"

    def clean(self):
        # Optional: Ensures return date is after booking date
        if self.return_date < self.booking_date:
            raise ValidationError("Return date must be after booking date.")

# 5. Payment Model
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, default="Pending")
    payment_method = models.CharField(max_length=20, blank=True)  # E.g., Credit Card, Cash
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking.user.username} - {self.amount}"
