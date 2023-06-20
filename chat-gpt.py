from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, editable=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    quantity_available = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def __str__(self):
        return self.name

    def reduce_quantity(self, quantity):
        if self.quantity_available >= quantity:
            self.quantity_available -= quantity
            self.save()
            return True
        return False


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user.username if self.user else self.session.session_key}"

    def get_total_price(self):
        total_price = self.cart_items.aggregate(total=models.Sum(models.F('quantity') * models.F('product__price')))['total']
        return total_price or 0

    def add_to_cart(self, product, quantity=1):
        if self.user:
            cart_item, created = self.cart_items.get_or_create(product=product)
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item, created = self.cart_items.get_or_create(product=product, session=self.session)
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

    def remove_from_cart(self, product):
        if self.user:
            self.cart_items.filter(product=product).delete()
        else:
            self.cart_items.filter(product=product, session=self.session).delete()

    def clear_cart(self):
        if self.user:
            self.cart_items.all().delete()
        else:
            self.cart_items.filter(session=self.session).delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)

    def get_item_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    created = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def get_total_price(self):
        total_price = self.items.aggregate(total=models.Sum(models.F('quantity') * models.F('product__price')))['total']
        return total_price or 0

    def complete_order(self):
        if not self.is_completed:
            with models.Model._meta.db_table_class.objects.select_for_update().filter(pk=self.pk):
                self.refresh_from_db()
                if self.is_completed:
                    return False
                for item in self.items.all():
                    if item.product.reduce_quantity(item.quantity):
                        item.save()
                    else:
                        return False
                self.is_completed = True
                self.save()
                return True
        return False

    def __str__(self):
        return f"Order - {self.user.username}"
