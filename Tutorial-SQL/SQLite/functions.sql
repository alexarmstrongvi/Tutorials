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
WITH t(col) AS (VALUES (2), (-2))
SELECT ABS(col) FROM t;
-- EQUALS [(2,), (2,)]

-- acos(X)
-- acosh(X)
-- asin(X)
-- asinh(X)
-- atan(X)
-- atan2(Y,X)
-- atanh(X)
-- ceil(X)
-- ceiling(X)
-- cos(X)
-- cosh(X)
-- degrees(X)
-- exp(X)
-- floor(X)
-- ln(X)
-- log(B,X)
-- log(X)
-- log10(X)
-- log2(X)
-- mod(X,Y)
-- pi()
-- pow(X,Y)
-- power(X,Y)
-- radians(X)
-- sin(X)
-- sinh(X)
-- sqrt(X)
-- tan(X)
-- tanh(X)
-- trunc(X)

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
-- trim(X)
-- trim(X,Y)
-- ltrim(X)
-- ltrim(X,Y)
-- rtrim(X)
-- rtrim(X,Y)
-- replace(X,Y,Z)
-- substr(X,Y)
-- substr(X,Y,Z)
-- substring(X,Y)
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
-- unhex(X)
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
