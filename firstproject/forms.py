from django import forms
from .models import Product, Tag, Category
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'Название товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-field',
                'rows': 4,
                'placeholder': 'Описание товара'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-field',
                'step': '0.01'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-field'
            }),
            'category': forms.Select(attrs={
                'class': 'form-field'
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'checkbox-group'
            }),
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-field', 'placeholder': 'Название тега'}),
            'description': forms.Textarea(attrs={'class': 'form-field', 'rows': 3, 'placeholder': 'Описание тега'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-field',
                'placeholder': 'Название категории'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-field',
                'rows': 3,
                'placeholder': 'Описание категории'
            }),
        }

class RegistrationForm(UserCreationForm):
    username= forms.CharField(
        label="Логин пользователя",
        widget=forms.TextInput(attrs={'class': 'form-field',}),
        min_length=2
    )
    email= forms.CharField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={'class': 'form-field',}),
    )
    password1= forms.CharField(
        label="Придумайте пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-field',}),
    )
    password2= forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-field',}),
    )

    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username= forms.CharField(
        label="Логин пользователя",
        widget=forms.TextInput(attrs={'class': 'form-field',}),
        min_length=2
    )
    password= forms.CharField(
        label="Ваш пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-field',}),
    )