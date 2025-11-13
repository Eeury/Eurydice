from __future__ import annotations

from decimal import Decimal
from typing import Dict, Optional

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import CustomUserCreationForm
from .models import Category, FlashSale, Product, Promotion


def _get_cart(session) -> Dict[str, int]:
    cart = session.get("cart")
    if cart is None:
        cart = {}
        session["cart"] = cart
    return cart


def _build_home_context(
    request: HttpRequest,
    *,
    login_form: Optional[AuthenticationForm] = None,
    signup_form: Optional[CustomUserCreationForm] = None,
) -> Dict[str, object]:
    now = timezone.now()
    promotions = Promotion.objects.filter(is_active=True, start_at__lte=now, end_at__gte=now).order_by("-start_at")[:8]
    flash_sales = FlashSale.objects.filter(is_active=True, start_at__lte=now, end_at__gte=now).order_by("-start_at")[:3]
    hot_products = Product.objects.filter(is_active=True).order_by("-created_at")[:12]
    categories = Category.objects.filter(is_active=True).order_by("name")
    context: Dict[str, object] = {
        "promotions": promotions,
        "flash_sales": flash_sales,
        "hot_products": hot_products,
        "categories": categories,
        "login_form": login_form or AuthenticationForm(request),
        "signup_form": signup_form or CustomUserCreationForm(),
    }
    return context


def home(request: HttpRequest) -> HttpResponse:
    context = _build_home_context(request)
    context["show_login_modal"] = request.GET.get("login") == "1"
    context["show_signup_modal"] = request.GET.get("signup") == "1"
    context["login_next"] = request.GET.get("next", "")
    return render(request, "shop/home.html", context)


def product_list(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.filter(is_active=True).order_by("name")
    products = Product.objects.filter(is_active=True).order_by("name")
    return render(request, "shop/products.html", {"categories": categories, "products": products})


def category_list(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.filter(is_active=True).order_by("name")
    return render(request, "shop/category_list.html", {"categories": categories})


def category_detail(request: HttpRequest, slug: str) -> HttpResponse:
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = category.products.filter(is_active=True).order_by("name")
    categories = Category.objects.filter(is_active=True).order_by("name")
    return render(
        request,
        "shop/category_detail.html",
        {"category": category, "products": products, "categories": categories},
    )


def cart_view(request: HttpRequest) -> HttpResponse:
    cart = _get_cart(request.session)
    product_slugs = list(cart.keys())
    products = Product.objects.filter(slug__in=product_slugs)
    items = []
    total = Decimal("0.00")
    for product in products:
        quantity = int(cart.get(product.slug, 0))
        line_total = product.price * quantity
        total += line_total
        items.append({"product": product, "quantity": quantity, "line_total": line_total})
    return render(request, "shop/cart.html", {"items": items, "total": total})


def cart_add(request: HttpRequest, slug: str) -> HttpResponse:
    product = get_object_or_404(Product, slug=slug, is_active=True)
    cart = _get_cart(request.session)
    cart[product.slug] = int(cart.get(product.slug, 0)) + 1
    request.session.modified = True
    messages.success(request, f"Added {product.name} to cart")
    return redirect(request.META.get("HTTP_REFERER") or "shop:cart_view")


def cart_remove(request: HttpRequest, slug: str) -> HttpResponse:
    cart = _get_cart(request.session)
    if slug in cart:
        del cart[slug]
        request.session.modified = True
        messages.info(request, "Item removed from cart")
    return redirect("shop:cart_view")


@login_required
def checkout(request: HttpRequest) -> HttpResponse:
    cart = _get_cart(request.session)
    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect("shop:product_list")
    product_slugs = list(cart.keys())
    products = Product.objects.filter(slug__in=product_slugs)
    subtotal = Decimal("0.00")
    item_count = 0
    for product in products:
        quantity = int(cart.get(product.slug, 0))
        item_count += quantity
        subtotal += product.price * quantity
    shipping_initial = Decimal("10.00") if subtotal > 0 else Decimal("0.00")
    tax = (subtotal * Decimal("0.07")).quantize(Decimal("0.01"))
    total = (subtotal + shipping_initial + tax).quantize(Decimal("0.01"))
    context = {
        "subtotal": subtotal.quantize(Decimal("0.01")),
        "item_count": item_count,
        "shipping_initial": shipping_initial.quantize(Decimal("0.01")),
        "tax": tax,
        "total": total,
    }
    return render(request, "shop/checkout.html", context)


def login_modal(request: HttpRequest) -> HttpResponse:
    next_url = request.POST.get("next") or request.GET.get("next")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect("shop:home")
        context = _build_home_context(request, login_form=form)
        context["show_login_modal"] = True
        context["login_next"] = next_url or ""
        return render(request, "shop/home.html", context, status=400)

    form = AuthenticationForm(request)
    context = _build_home_context(request, login_form=form)
    context["show_login_modal"] = True
    context["login_next"] = next_url or ""
    return render(request, "shop/home.html", context)


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can log in now.")
            redirect_url = reverse("login")
            if request.POST.get("next"):
                redirect_url += f"?next={request.POST['next']}"
            return redirect(redirect_url)
        messages.error(request, "Please correct the highlighted errors and try again.")
        context = _build_home_context(request, signup_form=form)
        context["show_signup_modal"] = True
        context["login_next"] = request.POST.get("next", "")
        return render(request, "shop/home.html", context, status=400)

    form = CustomUserCreationForm()
    context = _build_home_context(request, signup_form=form)
    context["show_signup_modal"] = True
    context["login_next"] = request.GET.get("next", "")
    return render(request, "shop/home.html", context)


