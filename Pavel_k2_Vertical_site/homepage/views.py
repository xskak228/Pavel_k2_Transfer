import json
import os
from django.conf import settings
from datetime import timedelta
import openrouteservice
from urllib.parse import unquote
from django.utils.timezone import now

from .models import Booking, Pricing
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader


api_key = "5b3ce3597851110001cf6248aa5159d26bb141e28af00c07d47a0ad4"
client = openrouteservice.Client(key=api_key)

def get_coordinates(city):
    result = client.pelias_search(city)
    if result and 'features' in result and result['features']:
        coords = result['features'][0]['geometry']['coordinates']
        return [coords[0], coords[1]]  # [долгота, широта]
    return None

def get_kilomiters(city_from, city_to):
    coords1 = get_coordinates(city_from)
    coords2 = get_coordinates(city_to)

    if coords1 and coords2:
        route = client.directions([coords1, coords2])
        distance = route['routes'][0]['summary']['distance']
        return distance / 1000
    else:
        return None

def get_price(km, num_people, luggage, shild_seat, pet):
    pricing = Pricing.objects.first()
    price = 0
    price += int(km) * int(pricing.price_per_km)
    price += int(num_people) * int(pricing.price_per_passenger)
    price += int(luggage) * int(pricing.price_per_baggage)
    if shild_seat:
        price += int(pricing.price_for_child_seat)
    if pet:
        price += int(pricing.price_for_pets)
    return price


def index(request):
    template = "homepage/index.html"
    error_message = None

    if request.method == "POST":
        from_location = request.POST.get("from_location")
        to_location = request.POST.get("to_location")
        num_people = request.POST.get("num_people")

        # Загружаем список городов
        cities_path = os.path.join(settings.BASE_DIR, "static", "cities.json")
        with open(cities_path, "r", encoding="utf-8") as f:
            cities = json.load(f)

        if from_location not in cities:
            error_message = f"Город отправления '{from_location}' не найден! Пожалуйста выберите город из списка"
        elif to_location not in cities:
            error_message = f"Город назначения '{to_location}' не найден! Пожалуйста выберите город из списка"
        else:
            # Сохраняем в сессии
            request.session["from_location"] = from_location
            request.session["to_location"] = to_location
            request.session["num_people"] = num_people

            return redirect(f"/form/{from_location}---{to_location}")  # Переход на вторую страницу
    return render(request, template, context={"error_message": error_message})

def form(request, city_from, city_to):
    # Загружаем список городов
    cities_path = os.path.join(settings.BASE_DIR, "static", "cities.json")
    with open(cities_path, "r", encoding="utf-8") as f:
        cities = json.load(f)

    if city_from not in cities:
        raise Http404("Неправильно указан город. Пожалуйста не играйтесь с URL, если же это ошибка сайта - обратитесь в поддержку")
    elif city_to not in cities:
        raise Http404("Неправильно указан город. Пожалуйста не играйтесь с URL, если же это ошибка сайта - обратитесь в поддержку")

    template = "formcity/index.html"
    tomorrow = now().date() + timedelta(days=1)
    error_message = None

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        date = request.POST.get("date")
        time = request.POST.get("time")
        from_location = request.POST.get("from_location")
        to_location = request.POST.get("to_location")
        num_people = request.POST.get("num_people")
        luggage = request.POST.get("luggage")
        child_seat = request.POST.get("child_seat") == "Да"
        pet = request.POST.get("pet") == "Да"

        kilometers = get_kilomiters(from_location, to_location)
        price = get_price(kilometers, num_people, luggage, child_seat, pet)
        status = "ПредПоказЦены"


        # Загружаем список городов
        cities_path = os.path.join(settings.BASE_DIR, "static", "cities.json")
        with open(cities_path, "r", encoding="utf-8") as f:
            cities = json.load(f)

        if from_location not in cities:
            error_message = f"Город отправления '{from_location}' не найден! Пожалуйста выберите город из списка"
        elif to_location not in cities:
            error_message = f"Город назначения '{to_location}' не найден! Пожалуйста выберите город из списка"
        else:
            booking = Booking.objects.create(
                name=name,
                phone=phone,
                date=date,
                time=time,
                from_location=from_location,
                to_location=to_location,
                num_people=num_people,
                luggage=luggage,
                child_seat=child_seat,
                pet=pet,
                price=price,
                status=status
            )

            request.session["from_location"] = ""
            request.session["to_location"] = ""
            request.session["num_people"] = ""

            return redirect("total_price", booking_id=booking.id)  # Замените на ваш реальный URL для подтверждения
    city_from = unquote(city_from)
    city_to = unquote(city_to)

    if city_from and city_to:
        from_location = city_from
        to_location = city_to
    else:
        from_location = request.session.get("from_location", "")
        to_location = request.session.get("to_location", "")
    num_people = request.session.get("num_people", "")

    context = {
        "error_message": error_message,
        "from_location": from_location,
        "to_location": to_location,
        "num_people": num_people,
        'tomorrow': str(tomorrow)
    }

    return render(request, template, context)


def total_price(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        booking.status = "ЗаявкаОтправленаБоту"
        booking.save()
        return redirect("../..")  # Заменить на страницу успешной заявки

    template = "formcity/total_price.html"

    context = {
        "price": booking.price,
        "booking_id": booking.id
    }

    return render(request, template, context)