from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy

from django.views.generic import (TemplateView, ListView, CreateView, DetailView,

                                  UpdateView, DeleteView, RedirectView)

from core.models import (Product, DeliveryDetails, Order, Inventory,
                         Delivery, Supplier,
                         ProductCategory, Warehouse, Location, Transfer, OrderItem, Notification)

from django.db.models import Sum, F, Count, Avg

from core.mixins import (WarehouseManagerRequiredMixin, SalesManagerRequiredMixins,
                         CombinedManagerRequiredMixin)

from core.forms import ( ProductCreateForm, ProductUpdateForm,
                        ProductCategoryCreateForm, DeliveryForm, DeliveryUpdateForm,
                         DeliveryDetailsFormSet,
                        DeliveryDetailsUpdateFormSet,
                        ProductCategoryUpdateForm,
                        SupplierUpdateForm, SupplierForm, WarehouseForm, WarehouseUpdateForm,
                        OrderForm,
                        OrderItemFormSet, OrderUpdateForm, OrderItemUpdateFormSet, LocationForm,
                         LocationUpdateForm, TransferForm, TransferUpdateForm, InventoryForm,
                        InventoryUpdateForm
                         )


from InventoryPlus.settings import GENERATIVE_API_KEY
import datetime
from django.utils import timezone
from accounts.models import User
from accounts.forms import UserUpdateForm





# Create your views here.
class DashboardTemplateView(WarehouseManagerRequiredMixin, TemplateView):
    template_name = 'dashboard/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_title'] = 'Products'
        context['quantity_available'] = Product.objects.aggregate(
            total_quantity=Sum('quantity_available')
        )['total_quantity']
        context['total_warehouses'] = Warehouse.objects.all().count()
        context['total_product'] = Product.objects.all().count()
        context['total_stock_title'] = 'Stock Value'
        context['stock_value'] = Product.objects.aggregate(
            total_stock_value=Sum(F('quantity_available') * F('unit_price'))
        )['total_stock_value']
        context['total_order'] = Order.objects.all().count()
        context['total_customers'] = User.objects.filter(user_type='CUSTOMER').all().count()
        context['total_sales_manager'] = User.objects.filter(user_type='SALES_MANAGER').all().count()
        context['total_suppliers'] = Supplier.objects.all().count()
        context['pending_deliveries'] = Delivery.objects.filter(status='pending')[:5]
        context['total_pending_deliveries'] = Delivery.objects.filter(status='pending').all().count()
        context['total_completed_deliveries'] = Delivery.objects.filter(status='completed').all().count()
        context['recent_orders'] = Order.objects.all()[:5]



        # Specify the categories of interest
        categories = [
            "Lumber and Wood Products",
            'Cement and Concrete Products',
            'Steel and Metal Products',
            'Electrical Supplies',
            'Plumbing Supplies'
        ]

        # Aggregate the total quantity available for each category
        category_totals = list(Product.objects.filter(
            category__name__in=categories
        ).values('category__name').annotate(
            total_quantity=Sum('quantity_available')
        ).order_by('category__name'))

        # Add the category totals to the context
        context['category_totals'] = category_totals

        return context


class SalesManagerTemplateView(TemplateView):
    template_name = 'dashboard/sales_manager.html'


class WarehouseManagerProductView(WarehouseManagerRequiredMixin, ListView):
    model = Product
    template_name = 'warehouse_manager/product/product_index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()


class ProductCreateView(WarehouseManagerRequiredMixin, CreateView):
    model = Product
    template_name = 'warehouse_manager/product/product_create.html'
    form_class = ProductCreateForm
    success_url = reverse_lazy('product_warehouse')

class ProductUpdateView(WarehouseManagerRequiredMixin, UpdateView):
    model = Product
    template_name = 'warehouse_manager/product/update.html'
    form_class = ProductUpdateForm
    success_url = reverse_lazy('product_warehouse')

class ProductDeleteView(WarehouseManagerRequiredMixin, DeleteView):
    model = Product
    template_name = 'warehouse_manager/product/confirm_delete.html'
    success_url = reverse_lazy('product_warehouse')





