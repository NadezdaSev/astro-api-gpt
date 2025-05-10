from fastapi import FastAPI
from astro_calc import (
    calculate_natal,
    calculate_transits,
    calculate_relocation,
    calculate_astrography,
    calculate_solar,
    calculate_progression,
)

app = FastAPI()

@app.post("/natal")
async def get_natal(data: dict):
    return calculate_natal(data)

@app.post("/transits")
async def get_transits(data: dict):
    return calculate_transits(data)

@app.post("/relocation")
async def get_relocation(data: dict):
    return calculate_relocation(data)

@app.post("/astrography")
async def get_astrography(data: dict):
    return calculate_astrography(data)

@app.post("/solar")
async def get_solar(data: dict):
    return calculate_solar(data)

@app.post("/progression")
async def get_progression(data: dict):
    return calculate_progression(data)
