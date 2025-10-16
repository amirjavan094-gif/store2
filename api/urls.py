from django.urls import path 
from .views import ( api_products,api_product,api_delete,api_update)


urlpatterns = [
    path("products/",api_products,name="products"),
    path("product/<int:id>",api_product,name="product"),
    path("delete/<int:id>/",api_delete,name="delete_product"),
    path("update/<int:id>/",api_update,name="update_product"),



]