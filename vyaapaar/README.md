# Vyaapaar - Multi Vendor E-Commerce Platform

## Project Overview

Vyaapaar is a scalable multi-vendor e-commerce platform built using Django and Django REST Framework.  
The project supports multiple user roles including Buyers, Sellers, and Admins.

This project is being developed to learn and implement advanced backend engineering concepts including:
- REST APIs
- Authentication & Authorization
- Payment Gateway Integration
- Docker
- Redis
- Celery
- Real-time Features
- Elasticsearch
- PostgreSQL
- Production-level Project Structure

---

# Planned Features

## Authentication & Authorization
- JWT Authentication
- Login / Registration
- Role-Based Access Control
- Buyer / Seller / Admin permissions

## Product Management
- Product CRUD
- Product Image Upload
- Category Management
- Inventory Tracking

## Shopping Features
- Cart System
- Wishlist
- Coupons & Discounts
- Product Reviews & Ratings

## Order & Payment
- Order Management
- Razorpay Payment Gateway
- PDF Invoice Generation
- Email Notifications

## Advanced Features
- Redis Caching
- Celery Background Tasks
- Elasticsearch Product Search
- Recommendation System
- Real-Time Order Tracking using WebSockets

---

# Tech Stack

## Backend
- Python
- Django
- Django REST Framework

## Database
- PostgreSQL

## Caching & Background Tasks
- Redis
- Celery

## Deployment & DevOps
- Docker
- Nginx

## Search Engine
- Elasticsearch

---

# Project Setup Journey

## Step 1 - Environment Setup

# Initially attempted to create virtual environments using:
python -m venv venv

# Activated environment using:
.\venv\Scripts\Activate.ps1

# Installed packages using:
python -m pip install django djangorestframework

Step 2 - Django Project Creation
# Created Django project:
django-admin startproject vyaapaar

# Created app:
python manage.py startapp ApnaCart

# Added applications inside INSTALLED_APPS:
'rest_framework',
'ApnaCart',

Step 3 - Environment Variables Setup

Installed:

pip install django-environ

# Created .env file for:
SECRET_KEY
DEBUG
Database credentials
Email credentials
Razorpay keys

# Configured environment variables inside settings.py.
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG")

# then remove SECRET_KEY and DEBUG from settings.py

<!-- now create others apps -->
Django encourages multiple apps to promote modularity, maintainability, and reusability

python manage.py startapp accounts
python manage.py startapp products
python manage.py startapp cart
python manage.py startapp orders
python manage.py startapp reviews
python manage.py startapp coupons

# after building our models 
ImageField requires the Pillow library because Django uses Pillow to process image files.

Just install Pillow.

Run:

pip install Pillow

OR:

python -m pip install Pillow

After installation:

python manage.py makemigrations
python manage.py migrate

# note : Instead of directly importing User, Django recommends using:

from django.conf import settings

Why?
Because:
avoids circular import issues
better scalability
recommended by Django
works even if user model changes later

# create superuser
python manage.py createsuperuser

# add media settings 
Open:vyaapaar/settings.py
Add at bottom:
import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configure URLs
Open:vyaapaar/urls.py

register your models to admin
products : Category, Product , ProductImage
account : User 

in admin, everything is working fine

# Install Django REST Framework (DRF)

This converts your Django project into a professional API backend.

Step 1 — Install Packages

Run:

pip install djangorestframework

For JWT authentication also install:

pip install djangorestframework-simplejwt
Step 2 — Add DRF in settings.py

Open:

vyaapaar/settings.py

Add:

INSTALLED_APPS = [

    ...

    'rest_framework',

]
Step 3 — Configure REST Framework

In settings.py add:

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

<!-- JWTAuthentication --> user login using token,token sent in headers, secure API authentication

<!-- IsAuthenticated -->only logged-in users can access APIs by default

# run : python manage.py migrate

# in account, create serializers, views and urls 

# Authentication & Product API Testing
* Successfully tested the User Registration API in Postman, and the API is working correctly.
* Added JWT authentication URLs in accounts/urls.py for secure token-based authentication.
* Tested the Login API in Postman and successfully received JWT access and refresh tokens.
* Created products using the Product Create API in Postman with authenticated seller access.
* Initially faced an issue while fetching the product list because the JWT access token was expiring too quickly.
* Increased the JWT token expiration time in settings.py, after which the Product List API worked successfully and products were fetched correctly.

# product image upload API
This is a very important real-world backend feature because frontend applications upload images through APIs, not Django admin.
 a. multipart/form-data
 b. file uploads in DRF
 c. media handling through APIs
 d. seller authorization
 e. image validation

step 1 : update serializer
step 2 : create upload view
step 3 : add url
step 4 : run server
step 5 : test in postman -> POST http://127.0.0.1:8000/api/products/upload-image/

