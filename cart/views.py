from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.models import Product

from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart})


@require_POST
def remove_product_from_cart(request):
    cart = Cart(request)
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    return redirect("cart:cart_detail")


@require_POST
def add_product_to_cart(request):
    cart = Cart(request)
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, id=product_id)

    # If `override_quantity` is intended to be set by a POST parameter or form field
    override_quantity = request.POST.get("override_quantity", False)
    cart.add(product, override_quantity=bool(override_quantity))

    return redirect("cart:cart_detail")
