from django.shortcuts import render,redirect,get_object_or_404
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress,Order,OrderItem
from django.contrib import messages
from store.models import Products,Profile



def payment_success(request):
    return render(request,'payment/payment_success.html', {})




def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quants()
    total_price = cart.total_price()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.filter(user__id=request.user.id).first()
        shipping_form = ShippingForm(request.POST or None,instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities' : quantities,'total_price': total_price,'shipping_form':shipping_form})
    else :
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities' : quantities,'total_price': total_price,'shipping_form':shipping_form})

def confirm_order(request):
    if request.method == "POST" :
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quants()
        total_price = cart.total_price()


        user_shipping = request.POST
        request.session['user_shipping']=user_shipping 

     
        return render(request, 'payment/confirm_order.html', {'cart_products':cart_products, 'quantities' : quantities,'total_price': total_price,'shipping_info':user_shipping})
   
         

        #  return render(request,'payment/confirm_order.html', {})
    else:
        messages.success(request,"دسترسی ب این صفحه امکان پذیرر نمیباشد ")
        return redirect("home")


def proccess_order(request):
    if request.method == "POST" :
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quants()
        total_price = cart.total_price()
        user_shipping = request.session.get('user_shipping')
        
        full_name = user_shipping['shipping_full_name']
        email = user_shipping['shipping_email']
        full_address = f'{user_shipping["shipping_address1"]}\n{user_shipping["shipping_address2"]}\n{user_shipping["shipping_city"]}\n{user_shipping["shipping_state"]}\n{user_shipping["shipping_zipcode"]}'
       
        if request.user.is_authenticated :
            user = request.user
            new_order = Order(
            user=user,
            full_name=full_name ,
            email = email,
            shipping_address = full_address,
            amount_paid = total_price)

            new_order.save()

            for key in list(request.session.keys()):
                if key == 'session_key' :
                    del request.session[key]
            
            cu = Profile.objects.filter(user__id = request.user.id)
            cu.update(old_cart="")

            for product in cart_products:
                order_instance = get_object_or_404(Order, id=new_order.pk)

                prod = get_object_or_404(Products,id=product.id)
                price = product.price
                for k,v in quantities.items() :
                    if int(k) == product.id :
                        new_orderitem =OrderItem(
                order = order_instance,
                product=prod,
                price = price,
                user=user,
                quantity=v
                )
                        new_orderitem.save()
                

            messages.success(request,"سفارش ثبت شد")
            return redirect("home")
        else:
            new_order = Order(
            full_name=full_name,
            email = email,
            shipping_address = full_address,
            amount_paid = total_price)

            new_order.save()

            for product in cart_products:
                order_instance = get_object_or_404(Order, id=new_order.pk)

                prod = get_object_or_404(Products,id = product.id)
                price = product.price
                for k,v in quantities.items() :
                    if int(k) == product.id :
                        new_orderitem =OrderItem(
                        order = order_instance,
                        product=prod,
                        price = price,
                        quantity=v
                ) 
                        new_orderitem.save()
            for key in list(request.session.keys()):
                if key == 'session_key' :
                   del request.session[key]
            
            messages.success(request,"سفارش ثبت شد  ")
            return redirect("home")


      
    else:
        messages.success(request,"دسترسی ب این صفحه امکان پذیرر نمیباشد ")
        return redirect("home")


