import datetime as dt
from src.daylight import is_light_enough

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

def test_daylight_single_day(datostr="2026-05-19"):
    dato = dt.date.fromisoformat(datostr)
    for klokkeslett in range(0,24):
        act_date_time = dt.datetime.combine(
            dato,
            dt.time(klokkeslett, 0),
            tzinfo=dt.UTC,
        )  
        result = is_light_enough(act_date_time=act_date_time)     
        if result == False:
            print(datostr, klokkeslett, result)


def show_daylight_single_day(datostr):
    dato = dt.date.fromisoformat(datostr)
    act_date_time = dt.datetime.combine(
        dato,
        dt.time(0, 0),
        tzinfo=dt.UTC,
    )  
    result = is_light_enough(act_date_time=act_date_time)     


test_daylight_single_day(datostr="2026-05-18")
