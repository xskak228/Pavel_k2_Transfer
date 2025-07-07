import json
import os

import pytz
from django.conf import settings
from datetime import timedelta, datetime
import openrouteservice
from urllib.parse import unquote, quote
from django.utils.timezone import now
import requests

from .models import Booking, Pricing, MainInfo, MainSettings, SupportInfo, Article
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

# https://openrouteservice.org/
# api_key = "5b3ce3597851110001cf6248aa5159d26bb141e28af00c07d47a0ad4"
api_key = MainSettings.objects.first().ApiKey_OpenRouteService
# settings_ = MainSettings.objects.first()
# api_key = settings_.ApiKey_OpenRouteService if settings_ else "5b3ce3597851110001cf6248aa5159d26bb141e28af00c07d47a0ad4"

# def get_api_key():
#     api_key_bad = "5b3ce3597851110001cf6248aa5159d26bb141e28af00c07d47a0ad4"
#     api_key = MainSettings.objects.first().ApiKey_OpenRouteService
#     return api_key if api_key else api_key_bad

client = openrouteservice.Client(key=api_key)


# function to get coord in city
def get_coordinates(city):
    print("___________________")
    print("f -> get_coordinates")
    city = city.replace("_", " ")
    print("p -> city")
    result = client.pelias_search(city)

    if result and 'features' in result and result['features']:
        coords = result['features'][0]['geometry']['coordinates']
        print("p -> coords -> ", coords)
        return [coords[0], coords[1]]  # [долгота, широта]
    return None


# function to get kilomiters from cities
def get_kilomiters(city_from, city_to):
    print("___________________")
    print("f -> get_kilomiters")
    print("p -> city_from, city_to -> ", city_from, city_to)
    coords1 = get_coordinates(city_from)
    coords2 = get_coordinates(city_to)

    if coords1 and coords2:
        route = client.directions([coords1, coords2])
        distance = route['routes'][0]['summary']['distance']
        print("p -> distance -> ", distance / 1000)
        return distance / 1000
    else:
        print("E -> bad coords")
        return None


# function to get price from prices form
def get_price(km, num_people, luggage, tariff, shild_seat, pet):
    print("___________________")
    print("f -> get_price")
    print("p -> km, num_people, luggage, tariff, shild_seat, pet -> ", km, num_people, luggage, tariff, shild_seat, pet)
    pricing = Pricing.objects.first()
    price = 0
    if "Эконом" in tariff:
        price += int(km) * int(pricing.tariff_price_econom)
    elif "Стандарт" in tariff:
        price += int(km) * int(pricing.tariff_price_standart)
    elif "Комфорт" in tariff:
        price += int(km) * int(pricing.tariff_price_comfort)
    elif "Минивэн" in tariff:
        price += int(km) * int(pricing.tariff_price_miniven)
    elif "Бизнес" in tariff:
        price += int(km) * int(pricing.tariff_price_biznes)
    else:
        return None

    price += int(km) * int(pricing.price_per_km)
    price += int(num_people) * int(pricing.price_per_passenger)
    price += int(luggage) * int(pricing.price_per_baggage)
    if shild_seat:
        price += int(pricing.price_for_child_seat)
    if pet:
        price += int(pricing.price_for_pets)
    print("p -> price ->", price)
    return price



def is_time_in_range(time_str):
    print("___________________")
    print("f -> is_time_in_range")
    print("p -> time_str", time_str)
    try:
        # Преобразуем строку времени в объект datetime.time
        time = datetime.strptime(time_str, "%H:%M").time()
        # Задаем границы
        start_time = datetime.strptime("07:00", "%H:%M").time()
        end_time = datetime.strptime("23:59", "%H:%M").time()
        # Проверка вхождения во временной диапазон
        return start_time <= time <= end_time
    except ValueError:
        print("E -> bad time")
        return False  # если строка времени некорректна


# MainPage - Form, tariffs, routes
def index(request):
    template = "homepage/index.html"
    error_message = None

    if request.method == "POST":
        request.session.flush()

        # from_location = request.POST.get("from_location")
        from_location = "Минеральные_Воды"
        to_location = request.POST.get("to_location")
        num_people = request.POST.get("num_people")

        # Загружаем список городов
        cities_path = os.path.join(settings.STATIC_ROOT_DIR, "cities.json")
        with open(cities_path, "r", encoding="utf-8") as f:
            cities = json.load(f)

        cities_lower = []
        for i in cities:
            cities_lower.append(i.lower())

        if from_location.lower() not in cities_lower:
            error_message = f"Город отправления '{from_location}' не найден! Пожалуйста выберите город из списка"
        elif to_location.lower() not in cities_lower:
            error_message = f"Город назначения '{to_location}' не найден! Пожалуйста выберите город из списка"
        elif from_location.lower() == to_location.lower():
            error_message = f"Нельзя выбрать одинаковые города"
        else:
            # Сохраняем в сессии
            request.session["from_location"] = from_location
            request.session["to_location"] = to_location
            request.session["num_people"] = num_people

            # return redirect(f"/booking/{quote(from_location)}---{quote(to_location)}")
            # return redirect(f"/booking/{from_location}---{to_location}")  # Переход на вторую страницу
            return redirect(form, from_location, to_location)
    return render(request, template, context={"error_message": error_message, "pricing": Pricing.objects.first(), "MainInfo": MainInfo.objects.first()})


