class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get('cart', {})

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def items(self):
        from .models import Product
        products = Product.objects.filter(id__in=self.cart.keys())
        return [
            {
                'product': product,
                'quantity': self.cart[str(product.id)],
                'total': product.price * self.cart[str(product.id)],
            }
            for product in products
        ]

    def total_price(self):
        return sum(item['total'] for item in self.items())
