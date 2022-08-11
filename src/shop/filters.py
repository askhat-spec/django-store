import django_filters
from .models import Product, Category
from django import forms


class ProductFilter(django_filters.FilterSet):
    CHOICES = (
        ('newest', 'Сначала новые'),
        ('oldest', 'Сначала старые'),
        ('cheaper', 'Сначала дешевле'),
        ('pricier', 'Сначала дороже'),
    )

    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(), 
        empty_label='Все категории',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                }
            )
        )

    price = django_filters.RangeFilter(
        label='По ценам (от-до)',
        widget=django_filters.widgets.RangeWidget(
            attrs={
                'class': 'form-control',
                'placeholder': 'Цена'
                }
            )
        )

    ordering = django_filters.ChoiceFilter(
        label='Сортировка', 
        choices=CHOICES, method='filter_by_order', 
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                }
            )
        )

    class Meta:
        model = Product
        fields = ['category', 'ordering', 'price']

    def filter_by_order(self, queryset, name, value):
        ORDER_EXP = (
            ('newest', '-created'),
            ('oldest', 'created'),
            ('cheaper', 'price'),
            ('pricier', '-price'),
        )

        for key, expression in ORDER_EXP:
            if key == value:
                return queryset.order_by(expression)
