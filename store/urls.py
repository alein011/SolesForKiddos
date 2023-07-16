
from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('gender/<slug:gender_slug>/', views.gender, name='products_by_gender'),
    path('age/<slug:age_slug>/', views.age, name='products_by_age'),
    path('age/', views.age, name='age'),
    path('brand/', views.brand, name='brand'),
    path('brand/<str:brand_slug>/', views.brand, name='products_by_brand'),
    path('search/', views.search, name='search'),
    path('faq/', views.faq, name='faq'),
    
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
] 
