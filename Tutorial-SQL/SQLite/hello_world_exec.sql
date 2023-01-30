#!/usr/bin/env bash
tail -n +4 "$0" | sqlite3
exit $?
SELECT "Hello World";
