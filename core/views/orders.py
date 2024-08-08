from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy
from accounts.models import User

from core.models import OrderItem, Order, Notification
from core.forms import CustomerOrderForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView



@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = CustomerOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'])
            cart.clear()
            notify_managers_new_order(order)

            request.session['order_id'] = order.id
            messages.success(request, 'Order placed successfully!')
            return redirect(reverse('payment:process'))

    else:
        form = CustomerOrderForm()

    customer_name = request.user.get_full_name()

    return render(request, 'warehouse_manager/order/customer_order.html', {
        'cart': cart,
        'form': form,
        'customer_name': customer_name
    })


def notify_managers_new_order(order):
    managers = User.objects.filter(user_type__in=[User.WAREHOUSE_MANAGER, User.SALES_MANAGER])
    for manager in managers:
        Notification.objects.create(
            user=manager,
            message=f'New order placed by {order.customer.get_full_name()}. Order Code: {order.code}'
        )


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'warehouse_manager/order/created.html', {'order': order})

class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'warehouse_manager/order/history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-order_date')

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'warehouse_manager/order/history_detail.html'
    context_object_name = 'order'

    def get_queryset(self):

        return Order.objects.filter(customer=self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.filter(order=self.object)
        return context





def generate_pdf_receipt(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # Render HTML template with context
    html_string = render_to_string('warehouse_manager/order/receipt.html', {'order': order})

    # Create PDF from HTML
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{order_id}.pdf"'

    return response



