from rest_framework.decorators import api_view 
from django.shortcuts import get_object_or_404
from store.models import Products 
from.serializers import Products_serializer
from rest_framework.response import Response
from rest_framework import status




@api_view(["GET"])
def api_products(request):
        products = Products.objects.all()

        if not products.exists():
            return Response({"message":"No products found"},status=status.HTTP_404_NOT_FOUND)
        serialize = Products_serializer(products,many =True)
        return Response(serialize.data,status=status.HTTP_200_OK)


@api_view(["GET"])
def api_product(request,id):
        product = get_object_or_404(Products,id=id)
        serialize = Products_serializer(product)
        return Response(serialize.data,status=status.HTTP_200_OK)


@api_view(["POST"])
def api_add(request):
    data = request.data
        name= request.data.get("name")
        if products.objects.filter(name=name).exists():
                return Response({"message":"this product already exist"},status=status.HTTP_400_BAD_REQUEST)
                
        serialize = Products_serializer(data=data)
        if serialize.is_valid():
                serialize.save()
                return Response (serialize.data,status=status.HTTP_201_CREATED)
        return Response (serialize.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def api_update(request,id):
        product = get_object_or_404(Products,id=id)
        serialize = Products_serializer(product,data = request.data ,partial =True) 
        if serialize.is_valid():
               serialize.save()
               return Response(serialize.data,status=status.HTTP_200_OK)
        print(serialize.errors)
        return Response (serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    



@api_view(["DELETE"])
def api_delete(request,id):
       product = get_object_or_404(Products,id=id)
       product.delete()
       return Response({"message":"item successfully deleted"},status=status.HTTP_200_OK)



   
