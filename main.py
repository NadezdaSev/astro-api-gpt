from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from astro_calc import calculate_natal, calculate_transits, calculate_relocation, calculate_astrography, calculate_solar, calculate_progression

app = FastAPI()

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

@app.post("/natal")
def get_natal_chart(data: BirthData):
    return calculate_natal(data)

@app.post("/transits")
def get_transits(data: TransitData):
    return calculate_transits(data)

@app.post("/relocation")
def get_relocation(data: RelocationData):
    return calculate_relocation(data)

@app.post("/astrography")
def get_astrography(data: BirthData):
    return calculate_astrography(data)

@app.post("/solar")
def get_solar(data: TransitData):
    return calculate_solar(data)

@app.post("/progression")
def get_progression(data: TransitData):
    return calculate_progression(data)
