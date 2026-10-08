SELECT Sales.sale_date as SalesDate, Products.product_name as ProductName, Sales.quantity as TotalQuantity, (Sales.quantity * Products.price) as TotalRevenue
FROM Sales
INNER JOIN Products ON Sales.product_id = Products.product_id
ORDER BY Sales.sale_date ASC;