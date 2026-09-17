
from datetime import datetime, timedelta, timezone


def split_forecast(data):
    tz_offset = data["city"]["timezone"]
    today = (datetime.now(timezone.utc) + timedelta(seconds=tz_offset)).date()
    tomorrow = today + timedelta(days=1)
    list_today,list_tomorrow = [],[]
    
    for item in data["list"]:
        dt_utc = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
        dt_local = dt_utc + timedelta(seconds=tz_offset)
        if dt_local.date() == today:
            list_today.append(item)
        elif dt_local.date() == tomorrow:
            list_tomorrow.append(item)
    return list_today,list_tomorrow

