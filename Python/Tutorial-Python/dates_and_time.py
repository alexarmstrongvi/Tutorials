#!/usr/bin/env python
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "python-dateutil",
#     "numpy",
#     "pandas",
#     "pytz",
#     "tzdata",
#     "pyarrow",
# ]
# ///
################################################################################
# Notes:
# - Calendar types
#   - ISO
#   - Gregorian (Proleptic)
#
################################################################################

# Standard library
import time as ctime
import datetime as pydatetime
from datetime import date, time, datetime, timedelta, timezone
import calendar
import sys
import zoneinfo

# 3rd party
import pandas as pd
import numpy as np
import pyarrow as pa
# Extensions of datetime
# import dateutil
# import pendulum # datetime wrapper with better API
# import arrow

# TODO: What is a good import convention to disambiguate 'time' and 'datetime'
# without always using full module path? Consider a module that uses the
# following:
#   time.time()
#   datetime.MAXYEAR
#   datetime.time()
#   datetime.datetime(2024,1,1)
# Option 1) Import objects and use aliases for module
#   import time as ctime
#   import datetime as pydatetime
#   from datetime import date, time, datetime, timedelta, timezone
# Option 2) Import modules and use aliases for objects
#   import time
#   import datetime
#   from datetime import time as dt_time, datetime as dt_datetime, date, timedelta, timezone
# Option 3) Import only objects without ambiguities
#   import time
#   import datetime
#   from datetime import date, timedelta, timezone

HOUR = 3600

################################################################################
# OS Time functionality
################################################################################
# struct_time class
t = ctime.gmtime(0)
assert isinstance(t, ctime.struct_time)
# Unix Epoch : Thu Jan  1 00:00:00 1970
assert t.tm_year   == 1970
assert t.tm_mon    == 1
assert t.tm_mday   == 1
assert t.tm_hour   == 0
assert t.tm_min    == 0
assert t.tm_sec    == 0
assert t.tm_wday   == 3
assert t.tm_yday   == 1
assert t.tm_isdst  == 0
assert t.tm_zone   == 'UTC'
assert t.tm_gmtoff == 0

# Conversions
# - floats and ints represent seconds since epoch
# - gm stands for Greenwhich Mean Time (GMT); old name for UTC
# - default input is the current local time in the expected units

EX_TIMESTAMP = 10**9
EX_STRUCT    = ctime.gmtime(EX_TIMESTAMP)
EX_STR       = ctime.ctime(EX_TIMESTAMP)
# Seconds -> struct
assert isinstance(ctime.gmtime(EX_TIMESTAMP)   , ctime.struct_time)
assert isinstance(ctime.localtime(EX_TIMESTAMP), ctime.struct_time)
# Seconds -> string
assert isinstance(ctime.ctime(EX_TIMESTAMP), str)
assert ctime.ctime(EX_TIMESTAMP) == ctime.asctime(ctime.localtime(EX_TIMESTAMP))

# Struct -> string
assert isinstance(ctime.asctime(EX_STRUCT), str)
assert isinstance(ctime.strftime('%c', EX_STRUCT), str)
# Struct -> seconds since epoch (require an input)
assert isinstance(ctime.mktime(EX_STRUCT), float)
assert isinstance(calendar.timegm(EX_STRUCT), int)

# string -> struct
assert isinstance(ctime.strptime(EX_STR), ctime.struct_time)

# Format directives
t = ctime.gmtime(10**9)
assert ctime.strftime('%c', t) == 'Sun Sep  9 01:46:40 2001'
assert ctime.strftime('%x', t) == '09/09/01'
assert ctime.strftime('%X', t) == '01:46:40'

assert ctime.strftime('%w', t) == '0'    # Weekday.
assert ctime.strftime('%a', t) == 'Sun'
assert ctime.strftime('%A', t) == 'Sunday'

assert ctime.strftime('%m', t) == '09'   # Month
assert ctime.strftime('%b', t) == 'Sep'
assert ctime.strftime('%B', t) == 'September'

assert ctime.strftime('%y', t) == '01'   # Year without century
assert ctime.strftime('%Y', t) == '2001' # Year with century
assert ctime.strftime('%G', t) == '2001' # Year with century (ISO 8601 year start)

