from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.
def all_products(request):
    """ A view to show all products, including sorting and search queries """
    
    products = Product.objects.all()
    query = None # Initialize query variable to None to avoid potential UnboundLocalError
    category = None # Initialize category variable to None to avoid potential UnboundLocalError
    
    if request.GET:
        if 'category' in request.GET:
            category = request.GET['category'].split(',') # Split the category string into a list of categories
            products = products.filter(category__name__in=category) # Filter the products queryset based on the selected categories
            category = Category.objects.filter(name__in=category) # Get the Category objects for the selected categories to display in the template
            
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
    
            queries = Q(name__icontains=query) | Q(description__icontains=query) # Use Q objects to perform a case-insensitive search on both the name and description fields
            products = products.filter(queries) # Filter the products queryset based on the search query
    context = {
        'products': products,
        'search_string': query, # Pass the search query to the template context to pre-fill the search input field with the user's search term
        'current_categories': category, # Pass the current categories to the template context to display the selected categories in the template
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)