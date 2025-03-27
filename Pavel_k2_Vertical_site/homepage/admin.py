from django.contrib import admin
from .models import Booking, Pricing
from django.core.exceptions import ValidationError


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("unique_number", "created_at", "name", "phone", "from_location", "to_location", "date", "time", "price", "status",)
    list_filter = ("from_location", "to_location", "date", "status")
    search_fields = ("unique_number", "name", "phone")
    readonly_fields = ("unique_number", "created_at", "updated_at")


@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change and Pricing.objects.exists():
            raise ValidationError("Можно создать только одну запись в этой таблице.")
        super().save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if Pricing.objects.exists():
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        if Pricing.objects.count() == 1:
            raise ValidationError("Невозможно удалить единственную запись.")
        super().delete_model(request, obj)

    list_display = ("price_per_km", "price_per_passenger", "price_per_baggage", "price_for_pets", "price_for_child_seat")