from django.shortcuts import redirect, render
from django.db import transaction
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            try:
                with transaction.atomic():
                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            price=item['price'],
                            quantity=item['quantity']
                        )
            except:
                return redirect('shop:main')
            cart.clear()
            return redirect('orders:order_success', order.id)
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


def order_success(request, order_id):
    return render(request, 'orders/order/created.html', {'order': order_id})