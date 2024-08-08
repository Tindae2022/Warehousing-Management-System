import uuid

from django.conf import settings
from django.db import models
from accounts.models import User
from django.contrib.auth import get_user_model



user = get_user_model()

# Create your models here.


DELIVERY_STATUS = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
)
ORDER_STATUS = [
    ('Pending', 'Pending'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
]


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['name']


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
        ordering = ['name']


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
        ordering = ['name']


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    barcode = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    quantity_available = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    packed_weight = models.DecimalField(max_digits=10, decimal_places=2)
    packed_height = models.DecimalField(max_digits=10, decimal_places=2)
    packed_width = models.DecimalField(max_digits=10, decimal_places=2)
    refrigerated = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return f'{self.code} - {self.name}'

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = str(uuid.uuid4().hex[:12].upper())  # Generate a 12-character barcode
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['barcode']),
        ]


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    is_refrigerated = models.BooleanField(default=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'
        ordering = ['name']


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.address}'

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        ordering = ['name']


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity_available = models.IntegerField()
    minimum_stock_level = models.IntegerField()
    maximum_stock_level = models.IntegerField()
    reorder_point = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    average_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.quantity_available = self.product.quantity_available
        self.check_quantity_and_notify()


    def __str__(self):
        return f'{self.product.name} - {self.warehouse.name}'

    def check_quantity_and_notify(self):
        if self.quantity_available < 0.4 * self.quantity_available:
            self.create_notification()

    def create_notification(self):
        managers = User.objects.filter(user_type__in=[User.WAREHOUSE_MANAGER, User.SALES_MANAGER])
        for manager in managers:
            Notification.objects.create(
                user=manager,
                message=f'The inventory for {self.product.name} is below 40% of the maximum stock level.'
            )

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'
        ordering = ['product__name']
        indexes = [
            models.Index(fields=['product', 'warehouse']),
        ]



class Order(models.Model):
    provider = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField()
    status = models.CharField(max_length=25, choices=ORDER_STATUS, default='Pending')
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            # Generate a unique code using UUID or another method
            self.code = str(uuid.uuid4().hex[:8].upper())

        super().save(*args, **kwargs)
        self.reduce_product_quantity()

    def reduce_product_quantity(self):
        for item in self.orderitem_set.all():
            product = item.product
            product.quantity_available -= item.quantity
            product.save()

    def __str__(self):
        return f'{self.customer.first_name} {self.customer.last_name} - {self.order_date}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-order_date']

    def get_total_cost(self):
        return sum(item.total_price for item in self.orderitem_set.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.product:
            self.product.quantity_available -= self.quantity
            self.product.save()

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        ordering = ['product__name']

    @property
    def total_price(self):
        if self.product:
            return self.quantity * self.product.unit_price
        return 0


""" 
 def update_inventory(self):
      inventory = Inventory.objects.get(product=self.product)
      inventory.quantity_available = self.product.quantity_available
      inventory.save()

      """


class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sales_date = models.DateField()
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS, default='pending')

    def __str__(self):
        return f'Delivery on {self.sales_date} - {self.status}'

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
        ordering = ['-sales_date']


class DeliveryDetails(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    expected_date = models.DateField()

    def __str__(self):
        return f'{self.product.name} ({self.quantity}) - Expected on {self.expected_date}'

    class Meta:
        verbose_name = 'Delivery Detail'
        verbose_name_plural = 'Delivery Details'
        ordering = ['expected_date']


class Transfer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    from_warehouse = models.ForeignKey(Warehouse, related_name='transfers_sent', on_delete=models.CASCADE)
    to_warehouse = models.ForeignKey(Warehouse, related_name='transfers_received', on_delete=models.CASCADE)
    transfer_quantity = models.IntegerField()
    sent_date = models.DateField()
    received_date = models.DateField(null=True, blank=True)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    shipping_company = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'Transfer {self.product.name} from {self.from_warehouse.name} to {self.to_warehouse.name}'

    class Meta:
        verbose_name = 'Transfer'
        verbose_name_plural = 'Transfers'
        ordering = ['-sent_date']

    @property
    def total_price(self):
        if self.product:
            return self.transfer_quantity * self.product.unit_price
        return 0


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('ORDER', 'Order'),
        ('MESSAGE', 'Message'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    conversation = models.ForeignKey('chat.Conversation', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message