from django.db import models
from decimal import Decimal
from django.utils import timezone

# Create your models here.
class Register(models.Model):
    username=models.CharField(max_length=30,null=True,blank=True)
    email=models.EmailField(unique=True,null=True,blank=True)
    phnumber=models.IntegerField(null=True,blank=True)
    password=models.CharField(max_length=100,null=True,blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.username)
    
    
class FoodCategory(models.Model):
    name = models.CharField(max_length=50)
    description=models.TextField(max_length=5000,null=True,blank=True)
    catimage=models.ImageField(upload_to='category_images/',null=True,blank=True)
    def __str__(self):
        return self.name
    
class FoodItem(models.Model):
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    fimage=models.ImageField(upload_to='food_images/',null=True,blank=True)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    product=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    qty=models.IntegerField()
    tprice=models.DecimalField(decimal_places=2,max_digits=10)

    def save(self, *args, **kwargs):
        self.tprice = self.qty * Decimal(self.product.price)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Order(models.Model): 
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    order_date = models.DateField(null=True,blank=True)
    venue = models.CharField(max_length=255)
    address = models.TextField(null=True,blank=True)
    eventdate = models.DateField(null=True,blank=True)
    place = models.CharField(max_length=255)
    preferred_time = models.TimeField(null=True, blank=True) 
    status = models.CharField(max_length=20, default='Pending') 

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    qty = models.IntegerField(null=True,blank=True)
    tprice = models.DecimalField(decimal_places=2, max_digits=10,null=True,blank=True)

    def __str__(self):
        return f"{self.qty} x {self.product.name} for Order {self.order.id}"


class Feedback(models.Model): 
    name=models.CharField(max_length=30,null=True,blank=True)
    RATING_CHOICES = [ 
        (1, '1'), 
        (2, '2'), 
        (3, '3'), 
        (4, '4'), 
        (5, '5'), 
    ] 
    
    feedback_text = models.TextField()  
    rating = models.IntegerField(choices=RATING_CHOICES)   
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    image = models.ImageField(upload_to='feedback_images/', null=True, blank=True)  
    image_description = models.TextField(null=True, blank=True)  

    def __str__(self): 
        return f"Rating: {self.rating}, feedback: {self.feedback_text[:50]}..."
    

class Contactus(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    subject=models.CharField(max_length=100,null=True,blank=True)
    message = models.TextField(max_length=2000,null=True,blank=True)


class RoomCategory(models.Model):
    name = models.CharField(max_length=100)
    categoryDescription = models.CharField(max_length=2000 , null=True , blank=True)
    image = models.ImageField(upload_to='room_category_images/', null=True, blank=True)  # New image field

    def __str__(self):
        return self.name

class Room(models.Model):
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    roomnum = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='room_images/')
    description = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.roomnum)


class RoomBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey('Register', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    age = models.PositiveIntegerField()
    num_people = models.PositiveIntegerField()
    booking_date = models.DateField(default=timezone.now)
    num_nights = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  
    
    def save(self, *args, **kwargs):
        self.total_amount = self.room.price * self.num_nights
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.room.roomnum} by {self.user.username}"
