import random

from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator
from django.db import models

def generate_unique_number():
    while True:
        number = ''.join(random.choices('0123456789', k=10))  # Генерация числа
        if not Booking.objects.filter(unique_number=number).exists():
            return number

# Create your models here.
class Booking(models.Model):
    unique_number = models.CharField(max_length=10, unique=True, default=generate_unique_number, editable=False, verbose_name="Индивидуальный номер")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Время создания заявки", verbose_name="Заявка создана")
    from_location = models.CharField(max_length=100, help_text="", verbose_name="Откуда")
    to_location = models.CharField(max_length=100, help_text="", verbose_name="Куда")
    name = models.CharField(max_length=255, help_text="", verbose_name="Имя")
    phone = models.CharField(max_length=20, help_text="", verbose_name="Телефон")
    date = models.DateField(verbose_name="Дата поездки", help_text="Время когда начинается поездка")
    time = models.TimeField(verbose_name="Время поездки", help_text="Дата когда начинается поездка")
    tariff = models.CharField(max_length=255, help_text="", verbose_name="Тариф")
    num_people = models.PositiveIntegerField( help_text="", verbose_name="Количество человек")
    luggage = models.PositiveIntegerField( help_text="", verbose_name="Количество багажа")
    child_seat = models.BooleanField(default=False, help_text="", verbose_name="Детское кресло")
    pet = models.BooleanField(default=False, help_text="", verbose_name="Животное")
    price = models.PositiveIntegerField( help_text="Предварительаня цена, НЕ ИЗМЕНЯТЬ!", verbose_name="Цена")
    sale_price = models.PositiveIntegerField( help_text="Предварительаня цена со Скидкой, НЕ ИЗМЕНЯТЬ!", verbose_name="Цена со скидкой")
    comment = models.CharField(max_length=1000, help_text="Комментарий от клиента", verbose_name="Комментарий")
    updated_at = models.DateTimeField(auto_now=True, help_text="Время изменения статуса с ЖдемПодтверждения на ЗаявкаОтправленаБоту", verbose_name="Статус изменен")
    status = models.CharField(max_length=100, help_text="Статус заявки", verbose_name="Статус")


    def __str__(self):
        return f"{self.name} - {self.from_location} -> {self.to_location} ({self.date} {self.time})"


class Pricing(models.Model):
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2, help_text="", verbose_name="Цена за километр", validators=[MinValueValidator(1)])
    price_per_passenger = models.DecimalField(max_digits=10, decimal_places=2, help_text="", verbose_name="Цена за 1 пассажира", validators=[MinValueValidator(1)])
    price_per_baggage = models.DecimalField(max_digits=10, decimal_places=2, help_text="", verbose_name="Цена за 1 багаж", validators=[MinValueValidator(1)])
    price_for_pets = models.DecimalField(max_digits=10, decimal_places=2, help_text="", verbose_name="Цена за домашних животных", validators=[MinValueValidator(1)])
    price_for_child_seat = models.DecimalField(max_digits=10, decimal_places=2, help_text="", verbose_name="Цена за детское кресло", validators=[MinValueValidator(1)])
    tariff_price_econom = models.DecimalField(max_digits=10, decimal_places=2, help_text="", verbose_name="Цена за ЭКОНОМ тариф", validators=[MinValueValidator(1)])
    tariff_price_standart = models.DecimalField(max_digits=10, decimal_places=2, help_text="", verbose_name="Цена за СТАНДАРТ тариф", validators=[MinValueValidator(1)])
    tariff_price_comfort = models.DecimalField(max_digits=10, decimal_places=2, help_text="", verbose_name="Цена за КОМФОРТ тариф", validators=[MinValueValidator(1)])
    tariff_price_miniven = models.DecimalField(max_digits=10, decimal_places=2, help_text="", verbose_name="Цена за МИНИВЕН тариф", validators=[MinValueValidator(1)])
    tariff_price_biznes = models.DecimalField(max_digits=10, decimal_places=2, help_text="", verbose_name="Цена за БИЗНЕС тариф", validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Расценка"


class MainInfo(models.Model):
    Company_Phone_Number = models.CharField(max_length=100, help_text="В формате +7(123)456-78-90, Будет отображаться на сайте поэтому красиво", verbose_name="Номер телефона Компании")
    Url_Telegram = models.CharField(max_length=100, help_text="В формате https://telegram.org", verbose_name="Ссылка на телеграмм канал/аккаунт")
    Url_WhatsApp = models.CharField(max_length=100, help_text="В формате https://whatsapp.org", verbose_name="Ссылка на Ватцап канал/аккаунт")

    def __str__(self):
        return f"Основная информация"


class MainSettings(models.Model):
    ApiKey_OpenRouteService = models.CharField(max_length=400, help_text="Api ключ для работы сайта через сервси OpenRouteService для вычисления расстояния https://openrouteservice.org/", verbose_name="Api Ключ OpenRouteService")
    ApiKey_TgBot = models.CharField(max_length=400, help_text="", verbose_name="Api Ключ Телеграмм Бота")
    ChatID_Telegram = models.CharField(max_length=50, help_text="", verbose_name="ID Чата для работы телеграмм бота")

    def __str__(self):
        return f"Основные Настройки"


class SupportInfo(models.Model):
    Phone_Number_Support = models.CharField(max_length=100, help_text="Телефон для связи с ТП (Техническая Поддержка), в формате +7(123)456-78-90", verbose_name="Телефон для связи с ТП")
    Url_Telegram_Support = models.CharField(max_length=300, help_text="В формате https://telegram.org", verbose_name="Ссылка на телеграмм бота ТП")
    Url_YandexForm_Support = models.CharField(max_length=300, help_text="В формате https://", verbose_name="Ссылка на Яндекс Форму ТП")

    def __str__(self):
        return f"Настройки/Информация Технической поддержки"


class Article(models.Model):
    title = models.CharField('Название', max_length=100)
    CompanyPolicy = RichTextField('Политика Компании', blank=True)
    PrivacyPolicy = RichTextField('Политика Конфиденциальности', blank=True)
    HelpTextToSupport = RichTextField('Вспомагательынй текст для ТП', blank=True)

    class Meta:
        verbose_name = 'Контент сайта'
        verbose_name_plural = 'Контент сайта'

    def __str__(self):
        return self.title