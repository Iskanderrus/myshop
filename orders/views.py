from django.shortcuts import render

from cart.cart import Cart

from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created


def order_create(request):
    cart = Cart(request)

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # Clear the cart after all items have been processed
            cart.clear()

            # Send an email notification using Celery (delay used to send the notification asynchronously)
            order_created.delay(order.id)

            # Redirect to a success page
            return render(request, "orders/order/created.html", {"order": order})
    else:
        form = OrderCreateForm()

    return render(request, "orders/order/create.html", {"cart": cart, "form": form})
