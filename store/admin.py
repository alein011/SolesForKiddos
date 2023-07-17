from django.contrib import admin
from .models import Banner, Product, Variation, ReviewRating, ProductGallery, FAQS, faq_topic, Policy
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'sale_price', 'stock', 'category', 'gender_category', 'age_category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

class PolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
admin.site.register(FAQS)
admin.site.register(faq_topic)
admin.site.register(Policy, PolicyAdmin)
admin.site.register(Banner)



