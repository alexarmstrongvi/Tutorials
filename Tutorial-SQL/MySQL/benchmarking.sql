-- Run these within a mysql interactive shell
SELECT BENCHMARK (100000000, CASE WHEN 1=1 THEN 'yes' ELSE 'no' END);
SELECT BENCHMARK (100000000, IF (1=1, 'yes', 'no'));
