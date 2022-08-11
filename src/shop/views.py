from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from .filters import ProductFilter
from .models import Category, Header, Product, ProductImage


def index(request):
    carousel = Header.objects.all()
    new_products = Product.objects.all().order_by('-created')[:10]
    return render(
        request, 'shop/index.html', 
        {
            'carousel': carousel,
            'new_products': new_products,
        }
    )


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    filter = ProductFilter(request.GET, queryset=products.order_by('-created'))

    paginator = Paginator(filter.qs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/product/list.html',
            {
                'category': category,
                'page_obj': page_obj,
                'filter': filter,
            }
        )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    photos = ProductImage.objects.filter(product=product)
    return render(request, 'shop/product/detail.html', 
        {
            'product': product, 
            'photos': photos,
        }
    )