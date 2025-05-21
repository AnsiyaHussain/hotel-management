from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from backend.models import Register,Feedback,FoodItem,Cart,Order,OrderItem,Contactus,Room,RoomCategory,RoomBooking
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.hashers import make_password,check_password
from django.views.decorators.csrf import csrf_exempt



def main(request):
    return render(request,'firstpage.html')


def firstabout(request):
    return render(request,'fabout.html')

#..............User module starts here............

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    m=request.session.get('email')
    con = Register.objects.get(email=m)
    if request.method =='POST':
        name=request.POST.get("name")
        email=request.POST.get("email")
        sub=request.POST.get("ss")
        message=request.POST.get("messages")
        obj=Contactus(name=name,email=email,subject=sub,message=message)
        obj.save()
    return render(request,'contact.html',{'con':con})

def feature(request):
    return render(request,'feature.html')


def registration(request):
    if request.method == 'POST':
        name = request.POST.get("uname")
        email = request.POST.get("email")
        phone = request.POST.get("phn")
        passw = request.POST.get("psw")

        if Register.objects.filter(email=email).exists():
            alert_message = "<script>alert('Email already in use !! Please enter a valid Email'); window.location.href='/registration/';</script>"
            return HttpResponse(alert_message)
        us = Register(username=name, email=email, phnumber=phone, password=passw)
        us.save()
        return redirect('login')
    return render(request, 'user_reg.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        passw = request.POST.get("psw")
        try:
            us = Register.objects.get(email=email, password=passw)
            smail = us.email
            request.session['email'] = smail
            return redirect('index')
        except :  
            message = "Invalid Email or password!"
        return render(request, 'user_reg.html', {'message': message})
    return render(request, 'user_reg.html')


def view_cart(request):
    semail = request.session.get('email') 
    if not semail:
        return redirect('login')   
    user = Register.objects.get(email=semail)

    cart_items = Cart.objects.filter(user=user)
    total_price = sum(item.tprice for item in cart_items)
  
    discount = 0
    if total_price > 16000:
        discount = 1999
    elif total_price > 10000:
        discount = 899
    elif total_price > 5000:
        discount = 499

    discounted_price = total_price - discount  
    user_orders_exist = Order.objects.filter(user=user).exists()

    # Fetch booked rooms for the user
    booked_rooms = RoomBooking.objects.filter(user=user)

    return render(request, 'cartpage.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'discounted_price': discounted_price, 
        'discount': discount, 
        'user_orders_exist': user_orders_exist,
        'booked_rooms': booked_rooms  # Pass booked rooms
    })


def profile(request):
    semail = request.session.get('email')
    if not semail:
        return redirect('login')

    user = get_object_or_404(Register, email=semail)
    
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phnumber = request.POST.get('phnumber')
        user.address = request.POST.get('address')

        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES['profile_image']
        user.save()  
        return redirect('profile')  
    
    return render(request, 'profile.html', {'user': user})


def order_status(request):
    semail = request.session.get('email') 
    if not semail:
        return redirect('login')
    
    user = Register.objects.get(email=semail)
    
    user_orders = Order.objects.filter(user=user).prefetch_related('order_items')
    
    return render(request, 'order_status.html', {'user_orders': user_orders})


def remove_from_cart(request, product_id):
    semail = request.session.get('email')  
    if not semail:
        return redirect('login')
    user = get_object_or_404(Register, email=semail)
    cart_item = get_object_or_404(Cart, id=product_id, user=user)
    cart_item.delete()
    messages.success(request, f'{cart_item.product.name} has been removed from your cart!')
    return redirect('view_cart')

def add_to_cart(request):
    semail = request.session.get('email') 
    if not semail:
        return redirect('login')
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))  
        
        try:
            product = FoodItem.objects.get(id=product_id)
        except FoodItem.DoesNotExist:
            return redirect('Menu')  

        user = Register.objects.get(email=semail)

        existing_cart_item = Cart.objects.filter(user=user, product=product).first()
        if existing_cart_item:
            existing_cart_item.qty += quantity
            existing_cart_item.tprice = existing_cart_item.qty * Decimal(product.price)
            existing_cart_item.save()
        else:
            cart_item = Cart(user=user, product=product, qty=quantity)
            cart_item.tprice = cart_item.qty * Decimal(product.price)  
            cart_item.save()

        return redirect('Menu')  
    
    return redirect('Menu')


