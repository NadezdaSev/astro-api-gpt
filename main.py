from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import swisseph as swe
import math

app = FastAPI()
swe.set_ephe_path('.')  # путь к эфемеридам (если будут .se1 файлы)

class BirthData(BaseModel):
    date: str
    time: str
    lat: float
    lon: float
    tz: float

class TransitData(BirthData):
    target_date: str

class RelocationData(BirthData):
    rel_lat: float
    rel_lon: float

def get_julian_day(date, time, tz):
    dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    return swe.julday(dt.year, dt.month, dt.day, dt.hour - tz + dt.minute / 60)

def get_planets(jd):
    result = {}
    for p in range(swe.SUN, swe.PLUTO + 1):
        pos, _ = swe.calc_ut(jd, p)
        name = swe.get_planet_name(p)
        result[name] = round(pos[0], 4)
    return result

def get_aspects(planets):
    aspect_list = [0, 60, 90, 120, 180]
    aspects = []
    keys = list(planets.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            diff = abs(planets[keys[i]] - planets[keys[j]])
            diff = diff if diff <= 180 else 360 - diff
            for asp in aspect_list:
                if abs(diff - asp) <= 5:
                    aspects.append({
                        "between": [keys[i], keys[j]],
                        "aspect": asp,
                        "orb": round(abs(diff - asp), 2)
                    })
    return aspects

def get_houses(jd, lat, lon):
    houses, _ = swe.houses(jd, lat, lon)
    return {"ASC": round(houses[0], 2), "MC": round(houses[10], 2)}

def get_fixed_stars(jd):
    stars = {
        "Regulus": 150.0,
        "Spica": 204.0,
        "Antares": 250.0
    }
    return stars

def get_astrodyne(planets):
    weights = {}
    for name, deg in planets.items():
        score = 10 - abs((deg % 30) - 15) / 1.5
        weights[name] = round(score, 2)
    return weights

@app.post("/natal")
def natal(data: BirthData):
    jd = get_julian_day(data.date, data.time, data.tz)
    planets = get_planets(jd)
    aspects = get_aspects(planets)
    houses = get_houses(jd, data.lat, data.lon)
    stars = get_fixed_stars(jd)
    astrodyne = get_astrodyne(planets)
    return {
        "julian_day": jd,
        "planets": planets,
        "aspects": aspects,
        "houses": houses,
        "fixed_stars": stars,
        "astrodyne": astrodyne
    }

@app.post("/transits")
def transits(data: TransitData):
    trans_jd = get_julian_day(data.target_date, data.time, data.tz)
    planets = get_planets(trans_jd)
    return {
        "target_day": trans_jd,
        "transits": planets
    }

@app.post("/relocation")
def relocation(data: RelocationData):
    jd = get_julian_day(data.date, data.time, data.tz)
    houses = get_houses(jd, data.rel_lat, data.rel_lon)
    return {
        "relocated_asc_mc": houses
    }

@app.post("/astrography")
def astro_lines(data: BirthData):
    jd = get_julian_day(data.date, data.time, data.tz)
    lines = []
    for planet_id in range(swe.SUN, swe.PLUTO + 1):
        name = swe.get_planet_name(planet_id)
        for lat in range(-60, 61, 30):
            for lon in range(-180, 181, 60):
                houses, _ = swe.houses(jd, lat, lon)
                lines.append({
                    "planet": name,
                    "lat": lat,
                    "lon": lon,
                    "ASC": round(houses[0], 1),
                    "MC": round(houses[10], 1)
                })
    return {"lines": lines}
