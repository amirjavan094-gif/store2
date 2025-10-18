from django.shortcuts import render,redirect
from .models import Products,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .forms import SignUpForms,UpdateUserForm,UpdatePasswordForm,UpdateUserInfo
from django.contrib import messages
from django.db.models import Q
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress,Order,OrderItem
from django.contrib import admin

def order_details(request,pk):
    if request.user.is_authenticated:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        context = {
            "order":order,
            "items":items
        }
        return render(request,"orders_details.html",context)
    else:
        messages.success(request,"دسترسی ب این صفحه امکان پذیر نمیباشد")
        return redirect("home")

def user_orders(request):
    if request.user.is_authenticated:
        delivered_orders = Order.objects.filter(user=request.user,status="Delivered")
        other_orders = Order.objects.filter(user=request.user).exclude(status="Delivered")

        context = {
          "delivered": delivered_orders,
          "other" :other_orders

        }
        return render(request,'orders.html',context)
    else:
        messages.success(request,"دسترسی ب این صفحه امکان پذیر نمیباشد")
        return redirect("home")
    






def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched =Products.objects.filter(Q(name__icontains=searched)| Q(description__icontains=searched))
        
        if not searched:
            messages.success(request, "چنین محصولی وجود ندارد ")
            return render(request,'search.html',{})
        else :
            return render(request,'search.html',{'searched':searched})
        
    return render(request,'search.html',{})



    

def category_summary(request):
    all_cat = Category.objects.all()
    return render(request,'category_summary.html',{'all_cat':all_cat})


def category_product(request,id):
    category = Category.objects.get(id=id)
    products = category.products.all()
    return render(request, 'category_product.html', {'category': category, 'products': products})



def home(request):
    all_product = Products.objects.all()
    return render(request,'index.html',{'products':all_product})
  
def about(request):

    return render(request,'about.html')

def contact(request):
    return render(request, 'contact.html')


def signup(request):
    form = SignUpForms()
    if request.method == "POST" : 
        form = SignUpForms(request.POST)
        if form.is_valid():
          form.save()
          username = form.cleaned_data['username']
          password1 = form.cleaned_data['password1']
          user = authenticate(request,username=username , password = password1)


          if user:
             login(request, user)
             messages.success(request, "اکانت شما ساخته شد")
             return redirect("home")
          else:
             messages.error(request, " ثبت‌ نام ناموفق بود")
             return render(request, 'signup.html', {'form': form})



        else:
            messages.error(request,"مشکلی در ثبت نام شما وجود دارد   ")
            return render(request, 'signup.html', {'form': form})
    else :
       return render(request, 'signup.html', {'form':form})
    
def update_user(request):
    if request.user.is_authenticated:
        current_user =User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None,instance=current_user)
        if user_form.is_valid():
           user_form.save()
           messages.success(request,'پروفایل شما ویرایش شد')
           return redirect("home")
    
        return render(request, 'update_user.html',{'user_form':user_form})
    else:
        messages.success(request,'ابتدا باید لاگین شوید')
        return redirect("home")    
    
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)

        if request.method == "POST":
            form = UpdateUserInfo(request.POST, instance=current_user)
            shipping_form = ShippingForm(request.POST, instance=shipping_user)

            if form.is_valid() and shipping_form.is_valid():   # 🔑 بجای or
                form.save()
                shipping_form.save()
                messages.success(request, 'اطلاعات کاربری شما ویرایش شد')
                return redirect("update_info")   # 🔑 ری‌دایرکت به همین صفحه برای نمایش داده‌های جدید
        else:
            form = UpdateUserInfo(instance=current_user)
            shipping_form = ShippingForm(instance=shipping_user)

        return render(request, "update_info.html", {"form": form, "shipping_form": shipping_form})
    else:
        messages.success(request, 'ابتدا باید لاگین شوید')
        return redirect("home")


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user


        if request.method == "POST":
            form = UpdatePasswordForm(current_user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'رمز با موفقیت ویرایش شد')
                login(request,current_user)
                return  redirect('update_user')
            else:
                for erorr in list(form.errors.values()):
                    messages.error(request,erorr)
                    return redirect("upsate_password")
        
        else:
            form = UpdatePasswordForm(current_user)
            return render(request,'update_password.html',{'form':form})
    else:
        messages.success(request,'اول باید لاگین بشوید')
        return redirect("home")



def logout_user(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید")
    return redirect("home")


def login_user(request):
    if request.method == "POST" :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request,user)
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart=json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)



            messages.success(request, "با موفقیت وارد شدید")
            return redirect("home")
        else :
             messages.error(request, "نام کاربری یا رمز ورود اشتباه است")
             return redirect("login")
        
    return render(request, 'login.html')


def product_details(request,pk):
    product = Products.objects.get(id=pk)
    return render(request, 'product_details.html', {'product': product})

def category(request,cat):
    cat = cat.replace("-"," ")
    try :
       
       category = Category.objects.get(name=cat)
       products = Products.objects.filter(category=category)
       return render(request, 'category.html',{'products': products, 'category': category})
    except:
       messages.success(request,("دسته بندی وجود ندارد"))
       return redirect("home")








