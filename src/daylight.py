import datetime as dt
import requests

HYTTA_LAT = 64.010927
HYTTA_LNG = 9.884884


# Vi jobber alltid med UTC-tid.
def is_daylight(lat=HYTTA_LAT, lng=HYTTA_LNG, act_date_time=dt.datetime.now(dt.UTC)):
    parameters = {
        "lat" : lat,
        "lng" : lng,
        "date" : act_date_time.strftime("%Y-%m-%d"),
        "formatted" : 0
    }

    
    response = requests.get(
        "https://api.sunrise-sunset.org/json",
        params=parameters,
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    print(data)
    sunrise_time = dt.datetime.fromisoformat(
        data["results"]["civil_twilight_begin"]
    ).strftime("%H:%M")

    sunset_time = dt.datetime.fromisoformat(
        data["results"]["civil_twilight_end"]
    ).strftime("%H:%M")

    print(f"sunrise_time: {sunrise_time}")
    print(f"sunset_time: {sunset_time}")

    return (
        sunrise_time < act_date_time.strftime("%H:%M") < sunset_time
        or sunset_time == "00:00"
        or sunrise_time > sunset_time
    )
is_daylight()