from django.views.generic import TemplateView, ListView, DetailView
from core.models import Product, ProductCategory
from cart.forms import CartAddProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'product/product_index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        context['selected_category'] = None
        return context


class CategoryProductListView(ListView):
    model = Product
    template_name = 'product/product_index.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Product.objects.filter(category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        context['selected_category'] = self.kwargs.get('category_id')
        return context


class TrendingProductsView(ListView):
    model = Product
    template_name = 'base.html'
    context_object_name = 'trending_products'

    def get_queryset(self):
        return Product.objects.all()[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_title'] = 'Trending Products'

        return context


class NewArrivalView(ListView):
    model = Product
    template_name = 'base.html'
    context_object_name = 'new_arrival_products'

    def get_queryset(self):
        return Product.objects.order_by('-id')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_title'] = 'New Arrivals'

        return context


class TopRatedProductsView(ListView):
    model = Product
    template_name = 'base.html'
    context_object_name = 'top_rated_products'

    def get_queryset(self):
        return Product.objects.order_by('-unit_price')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_title'] = 'Top Rated Products'

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    cart_product_form = CartAddProductForm()

    def get_context_data(self, **kwargs):
        product = self.object.category
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(category=product).exclude(pk=self.object.pk)
        context['cart_product_form'] = CartAddProductForm
        return context



