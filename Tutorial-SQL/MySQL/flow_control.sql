SET @var = 2;

-- Switch statement
SELECT
    CASE @var
        WHEN 1 THEN 'one'
        WHEN 2 THEN 'two'
        WHEN 3 THEN 'three'
        ELSE 'Unknown'
    END AS 'Switch';

-- If-else block
SELECT
    CASE
        WHEN @var = 1 THEN 'one'
        WHEN @var = 2 THEN 'two'
        WHEN @var = 3 THEN 'three'
        ELSE 'Unknown'
    END AS 'If-then';

-- Conditional ternary operator
SELECT IF(1<2,'yes','no') AS 'if statement';

SELECT IFNULL(1,'yes'), IFNULL(NULL,'yes'), IFNULL(1/0,'yes');

SELECT NULLIF(1,1), NULLIF(1,2);

