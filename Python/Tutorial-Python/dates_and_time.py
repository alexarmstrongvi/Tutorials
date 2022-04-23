#!/usr/bin/env python
################################################################################
# Notes:
# - Calendar types
#   - ISO
#   - Gregorian (Proleptic)
#
################################################################################

import LexTools as utils
import time
import datetime # DataTypes
import calendar # DataTypes
import zoneinfo # DataTypes

SEC_PER_HOUR = 3600
SEC_REF = 0
STRUCT_REF = time.gmtime(SEC_REF)
STR_REF = time.ctime(SEC_REF)

################################################################################
# OS Time functionality
################################################################################
# struct_time class
t = time.gmtime(0)
assert type(t) == time.struct_time
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

#print('\nConversions')
# - floats and ints represent seconds since epoch
# - gm stands for Greenwhich Mean Time (GMT); old name for UTC
# - default input is the current local time in the expected units

# Seconds -> struct
#print('gmtime()    =', time.gmtime(SEC_REF)) # GM -> Greenwich Mean = UTC
#print('localtime() =', time.localtime(SEC_REF))
# Seconds -> string
#print('ctime()     =', time.ctime(SEC_REF))
assert time.ctime(SEC_REF) == time.asctime(time.localtime(SEC_REF))
# Struct -> string
#print('asctime()   =', time.asctime(STRUCT_REF))
#print('strftime()  =', time.strftime('%c', STRUCT_REF))
# Struct -> seconds since epoch (require an input)
#print('mktime()    =', time.mktime(time.localtime(SEC_REF)))
#print('timegm()    =', calendar.timegm(time.gmtime(SEC_REF)))
# string -> struct
#print('strptime()  =', time.strptime(STR_REF))

# Format directives
#print(time.strftime('''
#Local aware
#%a \t\t: Abbreviated weekday name.
#%A   \t: Full weekday name.
#%b \t\t: Abbreviated month name.
#%B   \t: Full month name.
#%x   \t: Date representation.
#%X   \t: Time representation.
#%p \t\t: Locale’s equivalent of either AM or PM.
#Locale’s appropriate date and time representation.
#%c
#
#Numbers
#%d \t: Day of the month
#%H \t: Hour (24-hour clock)
#%I \t: Hour (12-hour clock)
#%j \t: Day of the year
#%m \t: Month
#%M \t: Minute
#%S \t: Second
#%w \t: Weekday.
#%W \t: Week number (Monday start)
#%U \t: Week number (Sunday start)
#%y \t: Year without century
#%Y \t: Year with century
#%z \t: Time zone offset
#''', time.localtime()))

# Action
# time.sleep()

#print('\nClocks returning seconds and nanoseconds')
#print('time()            = %.9f s' % time.time())
#print('time_ns()         = %d  ns' % time.time_ns())
#print('monotonic()       = %.9f s' % time.monotonic())
#print('monotonic_ns()    = %d  ns' % time.monotonic_ns())
#print('perf_counter()    = %.9f s' % time.perf_counter())
#print('perf_counter_ns() = %d  ns' % time.perf_counter_ns())
#print('process_time()    = %.9f s' % time.process_time())
#print('process_time_ns() = %d  ns' % time.process_time_ns())

#print('\nGet info on the above second clocks')
clock_name = 'monotonic'
result = time.get_clock_info(clock_name)
#print('Info on clock:', clock_name)
#print('\timplementation =',result.implementation)
#print('\tmonotonic      =',result.monotonic)
#print('\tadjustable     =',result.adjustable)
#print('\tresolution     =',result.resolution)

#print('\nConstants')
#print('Daylight savings zone defined?', bool(time.daylight))
#print('%s time zone is %+d hours w.r.t UTC' % (time.tzname[0], -time.timezone//SEC_PER_HOUR))
#print('%s time zone is %+d hours w.r.t UTC' % (time.tzname[1], -time.altzone//SEC_PER_HOUR))
assert time.altzone == time.timezone - SEC_PER_HOUR

# Configuration
# tzset()

#################################################################################
# Datetime
#################################################################################
assert datetime.MINYEAR == 1
assert datetime.MAXYEAR == 9999

