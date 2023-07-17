from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Product, ReviewRating, ProductGallery, FAQS, faq_topic, Policy, Banner
from category.models import Age, Brand, Category
from carts.models import CartItem
from django.db.models import Q

from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct


# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories).order_by('-is_available')
        paginator= Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        
    
    else:
        products = Product.objects.all().order_by('-is_available')
        paginator= Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    
    return render(request, 'store/store.html', context)


def gender(request, gender_slug=None):
    # gender_categories = None
    products = None

    if gender_slug != None:
        # gender_categories = get_object_or_404(Product.gender_category, gender_category = gender_slug)
        products = Product.objects.filter(gender_category=gender_slug).order_by('-is_available')
        paginator= Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().order_by('-gender_category', '-is_available')
        paginator= Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    
    return render(request, 'store/store.html', context)

def brand(request, brand_slug=None):
    brands = Brand.objects.all()
    selected_brands = request.GET.getlist('brand')

    if brand_slug is not None:
        selected_brands.append(brand_slug)

    if len(selected_brands) > 0:
        products = Product.objects.filter(brand__slug__in=selected_brands).order_by('-is_available')
    else:
        products = Product.objects.order_by('-is_available', 'brand')

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'brands': brands,
        'selected_brands': selected_brands,
    }

    return render(request, 'store/store.html', context)

def age(request, age_slug=None):
    ages = Age.objects.all()  # Retrieve all Age objects

    if age_slug is not None:
        age = get_object_or_404(Age, slug=age_slug)
        products = Product.objects.filter(age_category=age).order_by('-is_available')
    else:
        products = Product.objects.order_by('-is_available', 'age_category')

    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'ages': ages,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        products = []
        product_count = 0
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
            
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)



def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

def faq(request):
    
    faq_topics = faq_topic.objects.all()

    faq_data = []
    for topic in faq_topics:
        faqs = FAQS.objects.filter(category=topic)
        faq_data.append((topic, faqs))

    context = {
        'faq_data': faq_data,
    }
    
    return render(request, 'store/faq.html', context)

def faq_search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        faq_topics = faq_topic.objects.all()
        faq_data = []
        if keyword:
            for topic in faq_topics:
                faqs = FAQS.objects.filter(
                    Q(question__icontains=keyword) | Q(answer__icontains=keyword),
                    category=topic.id
                ).order_by('-category')
                if faqs.exists():
                    faq_data.append((topic, faqs))
                

    context = {
        'faq_data': faq_data,
    }
    
    return render(request, 'store/faq.html', context)

def policy(request, policy_slug=None):
    policies = Policy.objects.all()
    policy_indiv = None
    
    if policy_slug:
        policy_indiv = get_object_or_404(Policy, slug=policy_slug)
    else:
        policy_indiv = Policy.objects.all().order_by('title')
        return render(request, 'store/policy.html', context)
    
    context = {
        'policies': policies,
        'policy_indiv': policy_indiv,
    }
    
    return render(request, 'store/policy_indiv.html', context)

def carousel(request):
    banners = Banner.objects.all()
    
    context = {
        'banners': banners,
    }
    
    return render(request, 'home.html', context)

