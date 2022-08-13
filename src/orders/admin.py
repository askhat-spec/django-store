import csv
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from .models import Order, OrderItem


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Экспортировать выбранные в CSV файл"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['get_image', 'get_article', 'price', 'quantity']
    readonly_fields = ['get_image', 'get_article', 'price', 'quantity']

    def get_image(self, obj):
        image = f'<img src="{obj.product.thumbnail.url}" width="50", height=auto>'
        return mark_safe(f'<a href="{obj.product.get_absolute_url()}">{image}</a>')
    
    def get_article(self, obj):
        return str(obj.product.article)

    get_image.short_description = "Изображение"
    get_article.short_description = "Артикул"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'phone', 'city', 'address', 'paid',
        'created',
    ]
    list_filter = ['paid', 'created']
    inlines = [OrderItemInline]
    actions = ["export_as_csv"]
    save_on_top = True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "first_name", "last_name", 'email', 'phone',
                'city', 'address', 'created', 'updated',
                ]
        else:
            return []