class WarehouseReport(WarehouseManagerRequiredMixin, TemplateView):
    template_name = 'dashboard/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['daily_sales'] = DeliveryDetails.objects.filter(
            delivery__sales_date=today
        ).values('product__name').annotate(
            total_quantity=Sum('quantity')
        )

        # Daily Deliveries Status
        context['daily_deliveries_status'] = Delivery.objects.filter(
            sales_date=today
        ).values('status').annotate(
            count=Count('id')
        )

        # Weekly Sales Summary
        week_start = timezone.now().date() - datetime.timedelta(days=7)
        context['weekly_sales'] = DeliveryDetails.objects.filter(
            delivery__sales_date__range=[week_start, timezone.now().date()]
        ).values('product__category__name').annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('product__unit_price'))
        )

        # Weekly Stock Levels
        context['weekly_stock'] = Inventory.objects.filter(
            last_updated__range=[week_start, timezone.now()]
        ).values('warehouse__name').annotate(
            average_stock=Avg('quantity_available')
        )

        # Monthly Inventory Summary
        month_start = timezone.now().date() - datetime.timedelta(days=30)
        context['monthly_inventory'] = Inventory.objects.filter(
            last_updated__range=[month_start, timezone.now()]
        ).values('product__name').annotate(
            total_quantity=Sum('quantity_available'),
            average_cost=Avg('average_cost')
        )

        # Monthly Order Summary
        context['monthly_orders'] = Order.objects.filter(
            order_date__range=[month_start, timezone.now()]
        ).values('provider__name').annotate(
            total_orders=Count('id'),
            total_value=Sum(F('orderitem__quantity') * F('orderitem__product__unit_price'))
        )

        return context


class InventoryListView(WarehouseManagerRequiredMixin, ListView):
    model = Inventory
    template_name = 'warehouse_manager/inventory/index.html'
    context_object_name = 'inventories'

    def get_queryset(self):
        return Inventory.objects.select_related('product', 'warehouse').all()

class SupplierListView(WarehouseManagerRequiredMixin, ListView):
    model = Supplier
    template_name = 'warehouse_manager/supplier/index.html'
    context_object_name = 'suppliers'

    def get_queryset(self):
        return Supplier.objects.all()


class SupplierCreateView(WarehouseManagerRequiredMixin, CreateView):
    model = Supplier
    template_name = 'warehouse_manager/supplier/create.html'
    form_class = SupplierForm
    success_url = reverse_lazy('supplier_index')


class SupplierUpdateView(WarehouseManagerRequiredMixin, UpdateView):
    model = Supplier
    template_name = 'warehouse_manager/supplier/update.html'
    form_class = SupplierUpdateForm
    success_url = reverse_lazy('supplier_index')