# Product Update & Delete APIs
This is extremely important because real marketplaces require:
   a. sellers can edit their own products
   b. sellers can delete their own products
   c. buyers cannot modify products
   d. one seller cannot modify another seller’s products

   step 1 : Create Ownership Permission -> products/permissions.py
   step 2 : Update Product Detail View -> products/views.py
   step 3 : Import Permission
   step 4 : run server
   step 5 : test update api -> PATCH http://127.0.0.1:8000/api/products/1/ 
   step 6 : Test Delete API -> DELETE http://127.0.0.1:8000/api/products/1/
   Use seller token.

# Product API Testing & Authorization
a. Successfully tested Product Create API using authenticated seller access tokens in Postman.
b. Implemented secure JWT-based authentication for protected product operations.
c. Added product image upload functionality using multipart/form-data.
d. Verified that uploaded product images are stored correctly inside the media/products/ directory and accessible through browser URLs.
e. Implemented object-level permissions to ensure that only the product owner (seller) can update or delete their products.
f. Successfully tested Product Update API using PATCH requests with seller authorization.
f. Successfully tested Product Delete API using authenticated seller credentials.
g. Verified secure access control by preventing unauthorized users from modifying or deleting products belonging to other sellers.

# Cart System

Features We Will Implement
   Add product to cart
   Remove product from cart
   Update quantity
   Buyer-specific carts
   Calculate total price
   Prevent duplicate cart items

Architecture
Buyer
   ↓
Cart
   ↓
Cart Items
   ↓
Products

   step 1 : Create Cart Models -> cart/models.py
   step 2 : run Migrations
   step 3 : Create Cart Views
   step 4 : Create URLs
   step 5 : Main URLs
   step 6 : Test Add To Cart API : post : http://127.0.0.1:8000/api/cart/add/
   Step 6 — Test Cart API : GET : http://127.0.0.1:8000/api/cart/
   In, Authorization (postman) -> buyer token

   Remove From Cart API
   Step 1 — Create Remove Cart View
   Step 2 — Add URL
   Step 3 — Run Server
   Step 4 — Test Remove API : DELETE : http://127.0.0.1:8000/api/cart/remove/1/
   Step 5 — Verify : GET : http://127.0.0.1:8000/api/cart/
   buyer token

   Update Cart Quantity API
   This allows:
            increase quantity
            decrease quantity
   just like Amazon/Flipkart carts.

   Step 1 — Create Update Quantity View : cart/views.py
   Step 2 — Import Response
   Step 3 — Add URL : cart/urls.py
   Step 4 — Restart Server
   Step 5 — Test Update Quantity API : http://127.0.0.1:8000/api/cart/update/2/
   buyer token

#  Order Management System
Features We Will Build
    Core Order Features
         Place order from cart
         Create order items
         Store order history
         Calculate total amount
         Buyer order tracking
         Seller order visibility
         Order statuses

Real Ecommerce Flow
Products
   ↓
Cart
   ↓
Checkout
   ↓
Order
   ↓
Payment
   ↓
Delivery

Step 1 — Create Order Models : orders/models.py
Step 2 — Make Migrations

# Place Order API
This will:
   convert cart into order
   create order items automatically
   calculate total amount
   clear cart after checkout

This is real ecommerce backend logic.

Step 1 — Create Order Serializers : orders/serializers.py
Step 2 — Create Order Views : orders/views.py
Step 3 — Create URLs : orders/urls.py
Step 4 — Main URL
Step 5 — Run Server
Step 6 — Add Product To Cart Again : POST : http://127.0.0.1:8000/api/cart/add/
Step 7 — Place Order : POST  : http://127.0.0.1:8000/api/orders/place/
step 8 - check cart : GET : http://127.0.0.1:8000/api/cart/
Step 9 — View Order History : GET : http://127.0.0.1:8000/api/orders/
buyer token

# Order Management Upgrade (Status + Seller Side + Workflow)
1. Order Status System (Seller/Admin control)
Pending → Processing → Shipped → Delivered
2. Seller Order Dashboard
Seller sees only their products’ orders
3. Update Order Status API
Only seller/admin can update status
4. Separate Order Items view (detailed tracking)


Step 1 — Seller Order View : orders/views.py
Step 2 — Add URL : orders/urls.py
Step 3 — Test Seller Orders : GET : http://127.0.0.1:8000/api/orders/seller/
seller token

# Automatic Stock Management

Step 1 — Update PlaceOrderView : orders/views.py
Step 2 — Run Server
Step 3 — Test
step 4 - Verify Product : GET : http://127.0.0.1:8000/api/products/

Step 1 — Check Current Product Stock
GET
http://127.0.0.1:8000/api/products/

Find your product.

Example:

{
    "id": 2,
    "name": "Samsung S25",
    "stock": 15
}

Remember current stock.

Step 2 — Add Product To Cart
POST
http://127.0.0.1:8000/api/cart/add/

Authorization:

buyer token

Body → raw → JSON

{
    "product": 2,
    "quantity": 3
}
Step 3 — Place Order
POST
http://127.0.0.1:8000/api/orders/place/

Authorization:

buyer token

No body needed.

Expected Result

Order should create successfully.

Step 4 — Verify Stock Reduced

Again test:

GET
http://127.0.0.1:8000/api/products/

Now stock should become:

15 → 12

because:

ordered quantity = 3
Step 5 — Test Insufficient Stock

Now try adding:

{
    "product": 2,
    "quantity": 100
}

to cart.

Then place order.

Expected Response
{
    "error": "Insufficient stock for Samsung S25"
}

This confirms:

inventory protection works
overselling prevention works

which is real ecommerce behavior.



# Payment Integration (Razorpay)

Cart
 ↓
Order
 ↓
Create Razorpay Order
 ↓
Frontend Payment
 ↓
Payment Verification
 ↓
Order Confirmed

Features We Will Add
1. Razorpay Order Creation API

Backend creates Razorpay payment order.

2. Payment Verification API

Verify:

payment signature
payment authenticity
3. Payment Model

Store:

payment id
order id
payment status
amount
4. Secure Checkout Flow

Only after successful payment:

order becomes confirmed

FIRST IMPORTANT STEP : 
Install Razorpay

Run:
pip install razorpay

Step 2 — Create Razorpay Account
Go to:
Razorpay Official Website

Create:free account

Step 3 — Get API Keys

Dashboard → Settings → API Keys

Generate/View Secret
Click: Regenerate Key

Razorpay will show:
Key ID
Key Secret

You will get:

RAZORPAY_KEY_ID
RAZORPAY_KEY_SECRET

Step 4 — Add Environment Variables
Install dotenv:
pip install python-decouple

Create .env
Inside project root:
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret

Step 5 — settings.py
Add:
from decouple import config

Then:
RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET')

# Razorpay Payment Integration 
Step 1 — Payment Model : orders/models.py
This stores:
Razorpay order id
payment id
payment status
amount
linked ecommerce order

Step 2 — Make Migrations

sorry.dont do any thing


The error is happening because you still have this import:

from accounts.models import User

But your app name is NOT accounts.

Your app name is:

ApnaCart

So Django is trying to find:

accounts/models.py

and it either:

does not exist properly
or does not contain User
Fix

Replace this:

from accounts.models import User

with:

from ApnaCart.models import User

in ALL files where you imported User.

Most likely files:

products/models.py
from ApnaCart.models import User
cart/models.py
from ApnaCart.models import User
orders/models.py
from ApnaCart.models import User

Also confirm:

In settings.py
AUTH_USER_MODEL = 'ApnaCart.User'

After fixing imports:

Run again:

python manage.py makemigrations
python manage.py migrate
Better Professional Approach (IMPORTANT)

Instead of importing User directly:

from ApnaCart.models import User

industry projects usually use:

from django.conf import settings

Then:

seller = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)

Why?

Because:

avoids circular imports
works even if user model changes
recommended by Django documentation

We should refactor to this professional approach next.

ns
SystemCheckError: System check identified some issues:

ERRORS:
accounts.User.profile_image: (fields.E210) Cannot use ImageField because Pillow is not installed.
        HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "python -m pip install Pillow".
products.ProductImage.image: (fields.E210) Cannot use ImageField because Pillow is not installed.
        HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "python -m pip install Pillow".

This error is completely normal.

ImageField requires the Pillow library because Django uses Pillow to process image files.

Just install Pillow.

Run:

pip install Pillow

OR:

python -m pip install Pillow

After installation:

python manage.py makemigrations
python manage.py migrate
Why This Happens

You used:

models.ImageField()

inside:

profile_image
ProductImage.image

Django internally depends on Pillow for:

image validation
image processing
image dimensions

Without Pillow, Django cannot use ImageField.

Verify Installation

Run:

pip show Pillow

If installed correctly, you’ll see version details.

next ?

Now the next professional step is:

Step 1 — Register Models in Django Admin

This helps you:

test database quickly
add products manually
inspect relationships
manage users/orders
Create admin.py
ApnaCart/admin.py
from django.contrib import admin
from .models import User


admin.site.register(User)
products/admin.py
from django.contrib import admin
from .models import Category, Product, ProductImage


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
cart/admin.py
from django.contrib import admin
from .models import Cart, CartItem


admin.site.register(Cart)
admin.site.register(CartItem)
orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem


admin.site.register(Order)
admin.site.register(OrderItem)
Step 2 — Create Superuser

Run:

python manage.py createsuperuser

Example:

Username: admin
Email: admin@gmail.com
Password:
Step 3 — Run Server
python manage.py runserver

Open:

http://127.0.0.1:8000/admin

Login using superuser credentials.

Step 4 — Verify Everything

Inside admin panel check:

Users
Categories
Products
Product Images
Orders
Cart

If all appear correctly → models are working properly.

VERY IMPORTANT NEXT STEP

After admin verification:

We should NOT jump directly into APIs.

Correct workflow is:

Next We Build
Media/Image settings
DRF installation
JWT authentication
User Registration API
Login API
Role permissions

That creates the foundation of the entire platform.

User is defined in accounts app and not in ApnaCart app

Exactly — that means your earlier setup was actually correct.

So your structure is:

