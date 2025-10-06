
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout_user,name='logout'),
    path('login/',views.login_user,name='login'),
    path('update_user/',views.update_user,name='update_user'),
    path('update_info/',views.update_info,name='update_info'),
    path('update_password/',views.update_password,name='update_password'),
    path('product_details/<int:pk>/',views.product_details,name='product_details'),
    path('category_summary/',views.category_summary,name='category_summary'),
    path('category_product/<int:id>',views.category_product,name='category_product'),
    path('search/',views.search,name='search'),
    path('orders/',views.user_orders,name='orders'),
    path('order_details/<int:pk>',views.order_details,name='order_details'),
    

]

