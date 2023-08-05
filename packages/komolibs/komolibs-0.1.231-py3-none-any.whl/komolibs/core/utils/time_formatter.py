from datetime import datetime, time

import pandas as pd


def give_me_time_in_iso(timestamp: float):
    return pd.Timestamp(timestamp, unit="s", tz="UTC").isoformat()


def give_me_a_timestamp_from_this_string(str_date: str):
    return pd.Timestamp(str_date).timestamp()


def the_time_in_iso_now_is():
    _now = datetime.utcnow()
    stamp: pd.Timestamp = \
        pd.Timestamp(_now.year, _now.month, _now.day, _now.hour, _now.minute, _now.second, _now.microsecond)
    return stamp.isoformat()


def the_time_now_is() -> float:
    _now = datetime.utcnow()
    stamp: pd.Timestamp = \
        pd.Timestamp(_now.year, _now.month, _now.day, _now.hour, _now.minute, _now.second, _now.microsecond)
    return stamp.timestamp()


def get_past_by_hour(interval: int = 1):
    _now = datetime.utcnow()
    stamp: pd.Timestamp = \
        pd.Timestamp(_now.year, _now.month, _now.day, _now.hour, _now.minute, _now.second, _now.microsecond)

    result: pd.Timestamp = stamp - pd.Timedelta(hours=interval)
    return result.timestamp()


# def secs_until_next_oclock():
#     this_hour: pd.Timestamp = pd.Timestamp.utcnow().replace(minute=0, second=0, microsecond=0)
#     next_hour: pd.Timestamp = this_hour + pd.Timedelta(hours=1)
#     delta: float = next_hour.timestamp() - time()
#     return delta

def go_back_in_time(time_to_reduce: float, reduce_by_secs: int):
    stamp: pd.Timestamp = pd.Timestamp(time_to_reduce, unit="s", tz="UTC")
    result: pd.Timestamp = stamp - pd.Timedelta(seconds=reduce_by_secs)
    return result.timestamp()


def go_forth_in_time(time_to_add: float, reduce_by_secs: int):
    stamp: pd.Timestamp = pd.Timestamp(time_to_add, unit="s", tz="UTC")
    result: pd.Timestamp = stamp + pd.Timedelta(seconds=reduce_by_secs)
    return result.timestamp()


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return begin_time <= check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def has_time_past(base_time: float):
    # If check time is not given, default to current UTC time
    return base_time < the_time_now_is()
