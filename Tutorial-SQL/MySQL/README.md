Various guides and examples of using MySQL

# Current guides
* [basics](basics.sql)
* [variables](variables.sql)
* [data\_types](data_types.sql)
* SQL Statements
    * Data manipulation schemes
        * [delete](delete.sql)
* Functions and Operators
    * [user\_functions](user_functions.sql)
    * [aggregate\_functions](aggregate_functions.sql)
    * [window\_functions](window_functions.sql)
    * [dates\_and\_time](dates_and_time.sql)
* Other
    * [temporary\_data\_store](temporary_data_store.sql)
    

# References
* [MySQL official page](https://dev.mysql.com/doc/refman/8.0/en/)
* Helpful tutorial pages
    * [mysqltutorial.org](https://www.mysqltutorial.org/)

# MySQL CLI
## Start up interactive sessions
```bash
> mysql

```
## Execute an SQL script in bash terminal
```bash
> mysql < my_script.sql
```

# Notes
* When to store data in a database vs. spreadsheet vs. text files (e.g. csv, json, txt)
    - As you get more data (i.e. rows), spreadsheet -> files -> database
    - As more people will be reading and updating, files -> spreadsheet -> database 
    - As speed and memory become more important
                                                                    
* Scope, Connection, and Session? "Local temp tables can go out scope when the originating connection closes, and global temp tables can go out of scope when the originating session closes, and no other connection is referencing the table."
    - Connections take place inside a session
