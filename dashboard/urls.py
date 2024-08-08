from django.urls import path
from .views import ( DashboardTemplateView, SalesManagerTemplateView,
                     WarehouseManagerProductView, LocationCreateView,

                    ProductCreateView, WarehouseReport, InventoryListView, SupplierListView,

                    ProductCategoryListview, WarehousesListView, LocationListView,

                    DeliveryListView, DeliveryDetailView, TransferListView, SuccessView,

                    ProductUpdateView, ProductDeleteView, UserListView, UserUpdateView,

                    CustomerListView, SalesManagerListView, WarehouseManagerListView,
                    ProductCategoryCreatView, ProductCategoryUpdateView, ProductCategoryDeleteView,

                    SupplierCreateView, SupplierUpdateView, SupplierDeleteView,

                    WarehouseCreateView, WarehouseDeleteView, WarehouseUpdateView,
                    OrderListView, OrderDetailView, OrderDeleteView, OrderCreateView,
                   OrderUpdateView, DeliveryCreateView, DeliveryUpdateView,
                     DeliveryDeleteView, LocationDeleteView, LocationUpdateView, TransferDetailView,
                   TransferCreateView, TransferUpdateView, TransferDeleteView, YearlyReportView,
                   InventoryCreateView, InventoryUpdateView, InventoryDeleteView,
                  NotificationListView, MarkNotificationAsReadView










                    )

urlpatterns = [
    path('', DashboardTemplateView.as_view(), name='dashboard'),

    path('sales_manager/', SalesManagerTemplateView.as_view(), name='sales_manager'),

    path('warehouse_manager/product-view/', WarehouseManagerProductView.as_view(), name='product_warehouse'),

    path('ware-house/add/product/', ProductCreateView.as_view(), name='product_create'),

    path('warehouse/reports/', WarehouseReport.as_view(), name='report'),

    path('inventories/index/', InventoryListView.as_view(), name='inventory_index'),

    path('supplier/index/', SupplierListView.as_view(), name='supplier_index'),

    path('product/category-index/', ProductCategoryListview.as_view(), name='product_category_index'),

    path('warehouses/index/', WarehousesListView.as_view(), name='warehouse_index'),

    path('location/index/', LocationListView.as_view(), name='location_index'),

    path('delivery/index/', DeliveryListView.as_view(), name='delivery_index'),

    path('delivery/<int:pk>/', DeliveryDetailView.as_view(), name='delivery_detail'),

    path('transfer/index/', TransferListView.as_view(), name='transfer_index'),

    path('sucessfull-registration/', SuccessView.as_view(), name='success_view'),

    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),

    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    path('user-listview/', UserListView.as_view(), name='user_index'),

    path('user/update-view/<int:pk>/', UserUpdateView.as_view(), name='user_update'),

    path('customer/list-view/', CustomerListView.as_view(), name='customer_view'),

    path('sales-manager/list-view/', SalesManagerListView.as_view(), name='sales_manager_index'),

    path('warehouse-manager/index/', WarehouseManagerListView.as_view(), name='warehouse_manager_index'),

    path('product-category/create/', ProductCategoryCreatView.as_view(), name='product_category_create'),

    path('product-category/update/<int:pk>/', ProductCategoryUpdateView.as_view(), name='product_category_update'),

    path('product-category/delete/<int:pk>/', ProductCategoryDeleteView.as_view(), name='product_category_delete'),

    path('supplier/create/', SupplierCreateView.as_view(), name='supplier_create'),

    path('supplier/update-view/<int:pk>/', SupplierUpdateView.as_view(), name='supplier_update' ),

    path('supplier/delete-view/<int:pk>/', SupplierDeleteView.as_view(), name='supplier_delete'),

    path('warehouse/create-view/', WarehouseCreateView.as_view(), name='warehouse_create'),

    path('warehouse/update-view/<int:pk>/', WarehouseUpdateView.as_view(), name='warehouse_update'),

    path('warehouse/delete-view/<int:pk>/', WarehouseDeleteView.as_view(), name='warehouse_delete'),

    path('order/index/', OrderListView.as_view(), name='order_index'),

    path('order/detail-view/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),

    path('order/delete-view/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),

    path('order/create/', OrderCreateView.as_view(), name='order_create'),

    path('order/update-view/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),

    path('delivery/create-view/', DeliveryCreateView.as_view(), name='delivery_create'),

    path('delivery/update-view/<int:pk>/', DeliveryUpdateView.as_view(), name='delivery_update'),

    path('delivery/delete-view/<int:pk>/', DeliveryDeleteView.as_view(), name='delivery_delete'),

    path('location/create-view/', LocationCreateView.as_view(), name='location_create'),

    path('location/update-view/<int:pk>/', LocationUpdateView.as_view(), name='location_update'),

    path('location/delete-view/<int:pk>/', LocationDeleteView.as_view(), name='location_delete'),

    path('transfer/detail-view/<int:pk>/', TransferDetailView.as_view(), name='transfer_detail'),

    path('delete/create-view/', TransferCreateView.as_view(), name='transfer_create'),

    path('transfer/update-view/<int:pk>/', TransferUpdateView.as_view(), name='transfer_update'),

    path('transfer/delete-view/<int:pk>/', TransferDeleteView.as_view(), name='transfer_delete'),

    path('report/yearly/', YearlyReportView.as_view(), name='yearly_report'),

    path('inventory/create-view/', InventoryCreateView.as_view(), name='inventory_create'),

    path('inventory/update-view/<int:pk>/', InventoryUpdateView.as_view(), name='inventory_update'),

    path('inventory/delete-view/<int:pk>/', InventoryDeleteView.as_view(), name='inventory_delete'),

    path('notifications/', NotificationListView.as_view(), name='notifications'),

    path('notifications/mark_as_read/<int:pk>/', MarkNotificationAsReadView.as_view(), name='mark_as_read'),




]