# Form - edit form rout
def form(request, city_from, city_to):
    city_from = unquote(city_from, encoding='utf-8')
    city_to = unquote(city_to, encoding='utf-8')

    # Формируем путь к файлу
    cities_path = os.path.join(settings.STATIC_ROOT_DIR, "cities.json")
    print(f"Trying to load cities.json from: {cities_path}")  # Для отладки

    try:
        with open(cities_path, "r", encoding="utf-8") as f:
            cities = json.load(f)
            cities_lower = []
            for i in cities:
                cities_lower.append(i.lower())
    except FileNotFoundError:
        raise Http404(f"Файл cities.json не найден по пути: {cities_path}")

    if city_from.lower() != "минеральные_воды" or city_to.lower() not in cities_lower:
        raise Http404(f"Неправильно указан город. Пожалуйста, не играйтесь с URL. {city_from} -- {city_to}")

    template = "booking/index.html"
    confirm_template = "booking/total_price.html"
    moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
    date_now = moscow_time.date()  # Получаем только дату
    print(date_now)
    error_message = None

    step = request.session.get("step", "form")

    if request.method == "POST":
        if step == "form":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            date = request.POST.get("date")
            time = request.POST.get("time")
            # from_location = request.POST.get("from_location")
            from_location = "Минеральные_Воды"
            to_location = request.POST.get("to_location")
            tariff = request.POST.get("tariff")
            num_people = request.POST.get("num_people")
            luggage = request.POST.get("luggage")
            child_seat = request.POST.get("child_seat") == "Да"
            pet = request.POST.get("pet") == "Да"

            if city_from.lower() != "минеральные_воды" or city_to.lower() not in cities_lower:
                raise Http404(f"Неправильно указан город. Пожалуйста, не играйтесь с URL. {city_from} -- {city_to}")

            # elif date < date_now:
            #     raise Http404(f"Неправильно указана дата. Укажите дату учитывая время по МСК!!!")
            else:
                kilometers = get_kilomiters(from_location, to_location)
                price = get_price(kilometers, num_people, luggage, tariff, child_seat, pet)

                print(tariff, price)
                sale_price = price*0.9 if is_time_in_range(str(time)) and tariff != "Эконом" else 0
                print(sale_price)

                if price is None and kilometers is None:
                    raise Http404(f"Что то пошло не так, пожалуйста попробуйте ще раз, если не получаеться обратитесь в ТП")

                booking = Booking.objects.create(
                    name=name,
                    phone=phone,
                    date=date,
                    time=time,
                    tariff=tariff,
                    from_location=from_location,
                    to_location=to_location,
                    num_people=num_people,
                    luggage=luggage,
                    child_seat=child_seat,
                    pet=pet,
                    price=price,
                    sale_price=sale_price,
                    status="ПредПоказЦены"
                )

                request.session["booking_id"] = booking.id
                request.session["step"] = "confirm"
                return redirect(request.path)  # redirect to self — URL не меняется

        elif step == "confirm":
            booking_id = request.session.get("booking_id")

            if not booking_id:
                request.session["step"] = "form"
                return redirect(request.path)

            #https://api.telegram.org/bot8193779841:AAGpBzV0rRd6O79tziB_rr9H_GBDtVh5qP0/sendMessage?chat_id=1128832540&text=тест
            test = requests.post("https://api.telegram.org/bot8193779841:AAGpBzV0rRd6O79tziB_rr9H_GBDtVh5qP0/sendMessage?chat_id=1128832540&text=тест")
            booking = Booking.objects.get(id=booking_id)
            booking.status = "ЗаявкаОтправленаБоту"
            booking.save()
            request.session.flush()  # Очистить step/booking_id
            return redirect(index)  # Успешная заявка

    # GET запрос:
    if request.session.get("step") == "confirm":
        booking_id = request.session.get("booking_id")

        # Если данных нет — вернуть на первый шаг
        if not booking_id:
            request.session["step"] = "form"
            return redirect(request.path)

        booking = get_object_or_404(Booking, id=booking_id)
        return render(request, confirm_template, {
            "price": booking.price, "sale_price": booking.sale_price, "MainInfo": MainInfo.objects.first()
        })

    # Отрисовать первую форму
    return render(request, template, {
        "error_message": error_message,
        "from_location": unquote(city_from.capitalize()),
        "to_location": unquote(city_to.capitalize()),
        "date_now": str(date_now),
        "MainInfo": MainInfo.objects.first(),
        "pricing": Pricing.objects.first()
    })


def rules(request):
    template = "rules/index.html"
    return render(request, template, context={"Article": Article.objects.first()})