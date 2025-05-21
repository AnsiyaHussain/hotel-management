from django.contrib import admin
from backend.models import Register,Feedback,FoodCategory,FoodItem,Cart,Order,OrderItem,Contactus,Room,RoomCategory,RoomBooking

# Register your models here.
admin.site.register(Register)
admin.site.register(Feedback)
admin.site.register(FoodCategory)
admin.site.register(FoodItem)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Contactus)
admin.site.register(RoomCategory)
admin.site.register(Room)
admin.site.register(RoomBooking)