assert ctime.strftime('%d', t) == '09'   # Day of the month

assert ctime.strftime('%H', t) == '01'   # Hour (24-hour clock)
assert ctime.strftime('%I', t) == '01'   # Hour (12-hour clock)
assert ctime.strftime('%M', t) == '46'   # Minute
assert ctime.strftime('%S', t) == '40'   # Second
assert ctime.strftime('%p', t) == 'AM'

assert ctime.strftime('%z', t) == '-0500' # Time zone offset from UTC

assert ctime.strftime('%j', t) == '252'  # Day of the year
assert ctime.strftime('%W', t) == '36'   # Week number (Monday start)
assert ctime.strftime('%V', t) == '36'   # Week number (Monday start; ISO 8601 year start)
assert ctime.strftime('%U', t) == '36'   # Week number (Sunday start)
assert ctime.strftime('%u', t) == '7'    # Day of week (Sunday start)

# '%f' Microseconds as a decimal number [000000,999999]. Only for strptime()

# Clocks returning seconds and nanoseconds
assert isinstance(ctime.time(),            float)
assert isinstance(ctime.time_ns(),         int)
assert isinstance(ctime.monotonic(),       float)
assert isinstance(ctime.monotonic_ns(),    int)
assert isinstance(ctime.perf_counter(),    float)
assert isinstance(ctime.perf_counter_ns(), int)
assert isinstance(ctime.process_time(),    float)
assert isinstance(ctime.process_time_ns(), int)
result = dict(sorted({
    'time'         : ctime.time_ns(),
    'perf_counter' : ctime.perf_counter_ns(),
    'monotonic'    : ctime.monotonic_ns(),
    'process_time' : ctime.process_time_ns(),
}.items(), key = lambda kv : kv[0]))
assert ctime.time_ns()         >  ctime.perf_counter_ns(),    result
assert ctime.perf_counter_ns() >= ctime.process_time_ns(), result

# Get info on the above second clocks
clock_name = 'monotonic'
clock_info = ctime.get_clock_info(clock_name)
#print('Info on clock:', clock_name)
#print('\timplementation =',clock_info.implementation)
#print('\tmonotonic      =',clock_info.monotonic)
#print('\tadjustable     =',clock_info.adustable)
#print('\tresolution     =',clock_info.resolution)

# Local info
assert ctime.altzone == ctime.timezone - HOUR
print('Local clock info')
print(ctime.strftime('%c UTC%z', ctime.localtime(ctime.time())))
print('%s = UTC%+03d%02d' % (ctime.tzname[0], *divmod(-ctime.timezone,HOUR)))
if ctime.daylight:
    print('%s = UTC%+03d%02d' % (ctime.tzname[1], *divmod(-ctime.altzone,HOUR)))

# Configuration
# tzset()

#################################################################################
# Datetime module
#################################################################################
assert pydatetime.MINYEAR == 1
assert pydatetime.MAXYEAR == 9999

########################################
# Date
########################################
d = date(1970,1,1)
# Attributes
assert d.year       == 1970
assert d.month      == 1
assert d.day        == 1

# Extract
assert d.weekday()    == 3 # Mon = 0
assert d.isoweekday() == 4 # Sun = 0

## Conversion
# -> string
assert d.ctime()     == d.strftime('%c') == 'Thu Jan  1 00:00:00 1970'
assert d.isoformat() == str(d)           == '1970-01-01'

# -> ctime.struct_time
assert d.timetuple()

# -> pydatetime.IsoCalendarDate(year, week, weekday)
assert d.isocalendar()

# -> int (days since Jan 1, 0000)
assert d.toordinal()

# Class Constructors
# d.fromisocalendar()
# d.fromisoformat()
# d.fromordinal()
# d.fromtimestamp()

# Class Methods and Variables
assert d.max        == date.max        == date(9999,12,31)
assert d.min        == date.min        == date(1,1,1)
assert d.resolution == date.resolution == timedelta(days=1)
assert d.today()    == date.today()

