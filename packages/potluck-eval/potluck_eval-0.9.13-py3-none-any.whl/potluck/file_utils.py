"""
File-management utilities.

file_utils.py
"""

import os
import time
import datetime
import inspect

from . import logging


#---------#
# Globals #
#---------#

TIMESTAMP_FORMAT = "%Y%m%d@%H:%M:%S"
"""
Format for timestamps (see `time.strftime`).
"""


INITIAL_CWD = os.getcwd()
"""
The working directory on launch (e.g., not a temporary sandbox
directory).
"""


#-----------------#
# Time management #
#-----------------#

def timestamp(when=None):
    """
    Returns a timestamp string based on the current time, or based on a
    given datetime.datetime object or time value in seconds-since-epoch
    format.

    TODO: Time zone issues with showing these to users?
    """
    if when is None:
        when = time.gmtime()

    if isinstance(when, datetime.datetime):
        return when.strftime(TIMESTAMP_FORMAT)
    else:
        return time.strftime(TIMESTAMP_FORMAT, when)


def time_from_timestamp(timestamp):
    """
    Converts a timestamp back into a datetime.datetime.
    """
    return datetime.datetime.strptime(timestamp, TIMESTAMP_FORMAT)


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


def at_time(timestamp_or_datetime):
    """
    Combines `time_from_timestamp` and `fmt_datetime`, but skips applying
    `time_from_timestamp` if the argument is already a datetime object.
    """
    if isinstance(timestamp_or_datetime, datetime.datetime):
        return fmt_datetime(timestamp_or_datetime)
    else:
        return fmt_datetime(time_from_timestamp(timestamp_or_datetime))


def task_time__time(tasks_data, time_string, default_time_of_day=None):
    """
    Converts a time string from task info into a time value. Uses

    Requires a tasks data dictionary (loaded from tasks.json) from which
    it can get a "default_time_of_day" value in case an explicit
    default_time_of_day is not specified. The time string to convert is
    also required.
    str__time with the default hour and minute from the task info.
    """
    if default_time_of_day is None:
        default_time_of_day = tasks_data.get("default_time_of_day", "23:59")
    hd = int(default_time_of_day.split(':')[0])
    md = int(default_time_of_day.split(':')[1])

    return str__time(time_string, default_hour=hd, default_minute=md)


def str__time(tstr, default_hour=23, default_minute=59, default_second=59):
    """
    Converts a string to a datetime object. Default format is:

    yyyy-mm-dd HH:MM:SS TZ

    The hours, minutes, seconds, and timezone are optional. Timezone must
    be given as +HH:SS or -HH:SS. Hours/minutes/seconds default to the end
    of the given day/hour/minute (i.e., 23:59:59), not to 00:00:00,
    unless alternative defaults are specified.
    """
    formats = [
        ("%Y-%m-%d %H:%M:%S %z", {}),
        ("%Y-%m-%d %H:%M:%S", {}),
        ("%Y-%m-%d %H:%M %z", {"second": default_second}),
        ("%Y-%m-%d %H:%M", {"second": default_second}),
        (
            "%Y-%m-%d",
            {
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
        except Exception:
            pass

        if result is not None:
            result = result.replace(**defaults)
            break

    if result is None:
        raise ValueError("Couldn't parse time data: '{}'".format(tstr))

    return result


#---------------------#
# Directories + paths #
#---------------------#

def potluck_src_dir():
    """
    Returns the absolute path to the directory where this file is
    located.
    """
    return os.path.abspath(
        os.path.join(INITIAL_CWD, os.path.dirname(__file__))
    )


def get_spec_module_name():
    """
    Uses the inspect module to get the name of the specifications module,
    assuming that we're in a function which was ultimately called from
    that module, and that module is the only one in our current call
    stack that ends with '.spec'. Returns 'unknown' if it can't find an
    appropriate call frame in the current stack.
    """
    cf = inspect.currentframe()
    while (
        hasattr(cf, "f_back")
    and not cf.f_globals.get("__name__", "unknown").endswith('.spec')
    ):
        cf = cf.f_back

    if cf:
        result = cf.f_globals.get("__name__", "unknown")
        del cf
    else:
        result = "unknown"

    return result


def get_spec_file_name():
    """
    Uses the inspect module to get the path of the specifications file,
    assuming that we're in a function which was ultimately called from
    that module, and that module is the only one in our current call
    stack whose filename ends with '/spec.py'. Returns 'unknown' if it
    can't find an appropriate call frame in the current stack.
    """
    cf = inspect.currentframe()
    while (
        hasattr(cf, "f_back")
    and not cf.f_globals.get("__file__").endswith(os.path.sep + 'spec.py')
    ):
        cf = cf.f_back

    if cf:
        result = cf.f_globals.get("__file__", "unknown")
    else:
        result = "unknown"

    del cf

    return result


def deduce_task_id():
    """
    Uses `get_spec_module_name` to deduce the task ID for the file we're
    being called from. Returns "unknown" if it can't find the spec module
    name, and logs a warning in that case.
    """
    mname = get_spec_module_name()
    if mname == "unknown":
        cf = inspect.currentframe()
        files = []
        while (
            hasattr(cf, "f_back")
        and not cf.f_globals.get("__name__", "unknown").endswith('.spec')
        ):
            files.append(cf.f_globals.get("__file__", "???"))

        if cf:
            files.append(cf.f_globals.get("__file__", "???"))

        logging.log(
            (
                "Warning: unable to deduce correct task ID; results"
                " cache may become corrupted!\nTraceback files:\n  {}"
            ).format('\n  '.join(files))
        )
    return mname.split('.')[0]


#-----------#
# Utilities #
#-----------#

def unused_filename(orig_name):
    """
    Given a desired filename, adds a numerical suffix to the filename
    which makes it unique. If the file doesn't already exist, it returns
    the given name without any suffix. If the given filename already has
    a numerical suffix, it will be incremented until no file by that name
    exists.
    """
    # If the file doesn't exist, it's already unused
    if not os.path.exists(orig_name):
        return orig_name

    # Split the filename part
    dirs, name = os.path.split(orig_name)

    # Split the base + extension
    base, ext = os.path.splitext(name)

    # Get bits of base
    bits = base.split('-')
    last_part = bits[-1]
    first_stuff = '-'.join(bits[:-1])

    # If last part is a numeric suffix already...
    if last_part.isdigit():
        next_digit = int(last_part) + 1
        new_name = first_stuff + '-' + str(next_digit) + ext
        return unused_filename(os.path.join(dirs, new_name))
    else:
        return unused_filename(os.path.join(dirs, base + "-1" + ext))
