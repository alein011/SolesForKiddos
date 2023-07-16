from datetime import datetime, timedelta
from django.shortcuts import render
from store.models import Product, ReviewRating
from django.db.models import Q

def home(request):
    
    seven_days_ago = datetime.now() - timedelta(days=7)
    products = Product.objects.filter(Q(is_sale=True) | Q(modified_date__gte=seven_days_ago)).order_by('-modified_date')[:9]
    
    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)