def place_order(request):
    semail = request.session.get('email')  
    if not semail:
        return redirect('login')

    user = get_object_or_404(Register, email=semail)

    cart_items = Cart.objects.filter(user=user)
    total_price = sum(item.tprice for item in cart_items)

    discount = 0
    if total_price > 16000:
        discount = 1999
    elif total_price > 10000:
        discount = 899
    elif total_price > 5000:
        discount = 499

    discounted_price = total_price - discount

    if request.method == 'POST':
        order_date = request.POST.get('order_date') or timezone.now().date()
        venue = request.POST.get('venue')
        address = request.POST.get('address')
        place = request.POST.get('place')
        event_date = request.POST.get('event_date')
        preferred_time = request.POST.get('preferred_time')

        order = Order.objects.create(
            user=user,
            total_price=discounted_price,  
            order_date=order_date,
            venue=venue,
            address=address,
            place=place,
            eventdate=event_date,
            preferred_time=preferred_time
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                qty=item.qty,
                tprice=item.tprice
            )
        
        cart_items.delete()
        
        return redirect('view_cart')  

    else:
        default_order_date = timezone.now().date()

    return render(request, 'cartpage.html', {
        'total_price': total_price,
        'discounted_price': discounted_price,
        'default_order_date': default_order_date
    })



def feedback_success(request):
    return render(request,'f_success.html')


def gallery(request):
    feedbacks = Feedback.objects.all()  
    return render(request, 'gallery.html', {'feedbacks': feedbacks})


def Menu(request):
    categories = FoodCategory.objects.all()
    return render(request, 'menu.html', {'categories': categories})

def menu_list(request, mid):
    cat = get_object_or_404(FoodCategory, id=mid)  
    search_query = request.GET.get('search', '').strip() 

    if search_query:
        products = FoodItem.objects.filter(category=cat, name__icontains=search_query) 
    else:
        products = FoodItem.objects.filter(category=cat)

    return render(request, 'menulist.html', {'cat': cat, 'products': products, 'search_query': search_query})

def testimonial(request):
    return render(request,'testimonial.html')

def blog(request):
    return render(request,'blog.html')



def feedback(request):
    semail = request.session.get('email') 
    if not semail:
        return redirect('login')

    user = get_object_or_404(Register, email=semail)

    if request.method == 'POST':
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')
        image = request.FILES.get('image')
        image_description = request.POST.get('image_description')
        
        Feedback.objects.create(
            name=user.username, 
            feedback_text=feedback_text,
            rating=rating,
            image=image,
            image_description=image_description,
        )
        return redirect('feedback_success')  

    return render(request, 'feedback_rate.html', {'user': user})


def user_logout(request):
    request.session.flush()
    return redirect('main')

def rooms(request):
    room_categories = RoomCategory.objects.all()  
    return render(request, 'room.html', {'room_categories': room_categories})


def list_rooms(request, category_name):
    category = RoomCategory.objects.get(name=category_name)
    rooms = category.room_set.filter(is_available=True)
    return render(request, 'listrooms.html', {'category': category, 'rooms': rooms})


def book_room(request):
    # Get the email from session
    semail = request.session.get('email')  
    if not semail:
        return redirect('login')

    if request.method == 'POST':
        # Get data from the form
        room_id = request.POST.get('room_id')
        room_price = float(request.POST.get('room_price'))
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        age = int(request.POST.get('age'))
        num_people = int(request.POST.get('num_people'))
        num_nights = int(request.POST.get('num_nights'))
        
        # Calculate total amount based on room price and number of nights
        total_amount = room_price * num_nights
        
        # Get the room object using room_id
        room = Room.objects.get(id=room_id)

        # Fetch the Register instance using the logged-in user's email
        try:
            register_user = Register.objects.get(email=semail)
        except Register.DoesNotExist:
            return HttpResponse("No registered details found for this user. Please complete your registration.", status=400)

        # Create a RoomBooking instance
        booking = RoomBooking(
            user=register_user,  # Assign the Register instance to the 'user' field
            room=room,
            phone_number=phone_number,
            address=address,
            age=age,
            num_people=num_people,
            num_nights=num_nights,
            total_amount=total_amount,
            booking_date=timezone.now()
        )
        
        # Save the booking
        booking.save()
        
        # Redirect to a success page after booking
        return redirect('success_page')  # Replace with the actual success page URL
    
    return HttpResponse("Invalid request", status=400)


def success_page(request):
    return render(request, 'booking_confirmation.html')


#................... admin module starts here .....................


from django.contrib.auth import authenticate, login as auth_login
from backend.models import FoodCategory


def adminhome(request):
    contact = Contactus.objects.all()
    contact_count = contact.count()
    return render(request,'admindex.html',{'contact_count':contact_count})