class SupplierDeleteView(WarehouseManagerRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'warehouse_manager/supplier/delete.html'
    success_url = reverse_lazy('supplier_index')

class SuccessView(TemplateView):
    template_name = 'warehouse_manager/product/success.html'
class ProductCategoryListview(WarehouseManagerRequiredMixin, ListView):
    model = ProductCategory
    template_name = 'warehouse_manager/product_category/index.html'
    context_object_name = 'product_categories'

    def get_queryset(self):
        # Annotate each ProductCategory with the count of related Products
        return ProductCategory.objects.annotate(product_count=Count('product'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductCategoryCreatView(WarehouseManagerRequiredMixin, CreateView):
    model = ProductCategory
    template_name = 'warehouse_manager/product_category/create.html'
    form_class = ProductCategoryCreateForm
    success_url = reverse_lazy('product_category_index')


class ProductCategoryUpdateView(WarehouseManagerRequiredMixin, UpdateView):
    model = ProductCategory
    template_name = 'warehouse_manager/product_category/update.html'
    form_class = ProductCategoryUpdateForm
    success_url = reverse_lazy('product_category_index')


class ProductCategoryDeleteView(WarehouseManagerRequiredMixin, DeleteView):
    model = ProductCategory
    template_name = 'warehouse_manager/product_category/confirm_delete.html'
    success_url = reverse_lazy('product_category_index')
    context_object_name = 'product_categories'

class WarehousesListView(WarehouseManagerRequiredMixin, ListView):
    model = Warehouse
    template_name = 'warehouse_manager/warehouse/index.html'
    context_object_name = 'warehouses'

    def get_queryset(self):
        return Warehouse.objects.all()

class WarehouseCreateView(WarehouseManagerRequiredMixin, CreateView):
    model = Warehouse
    template_name = 'warehouse_manager/warehouse/create.html'
    form_class = WarehouseForm
    success_url = reverse_lazy('warehouse_index')


class WarehouseUpdateView(WarehouseManagerRequiredMixin, UpdateView):
    model = Warehouse
    template_name = 'warehouse_manager/warehouse/update.html'
    form_class = WarehouseUpdateForm
    success_url = reverse_lazy('warehouse_index')

class WarehouseDeleteView(WarehouseManagerRequiredMixin, DeleteView):
    model = Warehouse
    template_name = 'warehouse_manager/warehouse/delete.html'
    success_url = reverse_lazy('warehouse_index')





class LocationListView(WarehouseManagerRequiredMixin, ListView):
    model = Location
    template_name = 'warehouse_manager/location/index.html'
    context_object_name = 'locations'

    def get_queryset(self):
        return Location.objects.all()


class DeliveryListView(WarehouseManagerRequiredMixin, ListView):
    model = Delivery
    template_name = 'warehouse_manager/deliveries/index.html'
    context_object_name = 'deliveries'

    def get_queryset(self):
        return Delivery.objects.select_related('order__customer').all().order_by('-sales_date')


class DeliveryDetailView(WarehouseManagerRequiredMixin, DetailView):
    model = Delivery
    template_name = 'warehouse_manager/deliveries/detail.html'
    context_object_name = 'delivery'


class DeliveryCreateView(CombinedManagerRequiredMixin, CreateView):
    model = Delivery
    form_class = DeliveryForm
    template_name = 'warehouse_manager/deliveries/create.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['delivery_items'] = DeliveryDetailsFormSet(self.request.POST)
        else:
            data['delivery_items'] = DeliveryDetailsFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        delivery_items = context['delivery_items']
        if form.is_valid() and delivery_items.is_valid():
            self.object = form.save()
            delivery_items.instance = self.object
            delivery_items.save()
            return redirect('delivery_index')
        else:
            return self.render_to_response(self.get_context_data(form=form))

class DeliveryUpdateView(CombinedManagerRequiredMixin, UpdateView):
    model = Delivery
    form_class = DeliveryUpdateForm
    template_name = 'warehouse_manager/deliveries/update.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['delivery_items'] = DeliveryDetailsUpdateFormSet(self.request.POST)
        else:
            data['delivery_items'] = DeliveryDetailsUpdateFormSet()
        return data


    def form_valid(self, form):
        context = self.get_context_data()
        delivery_items = context['delivery_items']
        if form.is_valid() and delivery_items.is_valid():
            self.object = form.save()
            delivery_items.instance = self.object
            delivery_items.save()
            return redirect('delivery_index')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class DeliveryDeleteView(WarehouseManagerRequiredMixin, DeleteView):
    model = Delivery
    template_name = 'warehouse_manager/deliveries/delete.html'
    success_url = reverse_lazy('delivery_index')


class TransferListView(WarehouseManagerRequiredMixin, ListView):
    model = Transfer
    template_name = 'warehouse_manager/transfer/index.html'
    context_object_name = 'transfers'

    def get_queryset(self):
        return Transfer.objects.all().order_by('-sent_date')


class UserListView(WarehouseManagerRequiredMixin, ListView):
    model = User
    template_name = 'warehouse_manager/user/index.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all().order_by('-last_login')



class CustomerListView(WarehouseManagerRequiredMixin, ListView):
    model = User
    template_name = 'warehouse_manager/user/customer/index.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return User.objects.filter(user_type='CUSTOMER')


class SalesManagerListView(WarehouseManagerRequiredMixin, ListView):
    model = User
    template_name = 'warehouse_manager/user/sales_manager/index.html'
    context_object_name = 'sales_managers'

    def get_queryset(self):
        return User.objects.filter(user_type='SALES_MANAGER')


class WarehouseManagerListView(WarehouseManagerRequiredMixin, ListView):
    model = User
    template_name = 'warehouse_manager/user/warehouse_manager/index.html'
    context_object_name = 'warehouse_managers'

    def get_queryset(self):
        return User.objects.filter(user_type='WAREHOUSE_MANAGER')



class UserUpdateView(WarehouseManagerRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/user_update.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('user_index')


class OrderListView(ListView):
    model = Order
    template_name = 'warehouse_manager/order/index.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.all().order_by('-order_date')

class OrderDetailView(DetailView):
    model = Order
    template_name = 'warehouse_manager/order/detail.html'
    context_object_name = 'order'

    def get_object(self):
        # Fetch the order object and handle if it doesn't exist
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['order_items'] = OrderItem.objects.filter(order=order)
        return context


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'warehouse_manager/order/delete.html'
    success_url = reverse_lazy('order_index')

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'warehouse_manager/order/create.html'

    def __init__(self):
        self.object = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['order_items'] = OrderItemFormSet(self.request.POST)
        else:
            data['order_items'] = OrderItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']
        if form.is_valid() and order_items.is_valid():
            self.object = form.save()
            order_items.instance = self.object
            order_items.save()
            return redirect('order_index')
        else:
            return self.render_to_response(self.get_context_data(form=form))



class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderUpdateForm
    template_name = 'warehouse_manager/order/update.html'
    success_url = reverse_lazy('order_index')

    def __init__(self):
        self.object = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['order_items'] = OrderItemUpdateFormSet(self.request.POST)
        else:
            data['order_items'] = OrderItemUpdateFormSet()
        return data


    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']
        if form.is_valid() and order_items.is_valid():
            self.object = form.save()
            order_items.instance = self.object
            order_items.save()
            return redirect('order_index')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class LocationCreateView(WarehouseManagerRequiredMixin, CreateView):
    model = Location
    template_name = 'warehouse_manager/location/create.html'
    form_class = LocationForm
    success_url = reverse_lazy('location_index')


class LocationUpdateView(WarehouseManagerRequiredMixin, UpdateView):
    model = Location
    form_class = LocationUpdateForm
    template_name = 'warehouse_manager/location/update.html'
    success_url = reverse_lazy('location_index')

class LocationDeleteView(WarehouseManagerRequiredMixin, DeleteView):
    model = Location
    template_name = 'warehouse_manager/location/delete.html'
    success_url = reverse_lazy('location_index')


class TransferDetailView(WarehouseManagerRequiredMixin, DetailView):
    model = Transfer
    template_name = 'warehouse_manager/transfer/detail.html'
    context_object_name = 'transfer'

    def get_object(self, queryset=None):
        return get_object_or_404(Transfer, pk=self.kwargs['pk'])

class TransferCreateView(WarehouseManagerRequiredMixin, CreateView):
    model = Transfer
    template_name = 'warehouse_manager/transfer/create.html'
    form_class = TransferForm
    success_url = reverse_lazy('transfer_index')

class TransferUpdateView(WarehouseManagerRequiredMixin, UpdateView):
    model = Transfer
    template_name = 'warehouse_manager/transfer/update.html'
    form_class = TransferUpdateForm
    success_url = reverse_lazy('transfer_index')


class TransferDeleteView(WarehouseManagerRequiredMixin, DeleteView):
    model = Transfer
    template_name = 'warehouse_manager/transfer/delete.html'
    success_url = reverse_lazy('transfer_index')


class YearlyReportView(TemplateView):
    template_name = 'dashboard/yearly_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = datetime.date.today().year
        orders_year = Order.objects.filter(order_date__year=current_year)
        order_items_year = OrderItem.objects.filter(order__in=orders_year)

        # Prepare data for charts
        top_5_products = OrderItem.objects.values('product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
        bottom_5_products = OrderItem.objects.values('product__name').annotate(total_quantity=Sum('quantity')).order_by('total_quantity')[:5]

        top_5_products_quantity = Product.objects.all().order_by('-quantity_available')[:5]
        bottom_5_products_quantity = Product.objects.all().order_by('quantity_available')[:5]
        # Extract data for the charts
        top_5_product_names = [item['product__name'] for item in top_5_products]
        top_5_product_quantities = [item['total_quantity'] for item in top_5_products]
        bottom_5_product_names = [item['product__name'] for item in bottom_5_products]
        bottom_5_product_quantities = [item['total_quantity'] for item in bottom_5_products]

        context['orders_year'] = orders_year
        context['order_items_year'] = order_items_year
        context['top_5_product_names'] = top_5_product_names
        context['top_5_products_quantity'] = top_5_products_quantity
        context['bottom_5_products_quantity'] = bottom_5_products_quantity
        context['top_5_product_quantities'] = top_5_product_quantities
        context['bottom_5_product_names'] = bottom_5_product_names
        context['bottom_5_product_quantities'] = bottom_5_product_quantities
        return context

class InventoryCreateView(WarehouseManagerRequiredMixin, CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'warehouse_manager/inventory/create.html'
    success_url = reverse_lazy('inventory_index')


class InventoryUpdateView(WarehouseManagerRequiredMixin, UpdateView):
    model = Inventory
    form_class = InventoryUpdateForm
    template_name = 'warehouse_manager/inventory/update.html'
    success_url = reverse_lazy('inventory_index')


class InventoryDeleteView(WarehouseManagerRequiredMixin, DeleteView):
    model = Inventory
    template_name = 'warehouse_manager/inventory/delete.html'
    success_url = reverse_lazy('inventory_index')




class NotificationListView(CombinedManagerRequiredMixin, ListView):
    model = Notification
    template_name = 'dashboard/notification.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False)

class MarkNotificationAsReadView(CombinedManagerRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        notification = get_object_or_404(Notification, pk=kwargs['pk'])
        notification.is_read = True
        notification.save()
        return self.request.GET.get('next', '/notifications/')

