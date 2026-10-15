from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['id']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    is_pack = models.BooleanField(default=False)
    bundle_items = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='in_packs')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_available(self):
        return self.stock > 0

    def __str__(self):
        return self.name


class Wilaya(models.Model):
    code = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Commune(models.Model):
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, related_name='communes')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        FIRST_CALL = 'first_call', '1st Call'
        STOP_DESK = 'stop_desk', 'Stop Desk'
        RETURNED = 'returned', 'Returned'
        CONFIRMED = 'confirmed', 'Confirmed'

    class Shipping(models.TextChoices):
        HOME = 'home', 'To Home'
        STOP_DESK = 'stopdesk', 'To Stop Desk'

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True)
    commune = models.CharField(max_length=100)
    shipping_method = models.CharField(max_length=20, choices=Shipping.choices, default=Shipping.HOME)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)   # price/name snapshot
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"