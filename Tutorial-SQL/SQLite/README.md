Various guides and examples of using SQLite

# References
* [SQLite official page](https://www.sqlite.org/index.html)
    * [CLI overview](https://sqlite.org/cli.html)
    * [Syntax](https://sqlite.org/lang.html)
* Helpful tutorial pages
    * [sqlitetutorial.net](https://www.sqlitetutorial.net)
    * [Tutorials Point](https://www.tutorialspoint.com/sqlite/index.htm) for SQLite
    * [The Data School](https://dataschool.com/how-to-teach-people-sql/) for general SQL - very helpful visuals

# SQLite3 CLI
## Start up interactive sessions
```bash
> sqlite3

```
## Execute an SQL script in bash terminal
```bash
> sqlite3 < my_script.sql
```

If you want to run the file as a bash executable (`.my_script.sql`), then add
```bash
##!/usr/bin/env bash
tail -n +4 "$0" | sqlite3
exit $?
```
at the top (see this [StackOverflow](https://stackoverflow.com/questions/28976935/make-a-sqlite3-command-file-executable)).
This simply pipes the file code, excluding the first three lines, into sqlite3 and then exits the resulting interactive session.

## Create Database
A database can be created when starting an interactive session
```bash
> sqlite3 test.db
```
or from within an interactive session
```bash
sqlite3> .open test.db
sqlite3> .open --new test.db
```
where `--new` will overwrite any existing database file if it exists.

## Load Other Formats
```bash
sqlite3> .import my_data.csv my_db_name
```

## Globals
To display all databases in the current database connection
```bash
sqlite> .databases
```




