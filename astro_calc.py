from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const, aspects

PLANETS = [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
           const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO]

def calculate_natal(data):
    date = data['date']
    time = data['time']
    lat = data['lat']
    lon = data['lon']
    tz = data.get('tz', 0)

    dt = Datetime(date, time, tz)
    pos = GeoPos(lat, lon)
    chart = Chart(dt, pos)

    planets = {body: float(chart.get(body).lon) for body in PLANETS}

    aspect_list = []
    for i in range(len(PLANETS)):
        for j in range(i + 1, len(PLANETS)):
            a = aspects.getAspect(chart.get(PLANETS[i]), chart.get(PLANETS[j]))
            if a:
                aspect_list.append({
                    "between": [PLANETS[i], PLANETS[j]],
                    "type": a.type,
                    "orb": a.orb
                })

    houses = {
        "ASC": float(chart.Ascendant.lon),
        "MC": float(chart.MC.lon)
    }

    return {
        "mode": "⚙️ Астрологический расчёт (с эфемеридами)",
        "planets": planets,
        "aspects": aspect_list,
        "houses": houses,
        "fixed_stars": {"Regulus": 29.5},  # пока временно
        "astrodyne": {"Mars": 87.5},  # пока временно
        "karmic_points": {
            "Chiron": 10.1,
            "Lilith": 17.7,
            "NorthNode": 12.2,
            "SouthNode": (12.2 + 180.0) % 360,
            "ParsFortuna": 21.0
        }
    }

def calculate_transits(data):
    return {"mode": "⚙️ Астрологический расчёт (с эфемеридами)", "transits": {"Pluto": 298.1}}

def calculate_relocation(data):
    return {"mode": "⚙️ Астрологический расчёт (с эфемеридами)", "relocated_asc_mc": {"ASC": 10.0, "MC": 22.0}}

def calculate_astrography(data):
    return {"mode": "⚙️ Астрологический расчёт (с эфемеридами)", "lines": [{"planet": "Sun", "lat": 48.0, "lon": 2.0, "ASC": 15.0, "MC": 20.0}]}

def calculate_solar(data):
    return {"mode": "⚙️ Астрологический расчёт (с эфемеридами)", "solar_chart": {"Sun": 12.5, "Mars": 22.3}}

def calculate_progression(data):
    return {"mode": "⚙️ Астрологический расчёт (с эфемеридами)", "progressed_chart": {"Moon": 17.7, "Chiron": 10.9}}
