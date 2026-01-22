CREATE TABLE ##Orders
(
	order_id INT,
	order_date DATE,
	customer_name VARCHAR(250),
	city VARCHAR(100),	
	order_amount MONEY
)
 
--INSERT INTO ##Orders
--	SELECT '1001','04/01/2017','David Smith','GuildFord',10000 UNION ALL	  
--	SELECT '1002','04/02/2017','David Jones','Arlington',20000 UNION ALL	  
--	SELECT '1003','04/03/2017','John Smith','Shalford',5000 UNION ALL	  
--	SELECT '1004','04/04/2017','Michael Smith','GuildFord',15000 UNION ALL	  
--	SELECT '1005','04/05/2017','David Williams','Shalford',7000 UNION ALL	  
--	SELECT '1006','04/06/2017','Paum Smith','GuildFord',25000 UNION ALL	 
--	SELECT '1007','04/10/2017','Andrew Smith','Arlington',15000 UNION ALL	  
--	SELECT '1008','04/11/2017','David Brown','Arlington',2000 UNION ALL	  
--	SELECT '1009','04/20/2017','Robert Smith','Shalford',1000 UNION ALL	  
--	SELECT '1010','04/25/2017','Peter Smith','GuildFord',500

INSERT INTO ##Orders
	SELECT '1001','04/01/2017','David Smith','GuildFord',10000 UNION ALL
	SELECT '1002','04/02/2017','David Jones','Arlington',20000 UNION ALL
	SELECT '1003','04/03/2017','John Smith','Shalford',5000 UNION ALL
	SELECT '1004','04/04/2017','Michael Smith','GuildFord',15000 UNION ALL
	SELECT '1005','04/05/2017','David Williams','Shalford',5000 UNION ALL -- Tie in Shalford
	SELECT '1006','04/06/2017','Paum Smith','GuildFord',15000 UNION ALL -- Tie in GuildFord
	SELECT '1007','04/10/2017','Andrew Smith','Arlington',15000 UNION ALL
	SELECT '1008','04/11/2017','David Brown','Arlington',2000 UNION ALL
	SELECT '1009','04/20/2017','Robert Smith','Shalford',1000 UNION ALL
	SELECT '1010','04/25/2017','Peter Smith','GuildFord',500

Select order_id, order_date, customer_name, order_amount,city, 
	rank() over(partition by city order by order_amount desc) 
From ##Orders

--Select order_id, order_date, customer_name, order_amount,city, 
--	dense_rank() over(partition by city order by order_amount desc) 
--From ##Orders

Select order_id, order_date, customer_name, order_amount,city, 
	row_number() over(partition by city order by order_amount desc) 
From ##Orders


/*
	Best Example For Row,Rank and Dense_rank
*/
with sa as(
	
	SELECT PlateNumber, IsActive, row_number() over(partition by PlateNumber order by IsActive) as Active
FROM Vmplate
--ORDER BY PlateNumber DESC
)
Select * From sa
where PlateNumber = 'CUSTOMER'


CREATE TABLE #Grades(
  [Student] VARCHAR(50),
  [Subject] VARCHAR(50),
  [Marks]   INT
)
GO
 
INSERT INTO #Grades VALUES 
('Jacob','Mathematics',100),
('Jacob','Science',95),
('Jacob','Geography',90),
('Amilee','Mathematics',90),
('Amilee','Science',90),
('Amilee','Geography',100)

SELECT *  FROM #Grades
PIVOT (
  SUM([Marks])
  FOR [Subject]
  IN (
    [Mathematics],
    [Science],
    [Geography]
  )
) AS PivotTable

--use penskevektorr

--Declare @Columns varchar(1000) =''

--Select @Columns +=  (quoteName(CountryStateCode)+',') From VmCountryState

--SET @Columns = LEFT(@Columns, LEN(@Columns) - 1)


----Check the result

--PRINT @Columns

--SELECT STRING_AGG(
--    CONCAT_WS(',', database_id, ISNULL(recovery_model_desc, ''), ISNULL(containment_desc, 'N/A')), CHAR(13)
--) AS DatabaseInfo
--FROM sys.databases;


--SELECT DIFFERENCE(SOUNDEX('Juice'), SOUNDEX('Jucy'))
--SELECT DIFFERENCE(1,2);

--Select STRING_AGG(CountryStateCode,',') From VmCountryState
--Henry V \n Henry VI
--Select 'Henry V \n Henry VI'



with temp( Element )as (
	Select 'A' UNION ALL
	Select 'B' UNION ALL
	Select 'B' UNION ALL
	Select 'A' UNION ALL
	Select 'A' UNION ALL
	Select 'A' UNION ALL
	Select 'B' UNION ALL
	Select 'C' UNION ALL
	Select 'D' UNION ALL
	Select 'C' UNION ALL
	Select 'C' UNION ALL
	Select 'C' UNION ALL
	Select 'C' 

),
temp1(El, Orders) as ( Select  element, Row_Number()Over(order By (SElect null) ) from temp
						--Rank()Over(Order By Element) From temp)

SELECT * FROM temp1
Group By El, Orders
Having COUNT(Orders) > 3