########################################
# Date
########################################
d = datetime.date(1970,1,1)
# Attributes
assert d.year       == 1970
assert d.month      == 1
assert d.day        == 1

# Extract
#print('weekday()         =', repr(d.weekday()))
#print('isoweekday()      =', repr(d.isoweekday()))

# Modify
# d = d.replace()

## Conversion
# -> string
#print('ctime() =', d.ctime())
#print('isoformat()       =', repr(d.isoformat()))
assert str(d) == d.isoformat()
#print('strftime()        =', d.strftime())
# -> time.struct_time
#print('timetuple()       =', repr(d.timetuple()))
# -> datetime.IsoCalendarDate
#print('isocalendar()     =', repr(d.isocalendar()))
# -> int
#print('toordinal()       =', d.toordinal())

# Class Constructors
#print('fromisocalendar() =', d.fromisocalendar())
#print('fromisoformat()   =', d.fromisoformat())
#print('fromordinal()     =', d.fromordinal())
#print('fromtimestamp()   =', d.fromtimestamp())

# Class Methods and Variables
assert d.max        == datetime.date.max        == datetime.date(9999,12,31)
assert d.min        == datetime.date.min        == datetime.date(1,1,1)
assert d.resolution == datetime.date.resolution == datetime.timedelta(days=1)
assert d.today()    == datetime.date.today()

########################################
# Time
########################################
t = datetime.time()
assert str(t) == t.isoformat()
assert t.fold == 0
assert t.hour   == 0
assert t.minute == 0
assert t.second == 0
assert t.microsecond == 0
if t.tzinfo is not None:
    print('dst() =', t.dst())
    print('tzname() =', t.tzname())
    print('utcoffset() =', t.utcoffset())

## Conversion
# -> string
# t.isoformat()
# t.strftime()

# Class constructors 
# t.fromisoformat()

# Class variables
assert t.resolution == datetime.time.resolution == datetime.timedelta(microseconds=1)
assert t.max        == datetime.time.max        == datetime.time(23, 59, 59, 999999) 
assert t.min        == datetime.time.min        == datetime.time(0,0)

########################################
# Datetime
########################################
dt = datetime.datetime(1970,1,1)

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
# dt.now() ~ datetime.datetime.now() # differ by a few microsec

########################################
# Time Delta
########################################
td = datetime.timedelta()
assert td.days         == 0
assert td.seconds      == 0
assert td.microseconds == 0

# Conversion
assert td.total_seconds() == 0

# Class attributes
assert td.resolution == datetime.timedelta.resolution == datetime.timedelta(microseconds=1)
assert td.max == datetime.timedelta(days=999999999, seconds=86399, microseconds=999999)
assert td.min == datetime.timedelta(days=-999999999)


########################################
# Timezone
########################################
tz = datetime.timezone(td)
assert tz == datetime.timezone.utc
#attribute
# max = datetime.timezone(datetime.timedelta(seconds=86340))
# min = datetime.timezone(datetime.timedelta(days=-1, seconds=60))
# utc = datetime.timezone.utc
#method
# dst()
# fromutc()
# tzname()
# utcoffset()

########################################
# Timezone Info
# Abstract base class
########################################
# datetime.tzinfo

#################################################################################
# Calendar
#################################################################################
assert calendar.EPOCH == 1970

assert calendar.MONDAY    == 0
assert calendar.TUESDAY   == 1
assert calendar.WEDNESDAY == 2
assert calendar.THURSDAY  == 3
assert calendar.FRIDAY    == 4
assert calendar.SATURDAY  == 5
assert calendar.SUNDAY    == 6
assert calendar.January   == 1
assert calendar.February  == 2
assert tuple(calendar.day_abbr) == (
        'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
assert tuple(calendar.day_name) == (
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday')
assert tuple(calendar.month_abbr) == (
        '',
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec')
assert tuple(calendar.month_name) == (
        '',
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December')
assert calendar.mdays == [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

#calendar.c = <calendar.TextCalendar object at 0x7fbf4a9e81f0>
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
