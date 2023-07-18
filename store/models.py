from django.db import models
from category.models import Brand, Category, Age
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
from django.core.exceptions import ValidationError
import itertools
from ckeditor.fields import RichTextField

# Create your models here.

gender_choices = (
    ('boys', 'boys'),
    ('girls', 'girls')
)

age_choices = (
    ('infant-0-2', 'Infant (0 - 2)'),
    ('toddler-3-5', 'Toddler (3 - 5)'),
    ('little-kids-6-12', 'little kids(6 - 12)')
)

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    brand           = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    description     = models.TextField(max_length=500)
    price           = models.IntegerField()
    sale_price      = models.IntegerField(null=True, blank=True)
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_sale         = models.BooleanField(default=False)
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    gender_category = models.CharField(max_length=50, choices=gender_choices, blank=True)
    age_category    = models.ForeignKey(Age, on_delete=models.CASCADE, null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    def clean(self):
        
        if self.is_sale and not self.sale_price:
            raise ValidationError("Sale price must be provided when is_sale is True.")
        
        if self.sale_price and not self.is_sale:
            raise ValidationError("The product is not sale")
        
        if self.sale_price and self.sale_price >= self.price:
            raise ValidationError("Sale price must be less than the price.")
    
    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.is_available = False
        else:
            self.is_available = True
        super().save(*args, **kwargs)

        # Automatically set sizes based on age_category
        if self.age_category:
            if self.age_category.age == "Infant (0 - 2 years)":
                sizes = ["2C", "2.5C", "3C", "3.5C", "4C", "4.5C", "5C", "5.5C", "6C", "6.5C", "7C"]
            elif self.age_category.age == "Toddler (3 - 5)":
                sizes = [ "7.5C", "8C", "8.5C", "9C", "9.5C", "10C", "10.5C", "11C", "11.5C", "12C"]
            else:
                sizes = ["12.5C", "13C", "13.5C", "1Y", "1.5Y", "2Y", "2.5Y", "3Y", "3.5Y", "4Y", "4.5Y", "5Y", "5.5Y", "6Y"]
                
                for size in sizes:
                    Variation.objects.create(product=self, variation_category="size", variation_value=size)


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
    
variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)
    
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100, blank=True)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)
    
    objects = VariationManager()
    
    def __str__(self):
        return self.variation_value
    
class VariationCreator:
    @staticmethod
    def create_variations(product):
        colors = Variation.objects.colors().values_list('variation_value', flat=True)
        sizes = Variation.objects.sizes().values_list('variation_value', flat=True)

        variations = list(itertools.product(colors, sizes))

        for color, size in variations:
            variation_value = f"{product.product_name} - {color} - {size}"
            Variation.objects.create(product=product, variation_category='Product Variation', variation_value=variation_value)
    

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'

class faq_topic(models.Model):
    title = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = 'faq_topic'
        verbose_name_plural = 'FAQ Category'

    def __str__(self):
        return self.title        

class FAQS(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )  

    category = models.ForeignKey(faq_topic, default=None, on_delete=models.CASCADE, blank=True, null=True)
    question = models.CharField(max_length=200)
    answer = RichTextField()
    status=models.CharField(max_length=10, choices=STATUS, default=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'faqs'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return self.question
    
class Policy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    content = RichTextField()
    
    class Meta:
        verbose_name = 'policy'
        verbose_name_plural = 'policies'
        
    def get_url(self):
        return reverse('indiv_policy', args=[self.slug])
    
    def __str__(self):
        return self.title

class Banner(models.Model):
    images      = models.ImageField(upload_to='photos/banners',max_length=255)
    title       = models.CharField(max_length=200, blank=True)
    subtitle    = models.CharField(max_length=200, blank=True)
    is_active   = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    