def adminlogin(request):
    if request.method == 'POST':
        uname = request.POST.get('usr')
        pawd = request.POST.get('psw')
        user = authenticate(request, username=uname, password=pawd)
        if user is not None:
            auth_login(request, user)  
            return redirect('adminhome')
        else:
            return render(request, 'adlogin.html', {'error': 'Invalid username or password'})

    return render(request, 'adlogin.html')


def add_food_category(request):
    if request.method == "POST":
        category_name = request.POST['category_name']
        category_description = request.POST.get('category_description', '')
        image=request.FILES.get('category_image')
        new_category = FoodCategory(name=category_name, description=category_description,catimage=image)
        new_category.save()
        return redirect('food_category_list')
    return render(request, 'addcatogory.html')


def food_category_list(request):
    categories = FoodCategory.objects.all() 
    return render(request, 'foodlist.html', {'categories': categories})

def edit_food_category(request, category_id):
    category = FoodCategory.objects.get(id=category_id)
    if request.method == "POST":
        category.name = request.POST.get('category_name')
        category.description = request.POST.get('category_description')
        if request.FILES.get('category_image'):
            category.catimage = request.FILES['category_image']
        category.save()
        return redirect('food_category_list')
    return render(request, 'editcatogory.html', {'category': category})

def delete_food_category(request, category_id):
    category = get_object_or_404(FoodCategory, id=category_id)
    category.delete()
    return redirect('food_category_list')

def add_food(request):
    if request.method == 'POST':
        category_id = request.POST['category']
        food_name = request.POST['food_name']
        price = request.POST['price']
        food_image = request.FILES.get('food_image')

        FoodItem.objects.create(
            category_id=category_id,
            name=food_name,
            price=price,
            fimage=food_image
        )
        messages.success(request, 'Food item added successfully!')
        return redirect('add_food')  
    
    categories = FoodCategory.objects.all()
    return render(request, 'addfood.html', {'categories': categories})

def foodlisting(request):
    foods = FoodItem.objects.select_related('category').all() 
    return render(request, 'list_food.html', {'foods': foods})

def edit_food_item(request, food_id):
    food = FoodItem.objects.get(id=food_id)
    categories = FoodCategory.objects.all()

    if request.method == 'POST':
        food.category_id = request.POST['category']
        food.name = request.POST['food_name']
        food.price = request.POST['price']
        if request.FILES.get('food_image'):
            food.fimage = request.FILES['food_image']
        food.save()
        return redirect('foodlisting')
    return render(request, 'editfood.html', {'food': food, 'categories': categories})


def delete_food_item(request, d_id):
    food_item = get_object_or_404(FoodItem, id=d_id)
    food_item.delete()
    return redirect('foodlisting')

def admin_view_orders(request):
    orders = Order.objects.all().order_by('-order_date')  
    return render(request, 'view_orders.html', {'orders': orders})


def approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'Approved'
    order.save()
    return redirect('admin_view_orders')

def reject_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'Rejected'
    order.save()
    return redirect('admin_view_orders')

def adlogout(request):
    request.session.flush()
    return redirect('adminlogin')

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('admin_view_orders') 


def userlist_of_admin(request):
    search_query = request.GET.get('search', '')  # Get the search query from the URL params

    if search_query:
        # Filter users based on the search query (case insensitive)
        users = Register.objects.filter(username__icontains=search_query)
    else:
        # If no search query, get all users
        users = Register.objects.all()

    return render(request,'users_list.html',{'users': users})

def delete_user(request, user_id):
    user = Register.objects.get(id=user_id)
    user.delete()
    return redirect('userlist_of_admin')  

def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at') 
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})

def delete_feedback(request, feedback_id):
    feedback = Feedback.objects.get(id=feedback_id)
    feedback.delete()
    return redirect('feedback_list') 

def contact_list(request):
    contact = Contactus.objects.all()  
    contact_count = contact.count()
    return render(request, 'contactlist.html', {'contact': contact, 'contact_count': contact_count})

def clear_contacts(request):
    if request.method == 'POST': 
        Contactus.objects.all().delete()  
        return redirect('contact_list')  
    return redirect('contact_list')

def addroomcat(request):
    if request.method == "POST":
        rn = request.POST.get('name')
        desc = request.POST.get('description')
        image = request.FILES.get('image')  # Get the uploaded image

        obj = RoomCategory(name=rn, categoryDescription=desc, image=image)
        obj.save()
        success = True  
        return render(request, 'addroomcategory.html', {'success': success})
    return render(request, 'addroomcategory.html')


