from .cart import Cart
from .forms import CartAddProductForm


def cart(request):
    return {'cart': Cart(request)}


def cart_product_form(request):
    return {'cart_product_form': CartAddProductForm()}