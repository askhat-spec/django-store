from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline

from .filters import ProductFilter
from .models import Header, Product, ProductImage, About, Info


def index(request):
    carousel = Header.objects.all()
    new_products = Product.objects.filter(available=True).order_by('-created')[:10]
    return render(
        request, 'shop/index.html', 
        {
            'carousel': carousel,
            'new_products': new_products,
        }
    )


# def product_list(request):
#     products = Product.objects.filter(available=True).order_by('-created')
#     filter = ProductFilter(request.GET, queryset=products)
#     paginator = Paginator(filter.qs, 2)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'shop/product/list.html',
#             {
#                 'page_obj': page_obj,
#                 'filter': filter,
#             }
#         )


class ProductList(ListView):
    template_name = 'shop/product/list.html'
    model = Product
    paginate_by = 30
    ordering = ['-created']

    def get_queryset(self):
        qs = self.model.objects.filter(available=True)
        product_filtered_list = ProductFilter(self.request.GET, queryset=qs)
        return product_filtered_list.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = ProductFilter(self.request.GET, self.get_queryset())
        context['filter'] = filter
        return context


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    photos = ProductImage.objects.filter(product=product)
    similar_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id).order_by('?')[:10]
    if len(similar_products) < 3:
        similar_products = None
    return render(request, 'shop/product/detail.html', 
        {
            'product': product, 
            'photos': photos,
            'similar_products': similar_products,
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


def about(request):
    about = About.objects.last()
    return render(request, 'shop/about.html', {'about': about})


def info(request):
    info = Info.objects.last()
    return render(request, 'shop/info.html', {'info': info})