vyaapaar/      → project folder/settings.py
accounts/      → user app
products/
cart/
orders/

Therefore:

Correct Setting

In settings.py

AUTH_USER_MODEL = 'accounts.User'

because:

accounts → app name
User → model name
Correct Import

Inside other apps:

from accounts.models import User

OR the better professional approach:

from django.conf import settings

then:

seller = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)
Your Earlier Error Happened Because

You probably:

changed imports inconsistently
or changed AUTH_USER_MODEL
or mixed ApnaCart and accounts

Now keep it consistent everywhere.

Final Correct Structure
settings.py
AUTH_USER_MODEL = 'accounts.User'
accounts/models.py
class User(AbstractUser):
products/models.py

Preferred:

from django.conf import settings
seller = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)

Now run again:

python manage.py makemigrations
python manage.py migrate

Then:

python manage.py createsuperuser
this is my account app "from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='buyer'
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
" ,  and my  prodcut model "from django.db import models

# Create your models here.
from accounts.models import User


class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'seller'}
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.product.name"

Your models are correct now.
The import:

from accounts.models import User

is valid because your custom User model is inside the accounts app.

Your setup is consistent.

Now Improve It Professionally

Instead of directly importing User, Django recommends using:

from django.conf import settings

Why?

Because:

avoids circular import issues
better scalability
recommended by Django
works even if user model changes later
Better Product Model

Replace this:

from accounts.models import User

with:

from django.conf import settings

Then replace:

seller = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    limit_choices_to={'role': 'seller'}
)

with:

seller = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    limit_choices_to={'role': 'seller'}
)
Final Professional Version
from django.db import models
from django.conf import settings


class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'seller'}
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.product.name
Now Run
python manage.py makemigrations

Then:

python manage.py migrate

If successful:

python manage.py createsuperuser

Then:

python manage.py runserver

After that we’ll:

register admin models
configure media files
install DRF
build JWT authentication APIs
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "D:\Django_projects\E-Commerce\vyaapaar\ApnaCart\admin.py", line 4, in <module>
    from .models import User
ImportError: cannot import name 'User' from 'ApnaCart.models' (D:\Django_projects\E-Commerce\vyaapaar\ApnaCart\models.py)

The issue is now very clear.

Your User model is inside:

accounts/models.py

BUT in your admin file you are importing from:

from .models import User

inside:

ApnaCart/admin.py

Django is trying to find:

ApnaCart/models.py

and there is NO User model there.

Fix

Open:

ApnaCart/admin.py

and REMOVE this:

from .models import User

Replace with:

from accounts.models import User

Your final ApnaCart/admin.py should be:

from django.contrib import admin
from accounts.models import User


admin.site.register(User)
Why This Happened

Because:

. means current app
current app = ApnaCart
but User is actually inside accounts

So Django could not find it.

Important Understanding
This is correct:
from accounts.models import User
This is wrong:
from ApnaCart.models import User

because User is NOT inside ApnaCart/models.py.

Now run again:

python manage.py makemigrations

then:

python manage.py migrate
lets create superuser, suggest suitable usernames 

For a professional multi-vendor e-commerce platform, choose a clean and production-style admin username.

Good options:

admin
superadmin
apnacart_admin
vyaapaar_admin
platform_admin
coreadmin
systemadmin
admin_srinjay
apnacart_superuser
rootadmin

My recommendation:

apnacart_admin

or

vyaapaar_admin

because they look professional and project-specific.

Now create superuser:

python manage.py createsuperuser

Example:

Username: apnacart_admin
Email: admin@gmail.com
Password:
Password (again):
Superuser created successfully.
next

Now we move to an extremely important setup step:

Configure Media Files (Image Uploads)

Without this:

profile images won’t display
product images won’t work
admin uploaded images won’t open
Step 1 — Add Media Settings

Open:

vyaapaar/settings.py

Add at bottom:

import os

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
What This Means
MEDIA_URL
MEDIA_URL = '/media/'

URL path for accessing uploaded files.

Example:

http://127.0.0.1:8000/media/products/shoe.jpg
MEDIA_ROOT
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

Physical folder where uploaded images are stored.

Django automatically creates:

media/

folder.

Step 2 — Configure URLs

Open:

vyaapaar/urls.py
Add Imports
from django.conf import settings
from django.conf.urls.static import static
Final urls.py
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
Why This Is Needed

During development:

Django does NOT serve media automatically
this configuration allows browser access to uploaded files
Step 3 — Run Server
python manage.py runserver
Step 4 — Test Image Upload

Go to:

http://127.0.0.1:8000/admin

Create:

seller user
category
product
upload product image

Then verify:

images upload correctly
images open correctly
Next Major Step

After media setup:

We start API development professionally.

Next We Build
Django REST Framework
JWT Authentication
User Registration API
Login API
Seller permissions
Product APIs

This is where the real backend engineering starts.

how to Create:

seller user
category
product
upload product image

Then verify:

images upload correctly
images open correctly
Step 1 — Start Server

Run:

python manage.py runserver

Open:

http://127.0.0.1:8000/admin

