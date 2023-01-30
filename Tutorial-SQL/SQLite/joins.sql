/*
/*******************************************************************************
All the basics of joining tables in SQL

- https://dataschool.com/how-to-teach-people-sql/sql-join-types-explained-visually/
*******************************************************************************/

/*
* Not in SQLite
* - RIGHT JOIN - emulated with LEFT JOIN by swapping tables and column order
* - FULL OUTER JOIN - emulated using LEFT JOIN and UNION
*/

CREATE TABLE Orders (
    OrderID    INTEGER,
    CustomerID INTEGER
);
INSERT INTO Orders(OrderID, CustomerID)
VALUES (1, 11),
       (2, 22),
       (3, 22),
       (4, 33),
       (5, 44);

CREATE TABLE Customers (
    CustomerName TEXT,
    CustomerID   INTEGER
);
INSERT INTO Customers(CustomerName, CustomerID)
VALUES ("Alice",     11),
       ("Bob",       22),
       ("Cathy",     33),
       ("Catherine", 33),
       ("Derek",     55);

SELECT 'Order Data';
SELECT * FROM Orders;
SELECT '';
SELECT 'Customer Data';
SELECT * FROM Customers;
SELECT '';

/***************************************
* JOIN, INNER JOIN
* - Join tables at matched rows
* - Steps
*     (1) Create new table with specified columns from tables
*     (2) Loop through rows of first table
*         (2a) Loop through rows of second table
*         (2b) If match condition is true, build joined row and add to new table
* 
* Note) Duplicate rows if row in first table matches multiple rows in second table or vice versa
***************************************/
SELECT "Inner join customers to orders";
SELECT * FROM Orders
JOIN Customers ON Orders.CustomerID = Customers.CustomerID;
SELECT '';

SELECT "Inner join orders to customers";
SELECT * FROM Customers
JOIN Orders ON Customers.CustomerID = Orders.CustomerID;
SELECT '';

/***************************************
* LEFT JOIN, LEFT OUTER JOIN
* - Join tables at matched rows but add all entries from first table regardless
* - Steps
*     (1-2) Same as INNER JOIN
*         (2c) If match condition is false, build row from first table data and use NULL for second table data
***************************************/
SELECT "Left join customers to orders";
SELECT * FROM Orders
LEFT JOIN Customers ON Orders.CustomerID = Customers.CustomerID;
SELECT '';

SELECT "Left join orders to customers";
SELECT * FROM Customers
LEFT JOIN Orders USING (CustomerID);
SELECT '';

/***************************************
* CROSS JOIN
* - Cartesian cross product combining data in all columns
***************************************/
SELECT "Cross join orders to customers";
SELECT * FROM Orders
CROSS JOIN Customers
LIMIT 10;

/***************************************
* USING() and NATURAL JOIN
***************************************/
