from django.urls import path
from backend import views
from django.views.generic import TemplateView

urlpatterns = [

    path('',views.main , name='main'),
    path('firstabout/',views.firstabout , name='firstabout'),

    #................... admin module starts here .....................

    path('index/',views.index , name='index'),
    path('about/',views.about , name='about'),
    path('Menu/',views.Menu , name='Menu'),
    path('menu_list/<int:mid>/',views.menu_list , name='menu_list'),
    path('contact/',views.contact , name='contact'),
    path('feature/',views.feature , name='feature'),
    path('testimonial/',views.testimonial , name='testimonial'),
    path('blog/',views.blog , name='blog'),
    path('registration/',views.registration , name='registration'),
    path('login/',views.login , name='login'),
    path('feedback/',views.feedback , name='feedback'),
    path('profile/',views.profile , name='profile'),
    path('view_cart/',views.view_cart , name='view_cart'),
    path('gallery/',views.gallery , name='gallery'),
    path('add_to_cart/',views.add_to_cart , name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('feedback_success/', TemplateView.as_view(template_name='f_success.html'), name='feedback_success'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_status/', views.order_status, name='order_status'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('rooms/', views.rooms, name='rooms'),
    path('list_rooms/<str:category_name>/', views.list_rooms, name='list_rooms'),  
    path('book_room/', views.book_room, name='book_room'),
    path('roombookinglist/', views.roombookinglist, name='roombookinglist'),
    path('success/', views.success_page, name='success_page'),



#................... admin module starts here .....................


    path('adminhome/',views.adminhome , name='adminhome'),
    path('adminlogin/',views.adminlogin , name='adminlogin'),
    path('adlogout/',views.adlogout , name='adlogout'),
    path('add_food_category/',views.add_food_category , name='add_food_category'),
    path('edit_food_category/<int:category_id>/',views.edit_food_category , name='edit_food_category'),
    path('food_category_list/',views.food_category_list , name='food_category_list'),
    path('delete_food_category/<int:category_id>/', views.delete_food_category, name='delete_food_category'),
    path('add_food/',views.add_food , name='add_food'),
    path('foodlisting/',views.foodlisting , name='foodlisting'),
    path('edit_food_item/<int:food_id>/',views.edit_food_item , name='edit_food_item'),
    path('delete_food_item/<int:d_id>/',views.delete_food_item , name='delete_food_item'),
    path('admin_view_orders/', views.admin_view_orders, name='admin_view_orders'),
    path('approve_order/<int:order_id>/', views.approve_order, name='approve_order'),
    path('reject_order/<int:order_id>/', views.reject_order, name='reject_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('userlist_of_admin/', views.userlist_of_admin, name='userlist_of_admin'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('feedback_list/', views.feedback_list, name='feedback_list'),
    path('delete_feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    path('contact_list/', views.contact_list, name='contact_list'),
    path('clear_contacts/', views.clear_contacts, name='clear_contacts'),
    path('addroomcat/', views.addroomcat, name='addroomcat'),
    path('add_rooms/', views.add_rooms, name='add_rooms'),
    path('rooms_list/', views.rooms_list, name='rooms_list'),
    path('get-room-data/<int:room_id>/', views.get_room_data, name='get_room_data'),
    path('edit-room/', views.edit_room, name='edit_room'),
    path('delete-room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('get_rooms_by_category/<int:category_id>/', views.get_rooms_by_category, name='get_rooms_by_category'),
    path('manage_food/', views.manage_food, name='manage_food'),
    path('manage_rooms/', views.manage_rooms, name='manage_rooms'),
    path('view_room_categories/', views.view_room_categories, name='view_room_categories'),
    path('editcat/', views.editcat, name='editcat'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),

]