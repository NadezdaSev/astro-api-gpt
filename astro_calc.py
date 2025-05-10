from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

def calculate_natal(data):
    date = data['date']
    time = data['time']
    lat = data['lat']
    lon = data['lon']
    tz = data['tz']

    dt = Datetime(date, time, tz)
    pos = GeoPos(lat, lon)
    chart = Chart(dt, pos)

    # Планеты
    planets = {}
    for name in const.LIST_OBJECTS:
        obj = chart.get(name)
        planets[name] = obj.lon

    # Аспекты
    aspects = chart.getAspects()

    # Дома
    houses = {
        'ASC': chart.houses.ascendant.lon,
        'MC': chart.houses.midheaven.lon
    }

    return {
        'planets': planets,
        'aspects': [a.__dict__ for a in aspects],
        'houses': houses
    }
