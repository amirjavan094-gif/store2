from rest_framework.decorators import api_view 
from django.shortcuts import get_object_or_404
from store.models import Products 
from.serializers import ProductsSerializer
from rest_framework.response import Response
from rest_framework import status




@api_view(["GET"])
def api_products(request):
        products = Products.objects.all()

        if not products.exists():
            return Response({"message":"No products found"},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductsSerializer(products,many =True)
        return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(["GET"])
def api_product(request,id):
        product = get_object_or_404(Products,id=id)
        serializer = ProductsSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(["POST"])
def api_add(request):
    data = request.data
    name= request.data.get("name")
    if Products.objects.filter(name=name).exists():
        return Response({"message":"this product already exist"},status=status.HTTP_400_BAD_REQUEST)
                
    serializer = ProductsSerializer(data=data)
    if serializer.is_valid():
       serializer.save()
       return Response (serializer.data,status=status.HTTP_201_CREATED)
    return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def api_update(request,id):
        product = get_object_or_404(Products,id=id)
        serializer = ProductsSerializer(product,data = request.data ,partial =True) 
        if serializer.is_valid():
               serializer.save()
               return Response(serializer.data,status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


@api_view(["DELETE"])
def api_delete(request,id):
       product = get_object_or_404(Products,id=id)
       product.delete()
       return Response({"message":"item successfully deleted"},status=status.HTTP_200_OK)



   
