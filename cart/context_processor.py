from .cart import Cart 
from store.models import Category

def cart(request):
    return {'cart':Cart(request)}


def categories(request):
    return {"categories": Category.objects.all()}
