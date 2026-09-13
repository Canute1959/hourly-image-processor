import datetime as dt
import requests
import time
HYTTA_LAT = 64.010927
HYTTA_LNG = 9.884884


# Vi jobber alltid med UTC-tid.
def is_light_enough(
    lat=HYTTA_LAT, 
    lng=HYTTA_LNG, 
    act_date_time=None,
    ):
    """
    Returnerer True når det er civil twilight eller lysere.

    Alle tider håndteres i UTC.
    """

    if act_date_time is None:
        act_date_time = dt.datetime.now(dt.UTC)

    # Sørg for timezone-aware datetime
    if act_date_time.tzinfo is None:
        raise ValueError("act_date_time må ha timezone, f.eks. dt.UTC")

    act_date_time = act_date_time.astimezone(dt.UTC)

    parameters = {
        "lat" : lat,
        "lng" : lng,
        "date" : act_date_time.strftime("%Y-%m-%d"),
        "tz" : "UTC",
    }

    
    response = requests.get(
        "https://api.sunrise-sunset.org/v2",
        params=parameters,
        timeout=10,
    )
    response.raise_for_status()


    data = response.json()
    print(data)
# TODO sørge for at det blir tatt bilde selv når vi ikke får svar fra API
#      Dette må skje i den rutinen som kaller opp funksjon is_light_enough
    if data.get("status") != "OK":
        raise RuntimeError(
            f"Feil fra sunrise-sunset.org: {data.get('status')}"
        )

    results = data["results"]

    civil_begin_str = results["civil_twilight_begin"]
    civil_end_str = results["civil_twilight_end"]

    # API-et bruker hos deg 00:00 / 00:00 i perioden
    # hvor solen aldri går mer enn 6 grader under horisonten.
    if (
        civil_begin_str.endswith("T00:00:00+00:00")
        and civil_end_str.endswith("T00:00:00+00:00")
    ):
        return True

    print(f' {act_date_time} : civil_twilight_begin: {dt.datetime.fromisoformat(data["results"]["civil_twilight_begin"]).strftime("%H:%M")} \
            civil_twilight_end: {dt.datetime.fromisoformat(data["results"]["civil_twilight_end"]).strftime("%H:%M")} \
            sunrise: {dt.datetime.fromisoformat(data["results"]["sunrise"]).strftime("%H:%M")} \
            sunset : {dt.datetime.fromisoformat(data["results"]["sunset"]).strftime("%H:%M")} ')

    civil_begin = dt.datetime.fromisoformat(civil_begin_str)
    civil_end = dt.datetime.fromisoformat(civil_end_str)

    # Vanlig tilfelle:
    #
    #   03:46 -------- 18:47
    #
    if civil_begin <= civil_end:
        return civil_begin <= act_date_time <= civil_end

 # Sommer ved høy breddegrad:
    #
    # civil_end   = 22:35
    # civil_begin = 23:57
    #
    # Da er det lyst:
    #
    # 00:00 ---------- 22:35
    # 23:57 ---------- 24:00
    #
    # og for mørkt bare mellom 22:35 og 23:57.
    return (
        act_date_time <= civil_end
        or act_date_time >= civil_begin
    )
def test_daylight_all_year():
    year = 2026
    current = dt.date(year, 1, 1)
    one_day = dt.timedelta(days=1)
    while current.year == year:
        if current.month != 5:
            current += one_day
            continue
        # print(current)

        act_date_time = dt.datetime.combine(
            current,
            dt.time(12, 0),
            tzinfo=dt.UTC,
        )       
        print(current, is_light_enough(act_date_time=act_date_time))
        current += one_day
        time.sleep(1)

test_daylight_all_year()