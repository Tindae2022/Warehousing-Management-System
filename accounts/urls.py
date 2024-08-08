from django.urls import path
from .views import (RegisterCustomerView,
                    RegisterSalesManagerView, RegisterWarehouseManagerView,
                    LoginView, LogoutView, UpdateCustomerView,
                    UpdateSalesManagerView, UpdateWarehouseManagerView)

app_name = "accounts"

urlpatterns = [
    path("register/customer/", RegisterCustomerView.as_view(), name="register_customer"),
    path("register/sales_manager/", RegisterSalesManagerView.as_view(), name="register_sales_manager"),
    path("register/warehouse_manager/", RegisterWarehouseManagerView.as_view(), name="register_warehouse_manager"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("update/customer/", UpdateCustomerView.as_view(), name="update_customer"),
    path("update/sales_manager/", UpdateSalesManagerView.as_view(), name="update_sales_manager"),
    path("update/warehouse_manager/", UpdateWarehouseManagerView.as_view(), name="update_warehouse_manager"),
]