########################################
# Time
########################################
t = time(
    hour        = 15,
    minute      = 30,
    second      = 10,
    microsecond = 123456,
    tzinfo      = timezone.utc,
)
assert t.fold        == 0
assert t.dst()       is None
assert t.tzname()    == 'UTC'
assert t.utcoffset() == timedelta(0)

## Conversion
# -> string
assert t.isoformat() == str(t) == '15:30:10.123456+00:00'
assert t.strftime('%c') == 'Mon Jan  1 15:30:10 1900'

# Class constructors
# t.fromisoformat()

# Class variables
assert t.resolution == time.resolution == timedelta(microseconds=1)
assert t.max        == time.max        == time(23, 59, 59, 999999)
assert t.min        == time.min        == time(0,0)

########################################
# Datetime
########################################
dt = datetime(1970,1,1)

# All the methods of time and date

# Extract
# dt.date()
# dt.time()
# dt.timetz()

# Conversion
# -> string
# dt.ctime()
# dt.timestamp()
# -> struct_time
# dt.utctimetuple()
# -> datetime w/ tzinfo
# dt.astimezone

# Class constructors
# dt.strptime()
# dt.utcfromtimestamp()
# dt.combine(d, t)

# Class methods
# dt.now() ~ datetime.now() # differ by a few microsec

########################################
# Time Delta
########################################
td = timedelta()
assert td.days         == 0
assert td.seconds      == 0
assert td.microseconds == 0

# Conversion
assert td.total_seconds() == 0

# Class attributes
assert td.resolution == timedelta.resolution == timedelta(microseconds=1)
assert td.max == timedelta(days=999999999, seconds=86399, microseconds=999999)
assert td.min == timedelta(days=-999999999)


########################################
# Timezone: tzinfo and timezone
# Various date and time related classes support timezone handling via a tzinfo
# attribute whose type is derived from the pydatetime.tzinfo abstract base class.
# When this attribute is not set, the classes are called "naive" and all
# arithmatic behaves like a fixed offset time zone. When the attribute is set,
# these classes become timezone "aware" and arithmetic uses the tzinfo methods
# to correct for discontinuous behavior like daylight savings time.
########################################
# Fixed offset timezones can be handled with timezone objects, the
# simpliest implementation of pydatetime.tzinfo
tzinfo_utc = timezone(offset=timedelta(0))
assert isinstance(tzinfo_utc, pydatetime.tzinfo)
assert tzinfo_utc == timezone.utc

offset = timedelta(hours=-8)
name   = 'California'
tzinfo = timezone(offset, name)
# NOTE: Must specify dummy datetime argument even though irrelevant for fixed
# offset timezones because nothing is datetime dependent
dt = None
assert tzinfo.dst(dt)       is None
assert tzinfo.tzname(dt)    == name
assert tzinfo.utcoffset(dt) == offset

dt = datetime.now(tz=tzinfo)
assert dt.tzinfo          is tzinfo
assert dt.time().tzinfo   is None
assert dt.timetz().tzinfo is tzinfo
assert dt.dst()           is tzinfo.dst(dt)
assert dt.tzname()        is tzinfo.tzname(dt)
assert dt.utcoffset()     is tzinfo.utcoffset(dt)

dt_utc = dt.astimezone(timezone.utc)
assert dt.hour != dt_utc.hour
assert dt == dt_utc # Compares time accounting for timezones

########################################
# Timezone: zoneinfo
# Real timezones (e.g. America/Los_Angeles) are not fixed offset and instead
# have behavior that depends on time of year (e.g. daylight savings time) and on
# the time in history (e.g. the first day of DST changed in the US in 2007). The
# concrete implementations of tzinfo that handle this complexity used to be in
# the 3rd party pytz library but since python 3.9 have been added to zoneinfo
# in the standard library.
########################################
tzinfo = zoneinfo.ZoneInfo('America/Los_Angeles')
assert tzinfo.key == 'America/Los_Angeles'
assert tzinfo.key in zoneinfo.available_timezones()

# Error raised for unknown and non-existent time zones
assert 'NotATimeZone' not in zoneinfo.available_timezones()
try:
    zoneinfo.ZoneInfo('NotATimeZone')
    assert False
except zoneinfo.ZoneInfoNotFoundError:
    pass

