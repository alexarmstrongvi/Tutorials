/*******************************************************************************
https://www.sqlite.org/lang_corefunc.html
https://www.sqlite.org/lang_aggfunc.html

scalar            : FUNC(*args)  -> val
aggregate         : FUNC(grp)    -> val
window            : FUNC(window) -> rows
table-valued (TVF): FUNC(*args)  -> table
*******************************************************************************/

/*******************************************************************************
* Core functions - math {{{
*******************************************************************************/
--------------
-- math: ABS, MIN, MAX, ROUND, SIGN, RANDOM
--------------
SELECT
    abs(-2.0),
    ceil(1.1),
    ceiling(1.1),
    floor(2.9),
    trunc(2.9),
    mod(6, 4);
-- EQUALS [(2.0, 2.0, 2.0, 2.0, 2.0, 2.0)]

SELECT
    degrees(pi()),
    radians(180)/pi(),
    sin(pi()/2);
-- EQUALS [(180.0, 1.0, 1.0)]

SELECT
    sqrt(16),
    pow(2,3),
    power(2,3),
-- EQUALS [(8.0, 8.0, 8.0)],

-- exp(X)
-- ln(X)
-- log(X)
-- log2(X)
-- log10(X)
-- log(B,X)

-- sin(X)
-- sinh(X)
-- cos(X)
-- cosh(X)
-- tan(X)
-- tanh(X)
-- asin(X)
-- asinh(X)
-- acos(X)
-- acosh(X)
-- atan(X)
-- atanh(X)
-- atan2(Y,X)

--- }}}
/*******************************************************************************
* Core functions - strings {{{
*******************************************************************************/
--------------
-- strings
--------------
-- length(X)
-- octet_length(X)

-- lower(X)
-- upper(X)
-- trim(X,Y)
-- ltrim(X,Y)
-- rtrim(X,Y)
-- replace(X,Y,Z)
-- substr(X,Y,Z)
-- substring(X,Y,Z)

-- concat(X,...)
-- concat_ws(SEP,X,...)

-- glob(X,Y)
-- like(X,Y)
-- like(X,Y,Z)
-- instr(X,Y)

-- format(FORMAT,...)
-- printf(FORMAT,...)

-- quote(X)
-- char(X1,X2,...,XN)
-- hex(X)
-- soundex(X)
-- unhex(X,Y)
-- unicode(X)

-- zeroblob(N)
-- randomblob(N)

-- }}}
/*******************************************************************************
* Core functions - other {{{
*******************************************************************************/

--------------
-- logic: IFNULL, IIF, NULLIF
--------------

---------------------------------------
-- INSERT, UPDATE, DELETE properties --
---------------------------------------
-- changes()
-- last_insert_rowid()
-- total_changes()

------------------
-- query planner hints
------------------
-- likelihood(X,Y)
-- likely(X)
-- unlikely(X)

--------------
-- unsorted --
--------------
-- coalesce(X,Y,...)
-- typeof(X)

-- load_extension(X)
-- load_extension(X,Y)

-- sqlite_compileoption_get(N)
-- sqlite_compileoption_used(X)
-- sqlite_offset(X)
-- sqlite_source_id()
-- sqlite_version()

-- }}}
/*******************************************************************************
* Date and time functions {{{
*******************************************************************************/
-- date(time-value, modifier, modifier, ...)
-- time(time-value, modifier, modifier, ...)
-- datetime(time-value, modifier, modifier, ...)
-- julianday(time-value, modifier, modifier, ...)
-- unixepoch(time-value, modifier, modifier, ...)
-- strftime(format, time-value, modifier, modifier, ...)
-- timediff(time-value, time-value)

-- }}}
/*******************************************************************************
* Aggregate functions {{{
*******************************************************************************/
-- avg(X)
-- count(*)
-- count(X)
-- group_concat(X)
-- group_concat(X,Y)
-- max(X)
-- min(X)
-- string_agg(X,Y)
-- sum(X)
-- total(X)

-- }}}
/*******************************************************************************
* TODO
*******************************************************************************/
-- Table-valued functions (TVFs)
-- User-defined functions (UDFs)

/*******************************************************************************
{{{
vim: set foldmethod=marker: set foldlevel=0
}}}
*******************************************************************************/
