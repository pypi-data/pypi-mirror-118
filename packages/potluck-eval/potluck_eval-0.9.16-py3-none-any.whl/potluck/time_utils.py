"""
Time and date management utilities.

time_utils.py
"""

import time
import datetime

# Needed for better timezone handling, or ANY timezone handling in 2.7
import dateutil.tz


#---------#
# Globals #
#---------#

TIMESTRING_FORMAT = "%Y%m%d@%H:%M:%S(%z)"
"""
Format for time-strings (see `time.strftime`).
"""


#-----------------#
# Time management #
#-----------------#

def now():
    """
    Returns a time-zone-aware datetime representing the current time.
    """
    return datetime.datetime.now(dateutil.tz.UTC)


def timestring(when=None):
    """
    Returns a time string based on the current time, or based on a given
    datetime.datetime object or time value in seconds-since-epoch format.
    """
    if when is None:
        when = now()

    if isinstance(when, datetime.datetime):
        # Add UTC timezone if we were given a naive object
        if when.tzinfo is None:
            when = when.astimezone(dateutil.tz.UTC)
        return when.strftime(TIMESTRING_FORMAT)
    else:
        return time.strftime(TIMESTRING_FORMAT, when)


def time_from_timestamp(timestamp):
    """
    Converts a timestamp value into a timezone-aware datetime.datetime.
    """
    result = datetime.datetime.fromtimestamp(timestamp)
    if result.tzinfo is None:
        result = result.astimezone(dateutil.tz.UTC)
    return result


def time_from_timestring(timestring):
    """
    Converts a time string back into a (timezone-aware)
    datetime.datetime.
    """
    # Version that includes a timezone
    result = datetime.datetime.strptime(timestring, TIMESTRING_FORMAT)

    # Ensure we're a TZ-aware object in UTC
    result = result.astimezone(dateutil.tz.UTC)
    return result


def fmt_datetime(when):
    """
    Formats a datetime using 24-hour notation w/ extra a.m./p.m.
    annotations in the morning for clarity, and a timezone attached.
    """
    # Use a.m. for extra clarity when hour < 12, and p.m. for 12:XX
    am_hint = ''
    if when.hour < 12:
        am_hint = ' a.m.'
    elif when.hour == 12:
        am_hint = ' p.m.'

    tz = when.strftime("%Z")
    if tz != '':
        tz = ' ' + tz
    return when.strftime("at %H:%M{}{} on %Y-%m-%d".format(am_hint, tz))


def at_time(time_obj):
    """
    Uses `fmt_datetime` to produce a string, but accepts and converts
    `datetime` objects, `struct_time` objects, and time-strings.
    """
    if isinstance(time_obj, datetime.datetime):
        return fmt_datetime(time_obj)
    elif isinstance(time_obj, (int, float)):
        return fmt_datetime(time_from_timestamp(time_obj))
    elif isinstance(time_obj, str): # we assume it's a time string
        return fmt_datetime(time_from_timestring(time_obj))
    else:
        raise TypeError(
            "Cannot convert a {} ({}) to a time value.".format(
                type(time_obj),
                repr(time_obj)
            )
        )


def task_time__time(
    tasks_data,
    time_string,
    default_time_of_day=None,
    default_tz=None
):
    """
    Converts a time string from task info into a time value. Uses
    str__time with the default time zone, hours, and minutes from the
    task data.

    Requires a tasks data dictionary (loaded from tasks.json) from which
    it can get a "default_time_of_day" and/or "default_tz" value in case
    an explicit default_time_of_day is not specified. The time string to
    convert is also required.

    See `local_timezone` for information on how a timezone is derived
    from the tasks data.
    """
    if default_time_of_day is None:
        default_time_of_day = tasks_data.get("default_time_of_day", "23:59")

    if default_tz is None:
        default_tz = local_timezone(tasks_data)

    hd = int(default_time_of_day.split(':')[0])
    md = int(default_time_of_day.split(':')[1])

    return str__time(
        time_string,
        default_hour=hd,
        default_minute=md,
        default_tz=default_tz
    )


def str__time(
    tstr,
    default_hour=23,
    default_minute=59,
    default_second=59,
    default_tz=dateutil.tz.UTC
):
    """
    Converts a string to a datetime object. Default format is:

    yyyy-mm-dd HH:MM:SS TZ

    The hours, minutes, seconds, and timezone are optional.

    Timezone must be given as +HHMM or -HHMM (e.g., -0400 for 4-hours
    after UTC).

    Hours/minutes/seconds default to the end of the given day/hour/minute
    (i.e., 23:59:59), not to 00:00:00, unless alternative defaults are
    specified.
    """
    formats = [
        ("%Y-%m-%d %H:%M:%S %z", {}),
        ("%Y-%m-%d %H:%M:%S", {"tzinfo": default_tz}),
        ("%Y-%m-%d %H:%M %z", {"second": default_second}),
        ("%Y-%m-%d %H:%M", {"tzinfo": default_tz, "second": default_second}),
        (
            "%Y-%m-%d",
            {
                "tzinfo": default_tz,
                "second": default_second,
                "minute": default_minute,
                "hour": default_hour
            }
        )
    ]
    result = None
    for f, defaults in formats:
        try:
            result = datetime.datetime.fromtimestamp(
                time.mktime(time.strptime(tstr, f))
            )
        except ValueError:
            pass

        if result is not None:
            result = result.replace(**defaults)
            break

    if result is None:
        raise ValueError("Couldn't parse time data: '{}'".format(tstr))

    return result


def local_timezone(tasks_data):
    """
    Returns the timezone object implied by the settings in the given
    tasks data.

    The tasks data's "timezone" slot will be used; its value should be
    either a number of hours difference from UTC (positive or negative),
    or a list of two numbers specifying hours and minutes difference
    from UTC (for a negative offset, both numbers would be negative).

    If the tasks data has a "tz_name" slot, the string in that slot will
    be used as the name of the time zone.
    """
    return dateutil.tz.gettz(tasks_data.get("timezone"))


def local_time(
    tasks_data,
    time_obj
):
    """
    Given access to the tasks data object and a datetime, returns an
    equivalent datetime with the timezone set to the time zone specified
    by the tasks data. Uses UTC if the tasks data does not specify a
    timezone.
    """
    return time_obj.astimezone(local_timezone(tasks_data))
