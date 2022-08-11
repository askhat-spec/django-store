from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline

from .filters import ProductFilter
from .models import Header, Product, ProductImage


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


class Search(ListView):
    paginate_by = 20
    template_name = 'shop/search.html'
    # allow_empty = False
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        if not settings.DEBUG:
            vector = SearchVector('name', 'description')
            query = SearchQuery(q)
            # search_headline = SearchHeadline('description', query)
            # object_list = Paper.objects.annotate(rank=SearchRank(vector, query)).annotate(headline=search_headline).filter(rank__gte=0.001).order_by('-rank')
            object_list = Product.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.001).order_by('-rank')
        else:
            object_list = Product.objects.filter(name__icontains=q)
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        # context["search_list_lenght"] = self.object_list.count()
        return context