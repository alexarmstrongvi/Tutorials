ATTACH DATABASE 'test.db' AS db1;

CREATE TABLE tbl (
    id INTEGER PRIMARY KEY,
    c_null NULL,
    c_int  INTEGER,
    c_real REAL,
    c_text TEXT,
    c_blob BLOB
);

INSERT INTO tbl(c_null, c_int, c_real, c_text, c_blob)
VALUES (NULL,  1, 1.5, 'a', x'00'),
       (NULL,  9, 2.5, 'z', x'09'),
       (NULL, 10, 3.5, 'A', x'0A'),
       (NULL, 19, 3.5, 'Z', x'0F'),
       (NULL,  5, 3.5, 'C', x'1234'),
       (NULL,  6, 3.5, 'C', x'123456'),

SELECT "Dumping Table";
SELECT * FROM tbl;