Login using your superuser credentials.

Step 2 — Create Seller User

Inside admin panel:

Go To
Users

Click:

+ Add
Fill Basic Details

Example:

Username: seller1
Password: seller123

Click:

Save
Now Additional Fields Appear

Set:

Role → seller

Optional:

phone number
profile image

Then click:

Save

Now seller user is created.

Step 3 — Create Category

Go to:

Categories

Click:

+ Add

Example:

Name: Electronics
Slug: electronics

Click:

Save
What is Slug?

Slug is URL-friendly text.

Example:

electronics
mens-shoes
mobile-covers

Used in URLs:

/products/electronics/
Step 4 — Create Product

Go to:

Products

Click:

+ Add

Fill:

Seller      → seller1
Category    → Electronics
Name        → iPhone 15
Slug        → iphone-15
Description → Apple smartphone
Price       → 85000
Stock       → 10
Is Available → checked

Click:

Save
Step 5 — Upload Product Image

Go to:

Product Images

Click:

+ Add

Fill:

Product → iPhone 15
Image   → Choose File

Select any image from your computer.

Click:

Save
Step 6 — Verify Images

Now click on uploaded image preview.

OR open browser:

http://127.0.0.1:8000/media/products/your_image_name.jpg

If image opens correctly → media setup is working perfectly.

What Should Happen Internally

Django automatically creates:

media/

Inside it:

media/products/

Your uploaded image gets stored there.

Example:

media/products/iphone.jpg
Important Observation

If image uploads successfully:

Pillow is working
MEDIA_ROOT is correct
MEDIA_URL is correct
ImageField is working
Admin integration is working

That means your project foundation is now solid.

Next Step (Real Backend Begins)

Now we should install:

Django REST Framework + JWT

Then build:

Register API
Login API
Token authentication
Protected routes
Seller-only product creation APIs

This is where the real e-commerce backend starts.

where to create "Step 3 — Create Category

Go to:

Categories

Click:

+ Add

Example:

Name: Electronics
Slug: electronics

Click:

Save
What is Slug?

Slug is URL-friendly text.

Example:

electronics
mens-shoes
mobile-covers

Used in URLs:

/products/electronics/
Step 4 — Create Product

Go to:

Products

Click:

+ Add

Fill:

Seller      → seller1
Category    → Electronics
Name        → iPhone 15
Slug        → iphone-15
Description → Apple smartphone
Price       → 85000
Stock       → 10
Is Available → checked

Click:

Save
Step 5 — Upload Product Image

Go to:

Product Images

Click:

+ Add

Fill:

Product → iPhone 15
Image   → Choose File

Select any image from your computer.

Click:

Save
Step 6 — Verify Images

Now click on uploaded image preview.

OR open browser:

http://127.0.0.1:8000/media/products/your_image_name.jpg

If image opens correctly → media setup is working perfectly."

Yes, it is correct and it will work.

from django.contrib import admin

# Register your models here.
from accounts.models import User
from .models import Category, Product, ProductImage


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)

But professionally, registering User inside products/admin.py is not a good practice.

Because:

User belongs to accounts app
Category/Product/ProductImage belong to products app

Each app should manage its own admin registrations.

Better Structure
accounts/admin.py
from django.contrib import admin
from .models import User


admin.site.register(User)
products/admin.py
from django.contrib import admin
from .models import Category, Product, ProductImage


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)

This is cleaner and industry-standard organization.

Now restart server:

python manage.py runserver

Refresh admin page.

You should now see:

ACCOUNTS
PRODUCTS

with all models visible.

next

Excellent. Now let’s build JWT Login properly.

What We Will Build

Using JWT:

Login API
Access Token
Refresh Token
Protected APIs
Step 1 — Add JWT URLs

Open:

accounts/urls.py

Update it:

from django.urls import path

from .views import RegisterView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),

    path('login/', TokenObtainPairView.as_view(), name='login'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
What These APIs Do
Login API
/api/accounts/login/

returns:

access token
refresh token
Refresh API
/api/accounts/token/refresh/

generates new access token using refresh token.

Step 2 — Run Server
python manage.py runserver
Step 3 — Test Login API
POST Request
POST http://127.0.0.1:8000/api/accounts/login/
JSON Body

Use registered user credentials:

{
    "username": "buyer1",
    "password": "buyer123"
}
Expected Response
{
    "refresh": "long_refresh_token",
    "access": "long_access_token"
}
VERY IMPORTANT UNDERSTANDING
Access Token

Short-lived token.

Used to access protected APIs.

Sent in headers:

Authorization: Bearer access_token
Refresh Token

Used to generate new access token after expiration.

More secure authentication flow.

Step 4 — Test Protected Route

Now we create a protected API to verify JWT works.

Create Profile API

Open:

accounts/views.py

Add:

from rest_framework.permissions import IsAuthenticated

Now add below RegisterView:

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = RegisterSerializer(request.user)

        return Response(serializer.data)
Update URLs

Open:

accounts/urls.py

Import:

from .views import RegisterView, ProfileView

Add:

path('profile/', ProfileView.as_view(), name='profile'),
Final URLs
urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),

    path('login/', TokenObtainPairView.as_view(), name='login'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profile/', ProfileView.as_view(), name='profile'),
]
Step 5 — Test Protected API
GET Request
GET http://127.0.0.1:8000/api/accounts/profile/

