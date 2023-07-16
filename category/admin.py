from django.contrib import admin
from .models import Brand, Category, Age

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand_name',)}
    list_display = ('brand_name', 'slug')
    
class AgeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('age',)}
    list_display = ('age', 'slug')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Age, AgeAdmin)