# tzinfo attributes depend on datetime
# DST in 2020 ended at 2am on Nov 1st and so 1:30am occurred twice
dst_dt = datetime(2020, 11, 1, 1, 30, tzinfo=tzinfo)
std_dt = datetime(2020, 11, 1, 2, 30, tzinfo=tzinfo)
# Timezone info not knowable without a datetime
assert tzinfo.dst(None)      is None
assert tzinfo.tzname(None)   is None
assert tzinfo.utcoffset(None)is None
# Timezone info depends on being during DST or not
assert tzinfo.dst(std_dt) == timedelta(hours=0)
assert tzinfo.dst(dst_dt) == timedelta(hours=1)
assert tzinfo.tzname(std_dt) == 'PST'
assert tzinfo.tzname(dst_dt) == 'PDT'
assert tzinfo.utcoffset(std_dt) == timedelta(hours=-8)
assert tzinfo.utcoffset(dst_dt) == timedelta(hours=-7)

# The fold attribute added in PEP 494 disambiguates times that happen twice
# during the end of DST
dt0 = dst_dt.replace(fold=0) # 1:30am during DST
dt1 = dst_dt.replace(fold=1) # 1:30am after DST
dt0_utc = dt0.astimezone(timezone.utc)
dt1_utc = dt1.astimezone(timezone.utc)
assert dt0.fold == 0
assert dt1.fold == 1
assert dt0.tzname() == 'PDT'
assert dt1.tzname() == 'PST'
assert dt0_utc.tzname() == dt1_utc.tzname() == 'UTC'
# Comparisons and arithmatic on aware datetimes ignore fold to avoid breaking
# backwards compatibility so convert to UTC first.
# Takeaway: CONVERT TO UTC BEFORE DOING COMPARISONS OR ARITHMATIC
# Intra-timezone arithmetic and comparisons: fold and tzinfo ignored
assert dt1     == dt0     and dt1     - dt0     == timedelta(hours=0)
assert dt0_utc != dt1_utc and dt1_utc - dt0_utc == timedelta(hours=1) # Correct answer
# Inter-timezone arithmetic and comparisons: converted to UTC
assert dt0_utc != dt0 and (dt0_utc - dt0 == timedelta(hours=0))
assert dt1_utc != dt1 and (dt1_utc - dt1 == timedelta(hours=0))
# Timedelta arithmetic: ignores and removes fold
dt1_td = dt1 + timedelta(0)
assert dt1_td.fold     != dt1.fold
assert dt1_td.tzname() != dt1.tzname()
assert dt1_td.tzname() == dt0.tzname()

#################################################################################
# Calendar
#################################################################################
assert calendar.EPOCH == 1970

assert calendar.MONDAY    == 0
assert calendar.SUNDAY    == 6

if sys.version_info[:2] >= (3, 12):
    assert calendar.JANUARY   == 1
    assert calendar.DECEMBER  == 12

