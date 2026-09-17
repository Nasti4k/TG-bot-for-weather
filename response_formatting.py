
from collections import Counter

def summarize(day_items):
    temps = [x["main"]["temp"] for x in day_items]
    descs = [x["weather"][0]["description"] for x in day_items]
    speed_wind = [x["wind"]["speed"] for x in day_items]
    wind_deg=[x["wind"].get("deg", 0) for x in day_items]
    humidity=[x["main"]["humidity"] for x in day_items]

    
    t_min = min(temps)
    t_max = max(temps)

    
    main_desc = Counter(descs).most_common(1)[0][0]
    main_wind_deg=Counter(wind_deg).most_common(1)[0][0]
    main_speed_wind = sum(speed_wind) / len(speed_wind)
    main_humidity = sum(humidity) / len(humidity)       
    
    return f"Погода: {main_desc}\nТемпература от {t_min:.1f}°C до {t_max:.1f}°C\nСкорость ветра:{main_speed_wind:.0f} м/с,{wind_speed_new(main_speed_wind)}\nНаправление ветра:{wind_deg_new(main_wind_deg)}\nВлажность:{main_humidity:.1f},{humidity_new(main_humidity)}"


def wind_speed_new(wind):
    if wind==0:
        return 'Штиль'
    elif wind<=2:
        return 'Легкий ветер'
    elif wind<=5:
        return 'Слабый ветер'
    elif wind<=7:
        return 'Умеренный ветер'
    elif wind<=15:
        return 'Сильный ветер'
    elif wind<=29:
        return 'Шторм'
    else:
        return 'Ураган'

def wind_deg_new(deg):
    dirs = ["Северный", "Северо-Восточный", "Восточный", "Юго-Восточный",
            "Южный", "Юго-Западный", "Западный", "Северо-Западный"]
    return dirs[round(deg / 45) % 8]


def humidity_new(humidity):
    if humidity<30:
        return 'Низкая влажность'
    elif humidity<=60:
        return 'Норма влажности'
    else:
        return 'Высокая влажность'
    