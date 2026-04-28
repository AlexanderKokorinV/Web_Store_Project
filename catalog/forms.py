from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from .models import Product


class ProductForm(forms.ModelForm):
    """Класс формы для добавления нового товара"""

    forbidden_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    class Meta:
        model = Product
        fields = ["product_name", "product_description", "image", "category_name", "price"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields["product_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите наименование продукта",
            }
        )

        self.fields["product_description"].widget.attrs.update(
            {
                "class": "form-control",
                "rows": 3,
                "placeholder": "Введите описание продукта",
            }
        )

        self.fields["image"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )

        self.fields["image"].validators.append(
            FileExtensionValidator(
                allowed_extensions=["jpeg", "jpg", "png"],
                message="Недопустимый формат файла. Допустимы только JPEG, JPG и PNG.",
            )
        )

        self.fields["category_name"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )

        self.fields["price"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )

    def clean_product_name(self):
        cleaned_data = self.cleaned_data.get("product_name")

        if cleaned_data:
            for word in self.forbidden_words:
                if word.lower() in cleaned_data.lower():
                    raise ValidationError(f"Вы не можете использовать слово '{word}' в названии продукта")
        return cleaned_data

    def clean_product_description(self):
        cleaned_data = self.cleaned_data.get("product_description")

        if cleaned_data:
            for word in self.forbidden_words:
                if word.lower() in cleaned_data.lower():
                    raise ValidationError(f"Вы не можете использовать слово '{word}' в описании продукта")
        return cleaned_data

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if image:
            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError("Размер файла не должен превышать 5 МБ.")

        return image

    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price is not None and price < 0:
            raise ValidationError("Цена продукта не может быть отрицательной")

        return price
