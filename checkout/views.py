from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, reverse
from .forms import OrderForm

# Create your views here.

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51N8n9sHh7qj2mL1Xo5l3Zt0aQyKpVh6u7v8w9x0y1z2a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r0s1t2u3v4w5x6y7z8',
        'client_secret': 'test client_secret_1234567890abcdefg',
    }
    return render(request, template, context)
