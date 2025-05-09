def calculate_natal(data):
    return {"message": "Натальная карта рассчитана."}

def calculate_transits(data):
    return {"transits": {"Mars": 120.5}}

def calculate_relocation(data):
    return {"relocated_asc_mc": {"ASC": 18.4, "MC": 92.1}}

def calculate_astrography(data):
    return {
        "lines": [
            {"planet": "Mars", "lat": 40.0, "lon": -74.0, "ASC": 120, "MC": 150}
        ]
    }

def calculate_solar(data):
    return {"solar_chart": {"Sun": 5.1, "Moon": 12.2}}

def calculate_progression(data):
    return {"progressed_chart": {"Sun": 15.5, "Mercury": 22.3}}
