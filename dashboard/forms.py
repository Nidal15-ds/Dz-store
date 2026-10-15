from django import forms
from store.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'price', 'stock', 'photo', 'image_url',
            'description', 'rating', 'is_pack', 'bundle_items',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'bundle_items': forms.SelectMultiple(attrs={'size': 8}),
        }