assert tuple(calendar.day_abbr) == (
    'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
assert tuple(calendar.day_name) == (
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
)
assert tuple(calendar.month_abbr) == (
    '', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
)
assert tuple(calendar.month_name) == (
    '', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'
)
assert calendar.mdays == [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

#calendar.c = <calendar.TextCalendar obect at 0x7fbf4a9e81f0>
#calendar.calendar()
#calendar.firstweekday()
#calendar.month()
#calendar.monthcalendar()
#calendar.prcal()
#calendar.prmonth()
#calendar.week()
#calendar.weekheader()

#calendar.format()
#calendar.formatstring()
#calendar.isleap()
#calendar.leapdays()
#calendar.main()
#calendar.monthrange()
#calendar.setfirstweekday()
#calendar.timegm()
#calendar.weekday()

#calendar.Calendar
#calendar.HTMLCalendar
#calendar.IllegalMonthError

################################################################################
# 3rd party libraries and datetime arrays
################################################################################
############################################################################
# Datetime
# - float timestamps conventionally have units of seconds while integer
#   timestamps have subsecond precision (e.g. us, or ns)
############################################################################

# Getting datetimes
dt_int = ctime.time_ns()             # us precision; Always UTC
dt_flt = ctime.time()                # us precision; Always UTC
dt_py  = datetime.now(timezone.utc)  # us precision
dt_py2 = ctime.gmtime()              #  s precision; Always UTC
dt_np  = np.datetime64('now')        #  s precision; Always UTC
dt_pd  = pd.Timestamp.now('utc')     # us precision

# Datetimes
dt_int = 1234567890123456789
dt_flt = 1234567890.123456789
dt_str = '2009-02-13T23:31:30.123456789'
dt_py  = datetime(2009, 2, 13, 23, 31, 30, 123457)
dt_py2 = ctime.struct_time((2009, 2, 13, 23, 31, 30, None, None, None))
dt_np  = np.datetime64(dt_str)
dt_pd  = pd.Timestamp(dt_str)
dt_pa  = pa.scalar(dt_int, type=pa.timestamp(unit='ns'))

print('\n==== Datetimes ====')
buf = 60
print(f'{dt_int!r:<{buf}} | {type(dt_int)}')
print(f'{dt_flt!r:<{buf}} | {type(dt_flt)}')
print(f'{dt_str!r:<{buf}} | {type(dt_str)}')
print(f'{dt_py!r:<{buf}} | {type(dt_py)}')
print(f'{dt_np!r:<{buf}} | {type(dt_np)}')
print(f'{dt_pd!r:<{buf}} | {type(dt_pd)}')
print(f'{dt_pa!r:<{buf}} | {type(dt_pa)}')

# us_per_s = np.timedelta64(1,'s').astype('timedelta64[us]').astype(int)
precision = 10**9
result = [
# int | float | ISO string | datetime | numpy | pandas | pyarrow
[ # FROM int TO ...
    dt_int,                                          # int        :
    dt_int / precision,                              # float      :
    None,                                            # ISO string : int -> numpy -> string
    None,                                            # datetime   : int -> float -> datetime
    np.datetime64(dt_int, 'ns'),                     # numpy      :
    pd.Timestamp(dt_int, unit='ns'),                 # pandas     :
    pa.scalar(dt_int, type=pa.timestamp(unit='ns')), # pyarrow    :
],
[ # FROM float TO ...
    int(dt_flt * precision),        # int        : Loss of precision
    dt_flt,                         # float      :
    None,                           # ISO string : float -> datetime -> string
    datetime.fromtimestamp(dt_flt), # datetime   :
    None,                           # numpy      : float -> int or datetime -> numpy
    pd.Timestamp(dt_flt, unit='s'), # pandas     :
    None,                           # pyarrow    : float -> int -> pyarrow
],
[ # FROM string TO ...
    None,                           # int        : string -> numpy -> int
    None,                           # float      : string -> datetime -> float
    dt_str,                         # ISO string :
    datetime.fromisoformat(dt_str), # datetime   : Loss of precision
    np.datetime64(dt_str),          # numpy      :
    pd.Timestamp(dt_str),           # pandas     :
    None,                           # pyarrow    : string -> int -> pyarrow
],
[ # FROM datetime TO ...
    None,                 # int        : datetime -> float -> int
    dt_py.timestamp(),    # float      :
    dt_py.isoformat(),    # ISO string :
    dt_py,                # datetime   :
    np.datetime64(dt_py), # numpy      :
    pd.Timestamp(dt_py),  # pandas     :
    pa.scalar(dt_py)      # pyarrow    :
],
[ # FROM numpy TO ...
    int(dt_np),          # int        :
    None,                # float      : numpy -> int -> float
    str(dt_np),          # ISO string :
    None,                # datetime   : numpy -> string -> datetime
    dt_np,               # numpy      :
    pd.Timestamp(dt_np), # pandas     :
    pa.scalar(dt_np)     # pyarrow    :
],
[ # FROM pandas TO ...
    dt_pd.value,                                   # int        :
    dt_pd.timestamp(),                             # float      :
    dt_pd.isoformat(),                             # ISO string :
    dt_pd.round('us').to_pydatetime(),             # datetime   : rounding prevents warning
    dt_pd.to_numpy(),                              # numpy      :
    dt_pd,                                         # pandas     :
    pa.scalar(dt_pd, type=pa.timestamp(unit='ns')) # pyarrow    :
],
[ # FROM pyarrow TO ...
    dt_pa.value,    # int        :
    None,           # float      : pyarrow -> int -> float
    str(dt_pa),     # ISO string : Not ISO formatted
    None,           # datetime   : pyarrow -> pandas -> datetime
    None,           # numpy      : pyarrow -> int -> numpy
    dt_pa.as_py(),  # pandas     :
    dt_pa,          # pyarrow    :
],
]

order = 'int float ISO-string datetime numpy pandas pyarrow'.split()
df = pd.DataFrame(result, index=order, columns=order, dtype=object).rename_axis(index='from', columns='to')
# with pd.option_context('display.max_columns', None, 'display.max_colwidth', None):
# with pd.option_context('display.max_colwidth', None):
#     print(df)

# datetime arrays
dt_int_arr = [dt_int]
dt_np_arr  = np.array( [dt_np], dtype = 'datetime64[ns]')
dt_pd_arr  = pd.Series([dt_pd], dtype = 'datetime64[ns]')
dt_pa_arr  = pa.array( [dt_pa],  type = pa.timestamp(unit='ns'))

result = [
[ # FROM list[int]
    dt_int_arr,
    np.array(dt_int_arr,  dtype = 'datetime64[ns]'),
    pd.Series(dt_int_arr, dtype = 'datetime64[ns]'),
    pa.array(dt_int_arr,   type = pa.timestamp(unit='ns')),
],
[ # FROM numpy
    dt_np_arr.astype(int),
    dt_np_arr,
    pd.Series(dt_np_arr),
    pa.array(dt_np_arr),
],
[ # FROM pandas
    dt_pd_arr.astype(int),
    dt_pd_arr.to_numpy(),
    dt_pd_arr,
    pa.array(dt_pd_arr),
],
[ # FROM pyarrow
    pa.array(dt_pa_arr, type=pa.int64()),
    dt_pa_arr.to_numpy(),
    dt_pa_arr.to_pandas(),
    dt_pa_arr,
],
]
result = [[x[0] for x in row] for row in result]
order = 'int numpy pandas pyarrow'.split()
df = pd.DataFrame(result, index=order, columns=order, dtype=object).rename_axis(index='from', columns='to')
# with pd.option_context('display.max_columns', None, 'display.max_colwidth', None):
# with pd.option_context('display.max_colwidth', None):
#     print(df)

# Timezones
# - Numpy and PyArrow only work with naive timestamps
# - Timezone conversion is possible in PyArrow whereas Numpy requires converting
#   to python datetime and back
tzname = 'America/Los_Angeles'
dt_pd_arr_tz = dt_pd_arr.dt.tz_localize(tzname)
dt_pa_arr_tz = dt_pa_arr # ...not possible
dt_pd_arr_utc = dt_pd_arr_tz.dt.tz_convert('UTC')
dt_pa_arr_utc = pa.compute.assume_timezone(dt_pa_arr, tzname)
########################################
# TODO: dates and date arrays

########################################
# TODO: times and time arrays

########################################
# TODO: timedeltas and timedelta arrays
td_int = 1234560123456
td_flt = 1234560.123456
td_str = '14 days, 6:56:00.123456'
td_py  = timedelta(weeks=1, days=7, hours=6, minutes=56, seconds=0, milliseconds=123, microseconds=456)
td_np  = np.timedelta64(td_int, 'us')
td_pd  = pd.Timedelta(td_int, 'us')
td_pa  = pa.scalar(td_int, type=pa.duration(unit='us'))

print('\n==== Timedelta ====')
buf = 60
print(f'{td_int!r:<{buf}} | {type(td_int)}')
print(f'{td_flt!r:<{buf}} | {type(td_flt)}')
print(f'{td_str!r:<{buf}} | {type(td_str)}')
print(f'{td_py!r:<{buf}} | {type(td_py)}')
print(f'{td_np!r:<{buf}} | {type(td_np)}')
print(f'{td_pd!r:<{buf}} | {type(td_pd)}')
print(f'{td_pa!r:<{buf}} | {type(td_pa)}')
