import requests

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from products.models import Product, Category, Review, Wishlist

from cart.models import Cart, CartItem

from .forms import CustomUserCreationForm

from django.contrib.auth import login, logout, authenticate

from orders.models import Order, OrderItem, Coupon

from django.core.paginator import Paginator

from .forms import (
    ProductForm,
    ProductImageForm,
    ReviewForm
)

from django.db.models import Sum, Count

from decimal import Decimal
from rest_framework_simplejwt.tokens import RefreshToken

def home(request):

    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    query = request.GET.get('q')

    category_id = request.GET.get('category')

    if query:

        products = products.filter(
            name__icontains=query
        )

    if category_id:

        products = products.filter(
            category_id=category_id
        )

    paginator = Paginator(products, 6)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,

        'categories': categories
    }

    return render(
        request,
        'home.html',
        context
    )


def add_product(request):

    if 'access' not in request.session:

        return redirect('login')

    if request.method == 'POST':

        form = ProductForm(request.POST)

        image_form = ProductImageForm(

            request.POST,
            request.FILES
        )

        if form.is_valid() and image_form.is_valid():

            product = form.save(commit=False)

            product.seller = request.user

            product.save()

            product_image = image_form.save(commit=False)

            product_image.product = product

            product_image.save()

            return redirect('seller_dashboard')

    else:

        form = ProductForm()

        image_form = ProductImageForm()

    context = {

        'form': form,

        'image_form': image_form
    }

    return render(
        request,
        'add_product.html',
        context
    )


def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    reviews = product.reviews.all().order_by(
        '-created_at'
    )

    form = ReviewForm()

    average_rating = 0

    if reviews.exists():

        total = sum(
            review.rating
            for review in reviews
        )

        average_rating = (
            total / reviews.count()
        )

    context = {

        'product': product,

        'reviews': reviews,

        'form': form,

        'average_rating': round(
            average_rating,
            1
        )
    }

    return render(
        request,
        'product_detail.html',
        context
    )


def add_to_cart(request, product_id):

    if 'access' not in request.session:

        return redirect('/admin/login/')

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(

        cart=cart,

        product=product
    )

    if not created:

        cart_item.quantity += 1

        cart_item.save()

    return redirect('cart_view')


def cart_view(request):

    if 'access' not in request.session:

        return redirect('login')

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_items = cart.items.all()

    total_price = Decimal('0.00')

    for item in cart_items:

        item.subtotal = (
            Decimal(item.product.price) *
            item.quantity
        )

        total_price += item.subtotal

    discount = Decimal('0.00')

    coupon_id = request.session.get(
        'coupon_id'
    )

    coupon = None

    if coupon_id:

        try:

            coupon = Coupon.objects.get(
                id=coupon_id
            )

            discount = (
                total_price *
                Decimal(coupon.discount_percent)
            ) / Decimal('100')

        except Coupon.DoesNotExist:

            pass

    final_price = (
        total_price - discount
    )

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total_price': total_price,
            'discount': discount,
            'final_price': final_price,
            'coupon': coupon
        }
    )

def register_view(request):

    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:

        form = CustomUserCreationForm()

    context = {

        'form': form
    }

    return render(
        request,
        'register.html',
        context
    )


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            refresh = RefreshToken.for_user(user)

            request.session["access"] = str(
                refresh.access_token
            )

            request.session["refresh"] = str(
                refresh
            )

            login(request, user)

            return redirect("home")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid username or password"
            }
        )

    return render(
        request,
        "login.html"
    )


def logout_view(request):
    logout(request)

    request.session.flush()

    return redirect('home')


def checkout_view(request):

    if 'access' not in request.session:

        return redirect('login')

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_items = cart.items.all()

    if not cart_items.exists():

        return redirect('cart_view')

    order = Order.objects.create(
        buyer=request.user
    )

    total_amount = 0

    for item in cart_items:

        OrderItem.objects.create(

            order=order,

            product=item.product,

            quantity=item.quantity,

            price=item.product.price
        )

        total_amount += (
            item.product.price * item.quantity
        )

    order.total_amount = total_amount

    order.save()

    cart_items.delete()

    return redirect(
        'payment_view',
        order_id=order.id
    )


