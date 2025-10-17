from django.urls import path 
from .views import ( api_products,api_product,api_delete,api_update,api_add)


urlpatterns = [
    path("products_list/",api_products,name="products_list"),
    path("product/<int:id>/",api_product,name="product"),
    path("delete_product/<int:id>/",api_delete,name="delete_product"),
    path("update_product/<int:id>/",api_update,name="update_product"),
    path("add_product/",api_add,name="add_product"),


]
