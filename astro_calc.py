from fastapi import HTTPException
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.const import SIDEREAL
from datetime import datetime


def normalize_date(date_str):
    """Преобразует любую дату в формат DD/MM/YYYY для flatlib."""
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            parsed = datetime.strptime(date_str, fmt)
            return parsed.strftime("%d/%m/%Y")
        except ValueError:
            continue
    raise ValueError(f"Неподдерживаемый формат даты: {date_str}")


def calculate_natal(data):
    try:
        flatlib_date = normalize_date(data['date'])
        dt = Datetime(flatlib_date, data['time'], data['tz'])
        pos = GeoPos(str(data['lat']), str(data['lon']))
        chart = Chart(dt, pos, hsys='P')

        result = {
            'planets': {obj: chart.get(obj).lon for obj in chart.objects},
            'houses': {
                'ASC': chart.get('ASC').lon,
                'MC': chart.get('MC').lon
            },
            'aspects': [],  # Добавим позже
            'fixed_stars': {},  # Заглушка
            'astrodyne': {}     # Заглушка
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при расчёте натальной карты: {str(e)}")
