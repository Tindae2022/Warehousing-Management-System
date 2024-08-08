from django.urls import path
from core.views.orders import (
    order_create, order_success, OrderHistoryView, OrderDetailView,
                               generate_pdf_receipt
)
from .views.base_view import IndexTemplateView
from .views.products import (ProductListView, CategoryProductListView,
                             TrendingProductsView, TopRatedProductsView, NewArrivalView,
                             ProductDetailView)

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/category/<int:category_id>/', CategoryProductListView.as_view(), name='product_list_by_category'),
    path('products/trending/', TrendingProductsView.as_view(), name='trending_products'),
    path('products/new/', NewArrivalView.as_view(), name='new_arrivals'),
    path('product/top-rated/', TopRatedProductsView.as_view(), name='top_rated_products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', order_create, name='customer_order_create'),
    path('order-success/<int:order_id>/', order_success, name='order_success'),
    path('order-history/', OrderHistoryView.as_view(), name='order_history'),
    path('order_distory/detail/<int:pk>/', OrderDetailView.as_view(), name='order_history_detail'),
    path('receipt/<int:order_id>/', generate_pdf_receipt, name='generate_receipt'),


]