WITHOUT token:

You should get:

{
    "detail": "Authentication credentials were not provided."
}

GOOD — security works.

Step 6 — Add JWT Token

In Postman:

Headers
Authorization: Bearer your_access_token

Example:

Authorization: Bearer eyJhbGciOi...
Expected Response
{
    "username": "buyer1",
    "email": "buyer1@gmail.com",
    "role": "buyer",
    "phone_number": "9876543210"
}
HUGE MILESTONE

You now have:

custom user model
JWT authentication
protected APIs
registration system
login system
profile API

This is real backend engineering.

Next Best Step

Now we should build:

Product APIs

including:

create product
list products
product details
seller-only permissions
image uploads via API

That starts the actual e-commerce functionality.

lets build
lets test our all apis


Perfect. Testing APIs properly is a very important backend skill.

We will test everything step-by-step using:

Postman
Thunder Client
Insomnia

I’ll assume you are using Postman.

APIs We Will Test
Accounts APIs
Register User
Login User
Refresh Token
Profile API
Product APIs
List Products
Create Product
Product Details
IMPORTANT BEFORE TESTING

Start server:

python manage.py runserver

Base URL:

http://127.0.0.1:8000
1. Register API
Request
POST /api/accounts/register/

Full URL:

http://127.0.0.1:8000/api/accounts/register/
Body → raw → JSON
{
    "username": "seller1",
    "email": "seller1@gmail.com",
    "password": "seller123",
    "role": "seller",
    "phone_number": "9876543210"
}
Expected Response
{
    "message": "User registered successfully",
    "data": {
        "username": "seller1",
        "email": "seller1@gmail.com",
        "role": "seller",
        "phone_number": "9876543210"
    }
}
2. Login API
Request
POST /api/accounts/login/
Body
{
    "username": "seller1",
    "password": "seller123"
}
Expected Response
{
    "refresh": "jwt_refresh_token",
    "access": "jwt_access_token"
}
VERY IMPORTANT

Copy:

access token
refresh token

We will use access token in headers.

3. Profile API
Request
GET /api/accounts/profile/
Headers
Authorization : Bearer your_access_token

Example:

Authorization : Bearer eyJhbGc...
Expected Response
{
    "username": "seller1",
    "email": "seller1@gmail.com",
    "role": "seller",
    "phone_number": "9876543210"
}
4. Refresh Token API
Request
POST /api/accounts/token/refresh/
Body
{
    "refresh": "your_refresh_token"
}
Expected Response
{
    "access": "new_access_token"
}
5. Product List API
Request
GET /api/products/
Expected Response

Initially maybe:

[]

or list of products.

6. Create Product API

IMPORTANT:
Use SELLER token.

Request
POST /api/products/
Headers
Authorization : Bearer your_access_token
Body
{
    "category": 1,
    "name": "iPhone 15",
    "slug": "iphone-15",
    "description": "Apple smartphone",
    "price": "85000",
    "stock": 10,
    "is_available": true
}
Expected Response
{
    "id": 1,
    "seller": "seller1",
    "category": 1,
    "name": "iPhone 15",
    "slug": "iphone-15",
    "description": "Apple smartphone",
    "price": "85000.00",
    "stock": 10,
    "is_available": true,
    "images": [],
    "created_at": "..."
}
7. Product Detail API
Request
GET /api/products/1/
Expected Response

Single product details.

IMPORTANT ERROR CASES TO TEST
Buyer Trying To Create Product

Register buyer:

{
    "username": "buyer1",
    "email": "buyer1@gmail.com",
    "password": "buyer123",
    "role": "buyer"
}

Login as buyer.

Try:

POST /api/products/

Should FAIL.

This confirms seller permissions work correctly.

Common Errors
401 Unauthorized

Means:

token missing
token invalid
token expired
403 Forbidden

Means:

authenticated
but lacks permission
400 Bad Request

Means:

invalid data
serializer validation failed
HUGE MILESTONE

If all these APIs work:

authentication system works
JWT works
permissions work
DRF works
product APIs work
role system works

You now officially have a professional backend foundation.

Next Best Step

After testing:
we should build:

Product Image Upload API

with:

multipart/form-data
image validation
multiple image uploads
seller ownership checks

This is a very important real-world backend skill.

should i wright bearer with access token in header

Yes. You must write:

Bearer <your_access_token>

inside the Authorization header.

Example:

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
In Postman

Go to:

Headers

Add:

Key	Value
Authorization	Bearer your_access_token
VERY IMPORTANT

There must be:

a space after Bearer
no quotes
no commas

Correct:

Bearer eyJhbGciOi...

Wrong:

BearereyJhbGciOi...

Wrong:

