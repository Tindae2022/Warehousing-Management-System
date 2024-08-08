from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
import stripe
from django.conf import settings

from core.models import Order

# Create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id')
    if not order_id:
        # Handle the case where the order_id is not in session
        return redirect('order_list')  # Adjust the URL name as needed

    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        # Stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # Add order items to the Stripe checkout session
        for item in order.orderitem_set.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.total_price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })

        # Create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)

        # Redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', {'order': order})


def payment_completed(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'payment/completed.html', context={
        'order': order,
    })


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
