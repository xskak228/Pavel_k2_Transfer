from django.contrib import admin
from .models import Booking, Pricing, MainInfo, SupportInfo, Article, MainSettings
from django.core.exceptions import ValidationError


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("unique_number", "created_at", "name", "phone", "tariff", "from_location", "to_location", "date", "time", "price", "status")
    list_filter = ("from_location", "to_location", "date", "status", "tariff")
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

    list_display = ("price_per_km", "price_per_passenger", "price_per_baggage", "price_for_pets", "price_for_child_seat",
                    "tariff_price_econom", "tariff_price_standart", "tariff_price_comfort", "tariff_price_miniven", "tariff_price_biznes")


@admin.register(MainInfo)
class MainInfoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change and MainInfo.objects.exists():
            raise ValidationError("Можно создать только одну запись в этой таблице.")
        super().save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if MainInfo.objects.exists():
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        if MainInfo.objects.count() == 1:
            raise ValidationError("Невозможно удалить единственную запись.")
        super().delete_model(request, obj)

    list_display = ("Company_Phone_Number", "Url_Telegram", "Url_WhatsApp")


@admin.register(MainSettings)
class MainSettingsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change and MainSettings.objects.exists():
            raise ValidationError("Можно создать только одну запись в этой таблице.")
        super().save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if MainSettings.objects.exists():
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        if MainSettings.objects.count() == 1:
            raise ValidationError("Невозможно удалить единственную запись.")
        super().delete_model(request, obj)

    list_display = ("ApiKey_OpenRouteService", "ApiKey_TgBot", "ChatID_Telegram")


@admin.register(SupportInfo)
class SupportInfoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change and SupportInfo.objects.exists():
            raise ValidationError("Можно создать только одну запись в этой таблице.")
        super().save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if SupportInfo.objects.exists():
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        if SupportInfo.objects.count() == 1:
            raise ValidationError("Невозможно удалить единственную запись.")
        super().delete_model(request, obj)

    list_display = ("Phone_Number_Support", "Url_Telegram_Support", "Url_YandexForm_Support")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)