from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Header, Category, Product, ProductImage


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'url', 'get_image']

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.thumbnail.url}" width="50", height=auto>')

    get_image.short_description = "Изображение"

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated', 'get_image']
    list_filter = ['available', 'category', 'created', 'updated']
    search_fields = ('name', 'category__name', 'article')
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True
    inlines = [ProductImageAdmin]

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.thumbnail.url}" width="50", height=auto>')

    get_image.short_description = "Изображение"


admin.site.site_title = 'Sabinur Store'
admin.site.site_header = 'Sabinur Store'