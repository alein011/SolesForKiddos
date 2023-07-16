from django import forms
from .models import ReviewRating, Product

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['review', 'rating']
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['price', 'sale_price', 'images', 'stock', 'is_sale']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.is_sale:
            self.fields['sale_price'].widget = forms.HiddenInput()