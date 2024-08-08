from django.shortcuts import render
from django.views.generic import TemplateView

from core.models import Product


# Create your views here.


class IndexTemplateView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetching products
        context['trending_products'] = Product.objects.all()[:5]
        context['new_arrival_products'] = Product.objects.order_by('-id')[:5]
        context['top_rated_products'] = Product.objects.order_by('-unit_price')[:5]

        # Set section titles
        context['trending_section_title'] = 'Trending Products'
        context['new_arrival_section_title'] = 'New Arrivals'
        context['top_rated_section_title'] = 'Top Rated Products'

        return context
