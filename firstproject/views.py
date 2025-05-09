from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Tag,Order, OrderItem
from .forms import *
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from .cart import Cart
import uuid
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import ( ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.views import View
from django.contrib import messages

def custom_permission_denied_view(request, exception=None):
    context = {}
    return render(request, '403.html', context=context, status=403)

#ПРОДУКТЫ + КАТАЛОГ
@method_decorator(login_required, name='dispatch')
class ProductListView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'pages/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_deleted=False)

@method_decorator(login_required, name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    pk_url_kwarg = 'id'
    template_name = 'pages/product_detail.html'
    context_object_name = 'product'

@method_decorator(permission_required('firstproject.add_product', raise_exception=True), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'pages/add_product.html'
    success_url = reverse_lazy('catalog')

@method_decorator(permission_required('firstproject.change_product', raise_exception=True), name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    pk_url_kwarg = 'id'
    form_class = ProductForm
    template_name = 'pages/add_product.html'
    success_url = reverse_lazy('catalog')

@method_decorator(permission_required('firstproject.change_product', raise_exception=True), name='dispatch')
class ProductManageListView(ListView):
    model = Product
    template_name = 'pages/products_manage.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()

@method_decorator(permission_required('firstproject.delete_product', raise_exception=True), name='dispatch')
class ProductLogicalDeleteView(View):
    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        if product.is_deleted:
            messages.info(request, 'Товар уже помечен как удалён.')
        else:
            product.is_deleted = True
            product.save()
            messages.success(request, f'Товар "{product.name}" удалён логически.')
        return redirect('product_manage')

@method_decorator(permission_required('firstproject.delete_product_physical', raise_exception=True), name='dispatch')
class ProductPhysicalDeleteView(DeleteView):
    model = Product
    pk_url_kwarg = 'id'
    template_name = 'pages/product_confirm_delete.html'
    success_url = reverse_lazy('product_manage')
    
@method_decorator(permission_required('firstproject.restore_product', raise_exception=True), name='dispatch')
class ProductRestoreView(View):
    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        if not product.is_deleted:
            messages.info(request, 'Товар уже активен.')
        else:
            product.is_deleted = False
            product.save()
            messages.success(request, f'Товар "{product.name}" восстановлен.')
        return redirect('product_manage')

# КАТЕГОРИИ
@method_decorator(login_required, name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'pages/category_list.html'
    context_object_name = 'categories'

@method_decorator(login_required, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category
    pk_url_kwarg = 'category_id'
    template_name = 'pages/category_products.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(
            category=self.object,
            is_deleted=False
        )
        return context

@method_decorator(permission_required('firstproject.add_category', raise_exception=True), name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'pages/add_category.html'
    success_url = reverse_lazy('category_list')

@method_decorator(permission_required('firstproject.change_category', raise_exception=True), name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    pk_url_kwarg = 'category_id'
    form_class = CategoryForm
    template_name = 'pages/add_category.html'
    success_url = reverse_lazy('category_list')

@method_decorator(permission_required('firstproject.delete_category', raise_exception=True), name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    pk_url_kwarg = 'category_id'
    template_name = 'pages/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')


# ТЕГИ
@method_decorator(login_required, name='dispatch')
class TagListView(ListView):
    model = Tag
    template_name = 'pages/tag_list.html'
    context_object_name = 'tags'

@method_decorator(login_required, name='dispatch')
class TagDetailView(DetailView):
    model = Tag
    pk_url_kwarg = 'tag_id'
    template_name = 'pages/tag_products.html'
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(
            tags=self.object,
            is_deleted=False
        )
        return context

@method_decorator(permission_required('firstproject.add_tag', raise_exception=True), name='dispatch')
class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'pages/add_tag.html'
    success_url = reverse_lazy('tag_list')

@method_decorator(permission_required('firstproject.change_tag', raise_exception=True), name='dispatch')
class TagUpdateView(UpdateView):
    model = Tag
    pk_url_kwarg = 'tag_id'
    form_class = TagForm
    template_name = 'pages/add_tag.html'
    success_url = reverse_lazy('tag_list')

@method_decorator(permission_required('firstproject.delete_tag', raise_exception=True), name='dispatch')
class TagDeleteView(DeleteView):
    model = Tag
    pk_url_kwarg = 'tag_id'
    template_name = 'pages/tag_confirm_delete.html'
    success_url = reverse_lazy('tag_list')


#КОРЗИНА + ЗАКАЗЫ
@login_required
def cart(request):
    cart = Cart(request)
    return render(request, 'pages/cart.html', {
        'cart_items': cart.items(),
        'total_price': cart.total_price(),
    })

@login_required
def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart')

@login_required
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart')

@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        full_name = request.POST['full_name']
        phone = request.POST['phone']
        address = request.POST['delivery_address']
        
        order = Order.objects.create(
            user=request.user,
            number=uuid.uuid4().hex[:8].upper(),
            full_name=full_name,
            phone=phone,
            delivery_address=address
        )

        for item in cart.items():
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                discount=0
            )
        cart.clear()
        return redirect('order_list')

    return render(request, 'pages/checkout.html', {
        'cart_items': cart.items(),
        'total_price': cart.total_price(),
    })

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'pages/order_list.html', {'orders': orders})


# СЕССИИ
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('catalog')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def registration_user(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            login(request,form.save())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('catalog')
    else:
        form = RegistrationForm()
    return render(request, 'auth/registration.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('catalog')