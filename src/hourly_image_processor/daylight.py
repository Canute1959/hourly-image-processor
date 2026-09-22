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
    https://api.sunrise-sunset.org/v2?date=2026-09-20&lat=64.01&lng=9.88&tz=UTC
    Dokumentasjon av api https://sunrise-sunset.org/api
    Alle tider håndteres i UTC.
    """

    if act_date_time is None:
        act_date_time = dt.datetime.now(dt.UTC)

    try: 
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
        # print(data)
    # TODO sørge for at det blir tatt bilde selv når vi ikke får svar fra API
    #      Dette må skje i den rutinen som kaller opp funksjon is_light_enough
        if "error" in data:
            raise RuntimeError(
                f"{data.get('error')}: {data.get('message')}"
            )
        civil_begin_str = data["civil_twilight_begin"]
        civil_end_str = data["civil_twilight_end"]

        # Ingen civil twilight-grenser:
        # sola kommer ikke 6 grader under horisonten.
        if civil_begin_str is None and civil_end_str is None:
            return True

        # Sikkerhet dersom bare én av dem mangler
        if civil_begin_str is None or civil_end_str is None:
            raise RuntimeError(
                f"Uventede twilight-verdier: "
                f"begin={civil_begin_str}, end={civil_end_str}"
            )

        print(
            f'{act_date_time} : '
            f'civil_twilight_begin: {dt.datetime.fromisoformat(data["civil_twilight_begin"]).strftime("%H:%M")} '
            f'civil_twilight_end: {dt.datetime.fromisoformat(data["civil_twilight_end"]).strftime("%H:%M")} '
            f'sunrise: {dt.datetime.fromisoformat(data["sunrise"]).strftime("%H:%M")} '
            f'sunset : {dt.datetime.fromisoformat(data["sunset"]).strftime("%H:%M")} '
        )

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
    except (
        requests.RequestException,
        KeyError,
        ValueError,
        TypeError,
    ) as e:
        print(f"Error checking daylight: {e}")
        print("Assuming sufficient light - taking photo.")
        return True