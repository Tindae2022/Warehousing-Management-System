from django import forms
from .models import (Product, ProductCategory, Supplier, Warehouse, Order, OrderItem, Delivery,
                     DeliveryDetails, Location, Transfer, Inventory)
from django.forms.models import inlineformset_factory
from datetime import date



class ProductCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)

        self.fields['category'].label = 'Category'
        self.fields['code'].label = 'Code'

        self.fields['name'].label = 'Name'
        self.fields['description'].label = 'Description'
        self.fields['quantity_available'].label = 'Quantity Available'
        self.fields['unit_price'].label = 'Unit Price'
        self.fields['packed_weight'].label = 'Packed Weight'
        self.fields['packed_height'].label = 'Packed Weight'
        self.fields['refrigerated'].label = 'Refrigerated'
        self.fields['image'].label = 'Image'

    class Meta:
        model = Product
        fields = '__all__'

    def save(self, commit=True):
        product_form = super(ProductCreateForm, self).save(commit=False)
        if commit:
            product_form.save()
            return product_form


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'category': 'Category',
            'code': 'Code',

            'name': 'Name',
            'description': 'Description',
            'quantity_available': 'Quantity Available',
            'unit_price': 'Unit Price',
            'packed_weight': 'Packed Weight',
            'packed_height': 'Packed Height',
            'packed_width': 'Packed Width',
            'refrigerated': 'Refrigerated',

        }

    def save(self, commit=True):
        product = super(ProductUpdateForm, self).save(commit=False)
        if commit:
            product.save()
        return product
class ProductCategoryCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductCategoryCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Name'

    class Meta:
        model = ProductCategory
        fields = '__all__'

    def save(self, commit=True):
        product_category_form = super(ProductCategoryCreateForm, self).save(commit=False)
        if commit:
            product_category_form.save()
            return product_category_form


class ProductCategoryUpdateForm(forms.ModelForm):

    class Meta:
        model = ProductCategory
        fields = '__all__'
        labels = {

            'name': 'Name',

        }

    def save(self, commit=True):
        product_category = super(ProductCategoryUpdateForm, self).save(commit=False)
        if commit:
            product_category.save()
        return product_category

class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = '__all__'
        labels = {

            'name': 'Name',
            'address': 'Address'

        }

    def save(self, commit=True):
        supplier = super(SupplierForm, self).save(commit=False)
        if commit:
            supplier.save()
        return supplier


class SupplierUpdateForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        labels = {

            'name': 'Name',
            'address': 'Address'

        }

    def save(self, commit=True):
        supplier = super(SupplierUpdateForm, self).save(commit=False)
        if commit:
            supplier.save()
        return supplier


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'
        labels = {
            'name': 'Name',
            'is_refrigerated': 'Is Refrigerated',
            'location': 'Location'
        }

    def save(self, commit = True):
        warehouse = super(WarehouseForm, self).save(commit=False)
        if commit:
            warehouse.save()
        return warehouse


class WarehouseUpdateForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'
        labels = {
            'name': 'Name',
            'is_refrigerated': 'Is Refrigerated',
            'location': 'Location'
        }

    def save(self, commit=True):
        warehouse = super(WarehouseUpdateForm, self).save(commit=False)
        if commit:
            warehouse.save()

        return warehouse




class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['provider', 'customer', 'order_date', 'status']

OrderItemFormSet = inlineformset_factory(Order, OrderItem, fields=['product', 'quantity'], extra=1)

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['provider', 'customer', 'order_date', 'status']

OrderItemUpdateFormSet = inlineformset_factory(Order, OrderItem, fields=['product', 'quantity'], extra=1)

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['order', 'sales_date', 'status']
        labels = {
            'order': 'Order',
            'sales_date': 'Sales Date',
            'status': 'Status'
        }

    def save(self, commit=True):
        delivery = super(DeliveryForm, self).save(commit=False)
        if commit:
            delivery.save()
        return delivery

# Inline formset for DeliveryDetails
DeliveryDetailsFormSet = inlineformset_factory(
    Delivery, DeliveryDetails, fields=['product', 'quantity', 'expected_date'], extra=1
)

class DeliveryUpdateForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['order', 'sales_date', 'status']
        labels = {
            'order': 'Order',
            'sales_date': 'Sales Date',
            'status': 'Status'
        }

    def save(self, commit=True):
        delivery = super(DeliveryUpdateForm, self).save(commit=False)
        if commit:
            delivery.save()
        return delivery

# Inline formset for DeliveryDetails
DeliveryDetailsUpdateFormSet = inlineformset_factory(
    Delivery, DeliveryDetails, fields=['product', 'quantity', 'expected_date'], extra=1
)

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address']
        labels = {
            'name': 'Name',
            'address': 'Address',

        }

    def save(self, commit=True):
        location = super(LocationForm, self).save(commit=False)
        if commit:
            location.save()
        return location
class LocationUpdateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address']
        labels = {
            'name': 'Name',
            'address': 'Address',

        }

    def save(self, commit=True):
        location = super(LocationUpdateForm, self).save(commit=False)
        if commit:
            location.save()
        return location

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['product', 'from_warehouse', 'to_warehouse', 'transfer_quantity', 'sent_date', 'received_date', 'tracking_number']
        labels = {
            'product': 'Product',
            'from_warehouse': 'Current Warehouse',
            'to_warehouse': 'To',
            'transfer_quantity': 'Quantity',
            'sent_date': 'Sent Date',
            'received_date': 'Received Date',
            'tracking_number': 'Tracking Number',

        }

    def save(self, commit=True):
        transfer = super(TransferForm, self).save(commit=False)
        if commit:
            transfer.save()
        return transfer


class TransferUpdateForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['product', 'from_warehouse', 'to_warehouse', 'transfer_quantity', 'sent_date', 'received_date', 'tracking_number']
        labels = {
            'product': 'Product',
            'from_warehouse': 'Current Warehouse',
            'to_warehouse': 'To',
            'transfer_quantity': 'Quantity',
            'sent_date': 'Sent Date',
            'received_date': 'Received Date',
            'tracking_number': 'Tracking Number',

        }

    def save(self, commit=True):
        transfer = super(TransferUpdateForm, self).save(commit=False)
        if commit:
            transfer.save()
        return transfer


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'warehouse', 'minimum_stock_level', 'maximum_stock_level',
                  'reorder_point', 'average_cost']
        labels = {
            'product': 'Product',
            'warehouse': 'Warehouse',
            'minimum_stock_level': 'Minimum Stock Level',
            'maximum_stock_level': 'Maximum Stock Level',
            'reorder_point': 'Reorder Point',
            'average_cost': 'Average Cost',
        }

    def save(self, commit=True):
        inventory = super(InventoryForm, self).save(commit=False)
        if commit:
            inventory.save()
        return inventory


class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'warehouse', 'minimum_stock_level', 'maximum_stock_level',
                  'reorder_point', 'average_cost']
        labels = {
            'product': 'Product',
            'warehouse': 'Warehouse',
            'minimum_stock_level': 'Minimum Stock Level',
            'maximum_stock_level': 'Maximum Stock Level',
            'reorder_point': 'Reorder Point',
            'average_cost': 'Average Cost',
        }

    def save(self, commit=True):
        inventory = super(InventoryUpdateForm, self).save(commit=False)
        if commit:
            inventory.save()
        return inventory



class CustomerOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_date']
        widgets = {
            'order_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['order_date'].initial = date.today()




def generate_product_description(data):
    prompt = (
        f"Generate a detailed description for a product with the following details:\n"
        f"Name: {data['name']}\n"
        f"Category: {data['category']}\n"
        f"Code: {data['code']}\n"
        f"Quantity Available: {data['quantity_available']}\n"
        f"Unit Price: {data['unit_price']}\n"
        f"Packed Weight: {data['packed_weight']}\n"
        f"Packed Height: {data['packed_height']}\n"
        f"Packed Width: {data['packed_width']}\n"
        f"Refrigerated: {'Yes' if data['refrigerated'] else 'No'}\n"
        f"Generate a detailed and engaging description based on the above information."
    )

    # Assuming `model` is the AI model instance you are using
    response = model.generate_content(prompt)
    description = getattr(response, 'text', None)
    html = markdown.markdown(description)
    plain_text = BeautifulSoup(html, "html.parser").text
    print("Generated description (plain text):", plain_text)
    return plain_text
