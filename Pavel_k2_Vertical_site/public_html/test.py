import openrouteservice

# Ваш API-ключ OpenRouteService
api_key = "5b3ce3597851110001cf6248aa5159d26bb141e28af00c07d47a0ad4"
client = openrouteservice.Client(key=api_key)

# Функция для поиска координат по названию города через OpenRouteService

def get_coordinates(city):
    result = client.pelias_search(city)
    if result and 'features' in result and result['features']:
        coords = result['features'][0]['geometry']['coordinates']
        return [coords[0], coords[1]]  # [долгота, широта]
    return None
# Города
city1 = "Сочи"
city2 = "Минеральные Воды"

# Получаем координаты городов
coords1 = get_coordinates(city1)
coords2 = get_coordinates(city2)

if coords1 and coords2:
    # Запрос маршрута
    route = client.directions([coords1, coords2])

    # Извлечение расстояния (в метрах)
    distance = route['routes'][0]['summary']['distance']
    print(f"Расстояние между {city1} и {city2}: {distance / 1000:.2f} км")
else:
    print("Не удалось определить координаты одного из городов.")
