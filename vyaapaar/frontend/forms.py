from django import forms

from django.contrib.auth.forms import UserCreationForm

from accounts.models import User

from products.models import Product, ProductImage,  Review

class CustomUserCreationForm(UserCreationForm):

    class Meta:

        model = User

        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )


class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = [

            'category',

            'name',

            'description',

            'price',

            'stock'
        ]


class ProductImageForm(forms.ModelForm):

    class Meta:

        model = ProductImage

        fields = ['image']        


class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        fields = [
            'rating',
            'comment'
        ]