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


def product_list(request):
    products = Product.objects.filter(available=True).order_by('-created')
    filter = ProductFilter(request.GET, queryset=products)
    paginator = Paginator(filter.qs, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/product/list.html',
            {
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