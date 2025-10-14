from django.shortcuts import render,get_object_or_404
from .cart import Cart
from store.models import Products
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quants()
    total_price = cart.total_price()
    return render(request,"cart_summary.html",{'cart_products':cart_products, 'quantities' : quantities,'total_price': total_price})

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') ==  'post' :
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Products,id=product_id)
        cart.add(product=product,quantity = product_qty)


    cart_quantity =cart.__len__()
# response = JsonResponse({'Product name': product.name})
    response = JsonResponse({'qty': cart_quantity,'message': "محصول با موفقیت به سبد خرید اضافه شد"})
    return response

def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') ==  'post' :
        product_id = int(request.POST.get('product_id'))
        cart.delete(product_id=product_id)

        response = JsonResponse({'product': product_id,'message':"محصول از سبد خرید حذف شد"})
        return response


def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') ==  'post' :
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id,quantity=product_qty)
      
        
        cart_quantity =cart.__len__()
        return JsonResponse({'qty': cart_quantity,'message': "سبد خرید ویرایش شد"})
    
    



