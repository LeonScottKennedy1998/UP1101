from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from firstproject.models import Product, Category, Tag, Order, OrderItem

class Command(BaseCommand):

    def handle(self, *args, **options):
        User.objects.all().delete()
        Group.objects.filter(name__in=['Superuser','Seller','Administrator','Buyer']).delete()

        super_g = Group.objects.create(name='Superuser')
        seller_g = Group.objects.create(name='Seller')
        admin_g = Group.objects.create(name='Administrator')
        buyer_g = Group.objects.create(name='Buyer')

        su = User.objects.create_superuser('superuser', 'su@example.com', 'superpass')
        su.groups.add(super_g)

        perms_seller = Permission.objects.filter(
            content_type__app_label='firstproject',
            codename__in=['add_product','change_product','delete_product','restore_product',]
        )
        for p in perms_seller: seller_g.permissions.add(p)

        perms_admin = Permission.objects.filter(
        content_type__app_label='firstproject',
        codename__in=[
            'add_product', 'change_product', 'delete_product',
            'delete_product_physical', 'restore_product',
            'add_category', 'change_category', 'delete_category',
            'add_tag', 'change_tag', 'delete_tag'
            ]
        )
        for p in perms_admin: admin_g.permissions.add(p)


        perms_buyer = Permission.objects.filter(
            content_type__app_label='firstproject',
            codename__startswith='view_'
        )
        for p in perms_buyer: buyer_g.permissions.add(p)

        for i in range(1,4):
            u = User.objects.create_user(f'seller{i}', f'seller{i}@ex.com', 'sellerpass')
            u.is_staff = True
            u.save()
            u.groups.add(seller_g)

        for i in range(1,3):
            u = User.objects.create_user(f'admin{i}', f'admin{i}@ex.com', 'adminpass')
            u.is_staff = True
            u.save()
            u.groups.add(admin_g)

        for i in range(1,5):
            u = User.objects.create_user(f'buyer{i}', f'buyer{i}@ex.com', 'buyerpass')
            u.save()
            u.groups.add(buyer_g)

        self.stdout.write(self.style.SUCCESS('Успешно создано 10 пользователей.'))
