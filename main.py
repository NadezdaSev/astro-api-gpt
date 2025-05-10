from fastapi import FastAPI
from pydantic import BaseModel
from astro_calc import calculate_natal

app = FastAPI()


class BirthData(BaseModel):
    date: str  # формат: "DD/MM/YYYY"
    time: str  # формат: "HH:MM"
    lat: float
    lon: float
    tz: float


@app.post("/natal")
def get_natal(data: BirthData):
    return calculate_natal(data)
