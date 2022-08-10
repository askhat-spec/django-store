import csv
from django.contrib import admin
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
    raw_id_fields = ['product']


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

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "first_name", "last_name", 'email', 'phone',
                'city', 'address', 'created', 'updated',
                ]
        else:
            return []
