import random

from django.db import models

def generate_unique_number():
    while True:
        number = ''.join(random.choices('0123456789', k=10))  # Генерация числа
        if not Booking.objects.filter(unique_number=number).exists():
            return number

# Create your models here.
class Booking(models.Model):

    unique_number = models.CharField(max_length=10, unique=True, default=generate_unique_number, editable=False, verbose_name="Индивидуальный номер")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Заявка создана")
    from_location = models.CharField(max_length=100, verbose_name="Откуда")
    to_location = models.CharField(max_length=100, verbose_name="Куда")
    name = models.CharField(max_length=255, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    date = models.DateField(verbose_name="Дата поездки")
    time = models.TimeField(verbose_name="Время поездки")
    num_people = models.PositiveIntegerField(verbose_name="Количество человек")
    luggage = models.PositiveIntegerField(verbose_name="Количество багажа")
    child_seat = models.BooleanField(default=False, verbose_name="Детское кресло")
    pet = models.BooleanField(default=False, verbose_name="Животное")
    price = models.PositiveIntegerField(verbose_name="Цена")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Статус изменен")
    status = models.CharField(max_length=100, verbose_name="Статус")


    def __str__(self):
        return f"{self.name} - {self.from_location} -> {self.to_location} ({self.date} {self.time})"


class Pricing(models.Model):
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за километр")
    price_per_passenger = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за 1 пассажира")
    price_per_baggage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за 1 багаж")
    price_for_pets = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за домашних животных")
    price_for_child_seat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за детское кресло")
    tariff_price_econom = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за ЭКОНОМ тариф")
    tariff_price_standart = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за СТАНДАРТ тариф")
    tariff_price_comfort = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за КОМФОРТ тариф")
    tariff_price_miniven = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за МИНИВЕН тариф")
    tariff_price_biznes = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за БИЗНЕС тариф")

    def __str__(self):
        return f"Тариф {self.id}"