"Bearer eyJhbGciOi..."
Why Bearer?

JWT authentication expects:

Authorization: Bearer <token>

This is the industry-standard authentication format used by:

Django REST Framework
Node.js APIs
Spring Boot
FastAPI
Express.js
most modern APIs.
in authorization what should we write in auth type and token
check my header in postman

After getting the new access token, you use it to access protected APIs.

You do NOT send access token in Body → raw → JSON.

You send it in:

Authorization tab
OR
Headers
Example

Suppose refresh API returned:

{
    "access": "new_access_token_here"
}

Copy that token.

Now Test Protected API

Example:

GET http://127.0.0.1:8000/api/accounts/profile/
In Postman
Authorization Tab

Select:

Bearer Token

Paste:

new_access_token_here

inside Token field.

Body?

For profile API:

no body needed
leave Body empty

Because:

it is a GET request
Summary
Login API
POST

Body → raw → JSON

{
    "username": "seller1",
    "password": "seller123"
}

returns:

access token
refresh token
Refresh API
POST

Body → raw → JSON

{
    "refresh": "your_refresh_token"
}

returns:

new access token
Protected APIs

Example:

profile API
create product API

Use:

Authorization → Bearer Token
paste access token

No need to put token in body.

Example Protected API
GET
http://127.0.0.1:8000/api/accounts/profile/

Authorization:

Bearer Token
paste access token

Body:

empty

Then click:

Send

You should get user details.

i can see the user detail

Excellent. That means:

✅ JWT authentication works
✅ Access token works
✅ Protected API works
✅ Your custom user model works
✅ DRF configuration works
✅ Authorization headers work

You now officially have a working authentication backend.

Next Important Test

Now test:

Product Creation API

This verifies:

seller permissions
authenticated product creation
serializer functionality
database integration
Request
POST
http://127.0.0.1:8000/api/products/
Authorization

Use:

Bearer Token

Paste your seller access token.

Body

Go to:

Body → raw → JSON

Paste:

{
    "category": 1,
    "name": "iPhone 15",
    "slug": "iphone-15",
    "description": "Apple smartphone",
    "price": "85000",
    "stock": 10,
    "is_available": true
}
Expected Result

You should get:

{
    "id": 1,
    "seller": "seller1",
    "category": 1,
    "name": "iPhone 15",
    "slug": "iphone-15",
    "description": "Apple smartphone",
    "price": "85000.00",
    "stock": 10,
    "is_available": true,
    "images": [],
    "created_at": "..."
}
Then Test Product List API
GET
http://127.0.0.1:8000/api/products/

No body needed.

You should see your created products.

Then Test Product Detail API
GET
http://127.0.0.1:8000/api/products/1/

You should see single product details.

Important Real-World Test

Login as:

buyer user

Then try:

POST /api/products/

It should fail.

That confirms your role-based access control works properly.

now every thing is working
this is what i can see in razorpay settings - api keys ,""

Great. Now we will build:

# 🔥 Razorpay Payment Integration

We will start with:

Step 1 — Payment Model : orders/models.py

This stores:

Razorpay order id
payment id
payment status
amount
linked ecommerce order

Step 2 — Make Migrations
Run: python manage.py makemigrations, python manage.py migrate

Step 3 — Create Payment Serializer : orders/serializers.py
Step 4 — Create Razorpay Client : orders/views.py
Step 5 — Create Razorpay Client Object
Step 6 — Create Payment API
Step 7 — Add URL : orders/urls.py
Step 8 — Run Server
Step 9 — Test Payment API : POST : http://127.0.0.1:8000/api/orders/payment/1/
buyer token 

# 🔥 Payment Verification API

Step 1 — Update Order Model : orders/models.py
Step 2 — Migrations
Step 3 — Create Verification API : orders/views.py
Step 4 — Import APIView
Step 5 — Add URL : orders/urls.py

# Invoice PDF Generation

Step 1 — Install ReportLab
Run:

pip install reportlab
Step 2 — Create Invoice View

Open:

orders/views.py

Add imports:

from django.http import HttpResponse

from reportlab.pdfgen import canvas
Step 3 — Create Invoice API
Step 4 — Add URL : orders/urls.py
Step 5 — Run Server
Step 6 — Test Invoice API:GET:http://127.0.0.1:8000/api/orders/invoice/2/

# 🔥 Email Notifications System

Real ecommerce platforms send emails for:

order placed
payment success
shipping updates
invoice delivery

This is a core production feature.

Step 1 — Configure Email Settings
You already added SMTP settings in .env.

Step 2 — Enable App Password

Step 3 — Update .env

Step 4 — settings.py

Step 5 — Import Mail Function : orders/views.py

Step 6 — Send Email After Order Placement

Step 7 — Test
Place New Order

Create Test Email API (BEST FOR TESTING)

Step 1 — Create Test View : orders/views.py
Step 2 — Add URL : orders/urls.py
Step 3 — Test API