def add_rooms(request):
    success = False
    categories = RoomCategory.objects.all()  # Fetch all categories
    
    if request.method == 'POST':
        category = request.POST.get('category')
        roomnum = request.POST.get('room_number')
        price = request.POST.get('price')
        description = request.POST.get('description', '')  # Optional field
        is_available = 'is_available' in request.POST  # This will be True if checkbox is checked
        room_image = request.FILES.get('room_image')  # Handle file upload

        # Create the new room
        room = Room(
            category_id=category, 
            roomnum=roomnum, 
            price=price, 
            description=description, 
            image=room_image,
            is_available=is_available
        )
        room.save()
        success = True  # Set success to True after room is added
        return redirect('add_rooms')  # Optionally, redirect after POST to avoid resubmitting

    return render(request, 'addrooms.html', {'categories': categories, 'success': success})

def rooms_list(request):
    rooms = Room.objects.all()
    categories = RoomCategory.objects.all()
    return render(request, 'roomlist.html', {'rooms': rooms, 'categories': categories})

def get_room_data(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room_data = {
        'id': room.id,
        'roomnum': room.roomnum,
        'category': {
            'id': room.category.id,
            'name': room.category.name
        },
        'price': room.price,
        'is_available': room.is_available
    }
    return JsonResponse(room_data)

@csrf_exempt
def delete_room(request, room_id):
    if request.method == 'DELETE':
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        return JsonResponse({'success': True})
    
def edit_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        room = get_object_or_404(Room, id=room_id)
        
        # Update room data from POST parameters
        room.roomnum = request.POST.get('room_number')
        room.category_id = request.POST.get('category')
        room.price = request.POST.get('price')
        room.is_available = 'is_available' in request.POST
        
        # Check if there is an uploaded image and update the image field
        if request.FILES.get('room_image'):
            room.image = request.FILES['room_image']
        
        room.save()

        # Respond with a success message
        return JsonResponse({'message': 'Room updated successfully'})
def get_rooms_by_category(request, category_id):
    rooms = Room.objects.filter(category_id=category_id)
    room_data = []
    for room in rooms:
        room_data.append({
            'id': room.id,
            'room_number': room.roomnum,
            'price': room.price,
            'is_available': room.is_available,
            'category': room.category.name,
        })
    return JsonResponse({'rooms': room_data})

from django.core.mail import send_mail
from django.conf import settings

def roombookinglist(request):
    # Fetch all room bookings
    bookings = RoomBooking.objects.all()

    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('status')
        
        # Get the booking and update the status
        try:
            booking = RoomBooking.objects.get(id=booking_id)
            old_status = booking.status
            booking.status = new_status
            booking.save()
            
            # Send an email notification to the user about the status change
            send_status_email(booking, old_status, new_status)
            
            messages.success(request, f"Booking status changed to {new_status}.")
        except RoomBooking.DoesNotExist:
            messages.error(request, "Booking not found.")
    
    return render(request, 'admin_bookinglist.html', {'bookings': bookings})

def send_status_email(booking, old_status, new_status):
    subject = f"Your Room Booking Status Changed: {new_status.capitalize()}"
    message = f"""
    Dear {booking.user.username},

    Your room booking for room number {booking.room.roomnum} has been updated.

    Previous Status: {old_status.capitalize()}
    New Status: {new_status.capitalize()}

    Thank you for choosing our service!

    Regards,
    Your Hotel Team
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = booking.user.email
    
    # Send the email
    send_mail(subject, message, from_email, [to_email])

def manage_food(request):
    return render(request,'ad_managefood.html')

def manage_rooms(request):
    return render(request,'manage_rooms.html')

# View to list all room categories
def view_room_categories(request):
    categories = RoomCategory.objects.all()
    return render(request, 'viewroomcat.html', {'categories': categories})

# View to edit a specific room category
def editcat(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        category = get_object_or_404(RoomCategory, pk=category_id)

        # Update the category fields from the POST data
        category.name = request.POST.get('name')
        category.categoryDescription = request.POST.get('categoryDescription')
        
        # Handle image upload if present
        if 'image' in request.FILES:
            category.image = request.FILES['image']

        category.save()

        return redirect('view_room_categories')  # Redirect to the list view after editing

    # If it's a GET request, render the page with the form to edit the category
    category_id = request.GET.get('category_id')
    category = get_object_or_404(RoomCategory, pk=category_id)
    return render(request, 'editroomcat.html', {'category': category})

def delete_category(request, category_id):
    category = get_object_or_404(RoomCategory, pk=category_id)
    category.delete()
    return redirect('view_room_categories') 

def adminlogout(request):
    request.session.flush()
    return redirect('main')

