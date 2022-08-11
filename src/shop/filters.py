from dataclasses import fields
import django_filters
from django_filters import widgets
from .models import Product


class ProductFilter(django_filters.FilterSet):
    CHOICES = (
        ('newest', 'Сначала новые'),
        ('oldest', 'Сначала старые'),
        ('cheaper', 'Сначала дешевле'),
        ('pricier', 'Сначала дороже'),
    )

    price = django_filters.RangeFilter(
        label='По ценам (от-до)',
        widget=widgets.RangeWidget(
            attrs={
                'class': 'form-control',
                'placeholder': 'Цена'
                }
            )
        )

    ordering = django_filters.ChoiceFilter(label='Сортировка', choices=CHOICES, method='filter_by_order', empty_label=None)

    class Meta:
        model = Product
        fields = ['price', 'ordering']

    def filter_by_order(self, queryset, name, value):
        match value:
            case 'newest':
                expression = '-created'
            case 'oldest':
                expression = 'created'
            case 'cheaper':
                expression = 'price'
            case 'pricier':
                expression = '-price'
            case _:
                expression = '-created'

        return queryset.order_by(expression)
