from django.shortcuts import get_object_or_404, render, redirect, reverse 
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category

# Create your views here.
def all_products(request):
    """ A view to show all products, including sorting and search queries """
    
    products = Product.objects.all()
    query = None # Initialize query variable to None to avoid potential UnboundLocalError
    category = None # Initialize category variable to None to avoid potential UnboundLocalError
    sort = None # Initialize sort variable to None to avoid potential UnboundLocalError
    direction = None # Initialize direction variable to None to avoid potential UnboundLocalError
    
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name' # Annotate the queryset with a new field 'lower_name' that contains the lowercase version of the product name to enable case-insensitive sorting by name
                products = products.annotate(lower_name=Lower('name')) # Use the annotate() method to add the 'lower_name' field to the products queryset
                
            if sortkey == 'category':
                sortkey = 'category__name' # Use the double underscore notation to specify that we want to sort by the name field of the related Category model when sorting by category
            
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}' # Prepend a '-' to the sortkey to indicate descending order in the order_by() method
            products = products.order_by(sortkey) # Order the products queryset based on the sortkey
                
        
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
            
    current_sorting = f'{sort}_{direction}' # Create a string that represents the current sorting method and direction to use in the template for highlighting the active sorting option
    
    context = {
        'products': products, # Pass the filtered products queryset to the template context to display the search results
        'search_string': query, # Pass the search query to the template context to pre-fill the search input field with the user's search term
        'current_categories': category, # Pass the current categories to the template context to display the selected categories in the template
        'current_sorting': current_sorting, # Pass the current sorting method and direction to the template context to highlight the active sorting option
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)