# Dockerization
Step 1 — Install Docker Desktop
Step 2 — Verify Docker : docker --version
Step 3 — Create Dockerfile
    step 1 open docker desktop
    step 2 Verify Docker Works : docker --version followed by docker ps
    If working correctly, you should see:
CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES

Step 4 — Create requirements.txt
Step 5 — Create .dockerignore where manage.py is there
Step 6 — Build Docker Image : docker build -t apnacart . 
Step 7 — Run Container : docker run -p 8000:8000 apnacart
Step 8 — Open Browser

If Docker Desktop Does Not Start
then,
Step 1 — Open Docker Desktop
Step 2 — Enable WSL Integration
    Inside Docker Desktop: Settings → Resources → WSL Integration
    Enable:Ubuntu
    Enable integration with my default WSL distro
    Click : Apply & Restart
Step 6 — Build Docker Image : docker build -t apnacart . 
You should eventually see:Successfully tagged apnacart:latest   
step 7  Then Run Container :  docker run -p 8000:8000 apnacart

That means:
Django started successfully inside Docker
container is working
project files copied correctly
dependencies installed correctly

for  26 unapplied migrations run : docker run -p 8000:8000 apnacart python manage.py migrate

Each docker run creates a NEW temporary container
So:
migrations were applied in one temporary container
then another fresh container started again
SQLite database inside container got recreated

Proper Fix (Recommended)
Step 1 — Stop Container : CTRL + C
Step 2 — Run Container With Volume Mount
       docker run -p 8000:8000 -v ${PWD}:/app apnacart
       This mounts your local project folder into container.

IMPORTANT:keep this terminal running. do NOT close it   
Step 3 — Open NEW Terminal  -> run :  docker ps 
step 4 - Copy:CONTAINER ID
Step 5 — Apply Migrations Inside Running Container
         in new terminal only and keep old terminal running
         docker exec -it CONTAINER_ID python manage.py migrate
    i.e  docker exec -it 127f96039417 python manage.py migrate

# 🔥 PostgreSQL + Docker Compose    

Step 1 — Create docker-compose.yml
At same level as:manage.py
Step 2 — Update settings.py
Replace SQLite section:
Step 3 — Install PostgreSQL Driver : pip install psycopg2-binary
pip freeze > requirements.txt
Step 4 — Stop Old Containers -> docker ps -> docker stop CONTAINER_ID
Step 5 — Build Compose Containers : docker-compose build
Step 6 — Start Containers : docker-compose up
Step 7 — Apply Migrations -> Open NEW terminal : docker-compose exec web python manage.py migrate
Step 8 — Create Superuser Again Because PostgreSQL is fresh DB.

VERY IMPORTANT
Keep current docker-compose up terminal running.
Run migration command in:
another terminal
This is standard Docker Compose workflow

# 🔥 Redis + Celery
Why Celery?
Right now:
emails are sent synchronously
invoice generation happens inside request
heavy tasks block API response

Example

Without Celery:

User places order
→ waits for email
→ waits for invoice
→ API responds slowly

With Celery:

User places order
→ API responds instantly
→ background worker sends email
→ background worker generates invoice

This is how real ecommerce systems work.

Architecture We Will Build
Django
   +
PostgreSQL
   +
Redis
   +
Celery Worker

What Is Redis?

Redis is:ultra-fast in-memory datastore
used as: cache, message broker, queue system

Celery uses Redis to: store background tasks

What You Will Learn

✅ Asynchronous processing
✅ Background workers
✅ Task queues
✅ Production scalability
✅ Distributed architecture

Step 1 — Install Packages : pip install celery redis
pip freeze > requirements.txt

Step 2 — Update docker-compose.yml
Add Redis service:

Step 3 — Add Celery Worker Service
Inside docker-compose.yml:

Step 4 — Create vyaapaar/celery.py
Create:vyaapaar/celery.py 

Step 5 — Update __init__.py : vyaapaar/__init__.py

Step 6 — Add Redis Settings

Step 7 — Create Task File : orders/tasks.py

Step 8 — Use Celery Task ; Inside PlaceOrderView

Step 9 — Build Containers Again :
run:
docker-compose build
docker-compose up

HUGE ACHIEVEMENT
At this stage you are learning:
distributed backend architecture

now built template based frontend

after updating the model

Run
python manage.py makemigrations
python manage.py migrate

OR with Docker:

docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate


Flow:

Add Product
 ↓
Add To Cart
 ↓
Checkout
 ↓
Payment Page
 ↓
Razorpay Popup
 ↓
Success

# deployment
in settings, add

1. ALLOWED_HOSTS = ['*']

2. STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

3. pip install whitenoise gunicorn
pip freeze > requirements.txt

4. MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware']

5. STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

at the same level as manage.py
6. at project root, create Procfile and add
web: gunicorn vyaapaar.wsgi

7 create runtime.txt file and add
python-3.12.13

8. collect static : docker exec -it vyaapaar-web-1 python manage.py collectstatic

9. enviromnet variable

planning to deploy:
Only Django website + PostgreSQL

push your project to git

then open render
GitHub → Settings → Applications → Installed GitHub Apps → Render


