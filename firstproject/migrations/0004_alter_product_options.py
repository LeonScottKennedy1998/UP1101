# Generated by Django 5.2 on 2025-05-09 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstproject', '0003_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('delete_product_physical', 'Может физически удалять товар'), ('restore_product', 'Can restore deleted product')]},
        ),
    ]
