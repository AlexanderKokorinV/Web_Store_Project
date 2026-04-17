from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    """Класс формы для добавления нового товара"""

    class Meta:
        model = Product
        fields = ("product_name", "product_description", "image", "category_name", "price")
        widgets = {
            "product_name": forms.TextInput(attrs={"class": "form-control"}),
            "product_description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "category_name": forms.Select(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
        }