def orders_view(request):

    if 'access' not in request.session:

        return redirect('login')

    orders = Order.objects.filter(
        buyer=request.user
    ).order_by('-created_at')

    context = {

        'orders': orders
    }

    return render(
        request,
        'orders.html',
        context
    )


def increase_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )

    cart_item.quantity += 1

    cart_item.save()

    return redirect('cart_view')


def decrease_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save()

    else:

        cart_item.delete()

    return redirect('cart_view')


def remove_cart_item(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )

    cart_item.delete()

    return redirect('cart_view')


def seller_dashboard(request):

    if not request.user.is_authenticated:

        return redirect('login')

    products = Product.objects.filter(
        seller=request.user
    )

    total_products = products.count()

    seller_orders = OrderItem.objects.filter(
        product__seller=request.user
    )

    total_orders = seller_orders.count()

    total_revenue = seller_orders.aggregate(
        revenue=Sum('price')
    )['revenue'] or 0

    context = {

        'products': products,

        'total_products': total_products,

        'total_orders': total_orders,

        'total_revenue': total_revenue
    }

    return render(
        request,
        'seller_dashboard.html',
        context
    )


def edit_product(request, product_id):

    if 'access' not in request.session:

        return redirect('login')

    product = get_object_or_404(
        Product,
        id=product_id,
        seller=request.user
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():

            form.save()

            return redirect('seller_dashboard')

    else:

        form = ProductForm(instance=product)

        context = {

            'form': form
        }

        return render(
            request,
            'edit_product.html',
            context
        )


def delete_product(request, product_id):

    if 'access' not in request.session:

        return redirect('login')

    product = get_object_or_404(
        Product,
        id=product_id,
        seller=request.user
    )

    product.delete()

    return redirect('seller_dashboard')


def payment_view(request, order_id):

    print(
        "SESSION ACCESS TOKEN:",
        request.session.get('access')
    )

    token = request.session.get('access')

    context = {

        'order': {

            'id': order_id
        },

        'token': token
    }

    return render(
        request,
        'payment.html',
        context
    )


def add_review(request, product_id):

    if not request.user.is_authenticated:

        return redirect('login')

    product = get_object_or_404(
        Product,
        id=product_id
    )

    already_reviewed = Review.objects.filter(
        product=product,
        user=request.user
    ).exists()

    if already_reviewed:

        return redirect(
            'product_detail',
            product_id=product.id
        )

    if request.method == 'POST':

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.product = product

            review.user = request.user

            review.save()

    return redirect(
        'product_detail',
        product_id=product.id
    )


def add_to_wishlist(request, product_id):

    if not request.user.is_authenticated:

        return redirect('login')

    product = get_object_or_404(
        Product,
        id=product_id
    )

    Wishlist.objects.get_or_create(

        user=request.user,

        product=product
    )

    return redirect(
        'product_detail',
        product_id=product.id
    )


def wishlist_view(request):

    if not request.user.is_authenticated:

        return redirect('login')

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        'wishlist.html',
        {
            'wishlist_items': wishlist_items
        }
    )


def remove_from_wishlist(request, wishlist_id):

    if not request.user.is_authenticated:

        return redirect('login')

    wishlist_item = get_object_or_404(
        Wishlist,
        id=wishlist_id,
        user=request.user
    )

    wishlist_item.delete()

    return redirect('wishlist_view')

def seller_orders_view(request):

    if not request.user.is_authenticated:

        return redirect('login')

    order_items = OrderItem.objects.filter(

        product__seller=request.user

    ).select_related(

        'order',
        'product'
    )

    return render(

        request,

        'seller_orders.html',

        {
            'order_items': order_items
        }
    )

def update_order_status(request, order_id):

    if not request.user.is_authenticated:

        return redirect('login')

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if order.status == 'pending':

         order.status = 'processing'

    elif order.status == 'processing':

           order.status = 'shipped'

    elif order.status == 'shipped':

          order.status = 'delivered'
          
    order.save()

    return redirect(
        'seller_orders_view'
    )

def apply_coupon_view(request):

    if request.method == 'POST':

        code = request.POST.get(
            'coupon_code'
        )

        try:

            coupon = Coupon.objects.get(
                code=code,
                active=True
            )

            request.session['coupon_id'] = (
                coupon.id
            )

        except Coupon.DoesNotExist:

            request.session['coupon_id'] = None

    return redirect('cart_view')