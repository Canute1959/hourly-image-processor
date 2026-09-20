import daylight
import datetime as dt

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
        print(current, daylight.is_light_enough(act_date_time=act_date_time))
        current += one_day
        time.sleep(1)

def test_daylight_single_day():
    pass

test_daylight_all_year()