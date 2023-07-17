from store.models import faq_topic
from .models import Category, Brand, Age

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

def brand_list(request):
    brands = Brand.objects.all()
    return dict(brands=brands)

def age_list(request):
    ages = Age.objects.all()
    return dict(ages=ages)

def category_list(request):
    topics = faq_topic.objects.all()
    return dict(topics=topics)

