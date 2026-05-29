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

Select order_id, order_date, customer_name, order_amount,city, 
	dense_rank() over(partition by city order by order_amount desc) 
From ##Orders

Select order_id, order_date, customer_name, order_amount,city, 
	row_number() over(partition by city order by order_amount desc) 
From ##Orders

--Select DATEPART(quarter,DateAdd(Day,100,getDate()))
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
temp1(El, Orders) as ( Select  element, Row_Number()Over(order By (SElect null) ) --from temp)
						,Rank()Over(Order By Element) From temp)

SELECT * FROM temp1
Group By El, Orders
Having COUNT(Orders) > 3



--Gen Num
with genNum as (
	Select 1 as n
	Union All
	Select n+1 as n From genNum
	Where n < 50
	)

SELECT * FROM genNum
OPTION (MAXRECURSION 0)


CREATE TABLE ##Employee (
    EmpID    INT,
    EmpName  VARCHAR(50),
    DeptID   INT,
    Salary   DECIMAL(10,2),
    JoinDate DATE
)

INSERT INTO ##Employee VALUES
(1,  'Alice',   1, 5000,  '2020-01-15'),
(2,  'Bob',     1, 4000,  '2021-03-10'),
(3,  'Charlie', 1, 6000,  '2019-07-20'),
(4,  'David',   2, 8000,  '2020-05-11'),
(5,  'Eve',     2, 12000, '2018-09-01'),
(6,  'Frank',   2, 7000,  '2022-01-25'),
(7,  'Grace',   3, 9000,  '2019-11-30'),
(8,  'Henry',   3, 9500,  '2021-06-15'),
(9,  'Ivy',     3, 8500,  '2020-08-22'),
(10, 'Jack',    3, 7500,  '2023-02-10')

SELECT EmpName, Salary,

    -- Only current row
    SUM(Salary) OVER (
        ORDER BY Salary DESC
        ROWS BETWEEN CURRENT ROW AND CURRENT ROW
    ) AS CurrentOnly,

    -- Current + 1 before + 1 after (3 row window)
    SUM(Salary) OVER (
        ORDER BY Salary DESC
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ) AS ThreeRowWindow,

    -- Current + all before
    SUM(Salary) OVER (
        ORDER BY Salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS CumulativeTotal,

    -- Current + all after
    SUM(Salary) OVER (
        ORDER BY Salary DESC
        ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
    ) AS RemainingTotal,

    -- Entire partition
    SUM(Salary) OVER (
        ORDER BY Salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS GrandTotal
FROM ##Employee


CREATE TABLE ##SalesData (
    SalesRep  VARCHAR(50),
    Quarter   VARCHAR(10),
    Sales     DECIMAL(10,2)
)

INSERT INTO ##SalesData VALUES
('Alice', 'Q1', 15000),
('Alice', 'Q2', 18000),
('Alice', 'Q3', 12000),
('Alice', 'Q4', 20000),
('Bob',   'Q1', 10000),
('Bob',   'Q2', 14000),
('Bob',   'Q3', 16000),
('Bob',   'Q4', 11000),
('Eve',   'Q1', 20000),
('Eve',   'Q2', 22000),
('Eve',   'Q3', 19000),
('Eve',   'Q4', 25000)

SELECT SalesRep, [Q1], [Q2], [Q3], [Q4]
FROM (
    SELECT SalesRep, Quarter, Sales
    FROM ##SalesData
) AS src
PIVOT (
    SUM(Sales)              -- Aggregate function
    FOR Quarter IN          -- Column to pivot
    ([Q1], [Q2], [Q3], [Q4]) -- Values become columns
) AS pvt

-- Add Year to the mix
CREATE TABLE ##SalesData2 (
    SalesRep  VARCHAR(50),
    SaleYear  INT,
    Quarter   VARCHAR(10),
    Sales     DECIMAL(10,2)
)

INSERT INTO ##SalesData2 VALUES
('Alice', 2023, 'Q1', 15000),
('Alice', 2023, 'Q1', 15000),
('Alice', 2023, 'Q2', 18000),
('Alice', 2024, 'Q1', 20000),
('Alice', 2024, 'Q2', 25000),
('Bob',   2023, 'Q1', 10000),
('Bob',   2023, 'Q2', 14000),
('Bob',   2024, 'Q1', 16000),
('Bob',   2024, 'Q2', 18000),
('Bob',   2024, 'Q3', 18000)

SELECT SalesRep, SaleYear, [Q1], [Q2]
FROM (
    SELECT SalesRep, SaleYear, Quarter, Sales
    FROM ##SalesData2
) AS src
PIVOT (
    SUM(Sales)
    FOR Quarter IN ([Q1], [Q2])
) AS pvt
ORDER BY SalesRep, SaleYear


DECLARE @Columns NVARCHAR(MAX) = ''
DECLARE @SQL     NVARCHAR(MAX) = ''

-- Step 1: Build column list dynamically
SELECT @Columns += ',' + QUOTENAME(Quarter)
FROM ##SalesData
GROUP BY Quarter
ORDER BY Quarter

SELECT @Columns

-- Remove leading comma
SET @Columns = STUFF(@Columns, 1, 1, '')
SELECT @Columns

-- Step 2: Build dynamic SQL
SET @SQL = '
SELECT SalesRep, ' + @Columns + '
FROM (
    SELECT SalesRep, Quarter, Sales
    FROM ##SalesData
) AS src
PIVOT (
    SUM(Sales)
    FOR Quarter IN (' + @Columns + ')
) AS pvt
ORDER BY SalesRep'

-- Step 3: Execute
EXEC sp_executesql @SQL

SELECT DATEPART(hour, '2021/01/06 05:30')


Create table ##Logs (id int, num int)
--Truncate table ##Logs
insert into ##Logs (id, num) values ('1', '1')
insert into ##Logs (id, num) values ('2', '2')
insert into ##Logs (id, num) values ('3', '1')
insert into ##Logs (id, num) values ('4', '2')
insert into ##Logs (id, num) values ('5', '1')
insert into ##Logs (id, num) values ('6', '2')
insert into ##Logs (id, num) values ('7', '2')
insert into ##Logs (id, num) values ('8', '2')
insert into ##Logs (id, num) values ('9', '2')

WITH CTE AS (
    SELECT id,num,
        --ROW_NUMBER() OVER (ORDER BY id)  as ld,
        id- ROW_NUMBER() OVER (PARTITION BY num ORDER BY id) AS grp 
    FROM ##Logs
)
SELECT num AS ConsecutiveNums
FROM CTE
GROUP BY num, grp
HAVING COUNT(*) >= 3
Order BY ConsecutiveNums



Create table ##Employee (id int, name varchar(255), salary int, departmentId int)
Create table ##Department (id int, name varchar(255))
--Truncate table Employee
insert into ##Employee (id, name, salary, departmentId) values ('1', 'Joe', '70000', '1')
insert into ##Employee (id, name, salary, departmentId) values ('2', 'Jim', '90000', '1')
insert into ##Employee (id, name, salary, departmentId) values ('3', 'Henry', '80000', '2')
insert into ##Employee (id, name, salary, departmentId) values ('4', 'Sam', '60000', '2')
insert into ##Employee (id, name, salary, departmentId) values ('5', 'Max', '90000', '1')
--Truncate table Department
insert into ##Department (id, name) values ('1', 'IT')
insert into ##Department (id, name) values ('2', 'Sales')

SELECT * FROM ##Employee
Select rk.id, rk.name from (
		SELECT  id, name, dense_rank()over(Partition by departmentid order by salary desc ) as rnk
		FROM ##Employee
	) as rk
Inner Join ##Department d
	on d.id = rk.id
Where rnk = 1



Declare @CountinousInt int = 3;
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

),temp2 as ( 
	select ROW_NUMBER() Over( Order by (Select NUll)) as Rn, Element as El 
	From Temp
),
temp3 as(
	SELECT Rn, El, (Rn - DENSE_RANK() Over(Partition by El Order BY Rn asc )) as Serial
FROM temp2
Order by Rn
OFFSET 0 ROWS
)

SELECT El, Serial
FROM temp3
Group by El, Serial 
Having Count(*) >= @CountinousInt

-----------------------------------------------------------------------------------------------------------------------

insert into Trips (id, client_id, driver_id, city_id, status, request_at) values ('1', '1', '10', '1', 'completed', '2013-10-01')
insert into Trips (id, client_id, driver_id, city_id, status, request_at) values ('2', '2', '11', '1', 'cancelled_by_driver', '2013-10-01')
insert into Trips (id, client_id, driver_id, city_id, status, request_at) values ('3', '3', '12', '6', 'completed', '2013-10-01')
insert into Trips (id, client_id, driver_id, city_id, status, request_at) values ('4', '4', '13', '6', 'cancelled_by_client', '2013-10-01')
insert into Trips (id, client_id, driver_id, city_id, status, request_at) values ('5', '1', '10', '1', 'completed', '2013-10-02')
insert into Trips (id, client_id, driver_id, city_id, status, request_at) values ('6', '2', '11', '6', 'completed', '2013-10-02')
insert into Trips (id, client_id, driver_id, city_id, status, request_at) values ('7', '3', '12', '6', 'completed', '2013-10-02')
insert into Trips (id, client_id, driver_id, city_id, status, request_at) values ('8', '2', '12', '12', 'completed', '2013-10-03')
insert into Trips (id, client_id, driver_id, city_id, status, request_at) values ('9', '3', '10', '12', 'completed', '2013-10-03')
insert into Trips (id, client_id, driver_id, city_id, status, request_at) values ('10', '4', '13', '12', 'cancelled_by_driver', '2013-10-03')
Truncate table Users
insert into Users (users_id, banned, role) values ('1', 'No', 'client')
insert into Users (users_id, banned, role) values ('2', 'Yes', 'client')
insert into Users (users_id, banned, role) values ('3', 'No', 'client')
insert into Users (users_id, banned, role) values ('4', 'No', 'client')
insert into Users (users_id, banned, role) values ('10', 'No', 'driver')
insert into Users (users_id, banned, role) values ('11', 'No', 'driver')
insert into Users (users_id, banned, role) values ('12', 'No', 'driver')
insert into Users (users_id, banned, role) values ('13', 'No', 'driver')


	SELECT Distinct request_at as Day, 
		Cast( 
				Sum( Case When status != 'Completed' Then 1.00 Else 0.00 End ) 
				Over(Partition By request_at) 
				/ 
				Count(request_at) Over(Partition By request_at) 
			as decimal (10,2))
		 as [Cancellation Rate]		
	FROM Trips t
		Inner join Users u
			on t.client_id = u.users_id
		Inner join Users u1 
			on t.driver_id = u1.users_id
	Where ( u1.banned != 'Yes' And  u.banned != 'Yes' )
	And ( request_at > '2013-09-29' AND request_at < '2013-10-04')


	SELECT  request_at as Day, 
		Cast( 
				Sum( Case When status != 'Completed' Then 1.00 Else 0.00 End ) 
				Over(Partition By request_at) 
				/ 
				Count(request_at) Over(Partition By request_at)
			as decimal (10,2))
		 as [Cancellation Rate]		
	FROM Trips t
		Inner join Users u
			on t.client_id = u.users_id
		Inner join Users u1 
			on t.driver_id = u1.users_id
	Where ( u1.banned != 'Yes' And  u.banned != 'Yes' )
	And ( request_at > '2013-09-29' AND request_at < '2013-10-04')
	Group by request_at



-----------------------------------------------------------------------------------------------------------------------


CREATE TABLE reactions (
    user_id INT,
    content_id INT,
    reaction VARCHAR(255)
)

Truncate table reactions
insert into reactions (user_id, content_id, reaction) values ('1', '101', 'like')
insert into reactions (user_id, content_id, reaction) values ('1', '102', 'like')
insert into reactions (user_id, content_id, reaction) values ('1', '103', 'like')
insert into reactions (user_id, content_id, reaction) values ('1', '104', 'wow')
insert into reactions (user_id, content_id, reaction) values ('1', '105', 'like')
insert into reactions (user_id, content_id, reaction) values ('2', '201', 'like')
insert into reactions (user_id, content_id, reaction) values ('2', '202', 'wow')
insert into reactions (user_id, content_id, reaction) values ('2', '203', 'sad')
insert into reactions (user_id, content_id, reaction) values ('2', '204', 'like')
insert into reactions (user_id, content_id, reaction) values ('2', '205', 'wow')
insert into reactions (user_id, content_id, reaction) values ('3', '301', 'love')
insert into reactions (user_id, content_id, reaction) values ('3', '302', 'love')
insert into reactions (user_id, content_id, reaction) values ('3', '303', 'love')
insert into reactions (user_id, content_id, reaction) values ('3', '304', 'love')
insert into reactions (user_id, content_id, reaction) values ('3', '305', 'love')

;with reaction as (
		SELECT user_id, content_id, reaction,
		Row_Number()Over(partition by user_id order by user_id ) as Rn,
		Rank()Over(partition by user_id order by reaction ) as ReactionRn
		FROM reactions
	), ValidReaction as (
		Select  user_id, 
		Cast (
			sum( Case when ReactionRn = 1 Then 1 Else 0.00 End)--Over(partition by reaction order by reaction ) 
			/ count(user_id)  as decimal (10,2)
		)
		as Ratio
		From reaction
		Where rn >= 4
		Group by user_id--, reaction
	)
SELECT Distinct v.user_id,  r.reaction as dominant_reaction, Ratio as reaction_ratio
FROM ValidReaction v
	inner join reactions r
		on v.user_id = r.user_id
	Inner join reaction r1
		on r1.user_id = r.user_id
		and r.reaction = r1.reaction
where Ratio > 0.60
and r1.ReactionRn = 1
order By Ratio desc, user_id asc


WITH ReactionCount AS (
    SELECT 
        user_id,
        reaction,
        COUNT(*) AS reaction_count
    FROM reactions
    GROUP BY user_id, reaction
),
UserTotal AS (
    SELECT 
        user_id,
        COUNT(DISTINCT content_id) AS total_content
    FROM reactions
    GROUP BY user_id
)
	SELECT 
		rc.user_id, rc.reaction AS dominant_reaction,
		CAST(
			1.0 * rc.reaction_count / ut.total_content
			AS DECIMAL(10,2)
		) AS reaction_ratio
	FROM ReactionCount rc
	INNER JOIN UserTotal ut
		ON rc.user_id = ut.user_id
	WHERE ut.total_content >= 5
	AND (
		1.0 * rc.reaction_count / ut.total_content
	) >= 0.60
	ORDER BY reaction_ratio DESC, rc.user_id ASC;

---------------------------------------------------------------------------------------------------


Create Table Products(
	Category Varchar(100), Brand Varchar(100)
	)

INSERT INTO products (category, Brand)
VALUES 
('Beverages', 'Coca Cola'),
(NULL, 'Pepsi'),
(NULL, 'Sprite'),
(NULL, 'Fanta'),
('Snacks', 'Lays'),
(NULL, 'Doritos'),
(NULL, 'Kurkure'),
('Items', 'Lap'),
(NULL, 'mouse'),
(NULL, 'key'),
(NULL, 'switch'),
(NULL, 'cpu');

/*
	1 wrong
*/
SELECT 
    brand,
    MAX(category) OVER (ORDER BY (SELECT NULL) ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS filled_category
FROM products;

/*
	2 Advance
*/

with cte1 as(
	SELECT Category,Brand,ROW_NUMBER() over(order by (select null)) as rn
	FROM Products
),cte2 as (
	SELECT Category,Brand,rn, LEAD(rn) over(order by rn) as next_rn
	FROM cte1
	Where Category is not null
)
SELECT cte2.Category, cte1.Brand,*
FROM cte1
	 Inner join cte2 
		on cte1.rn >= cte2.rn
	and ( cte1.rn < cte2.next_rn or cte2.next_rn is null)


/*
	3
*/

WITH cte AS
(
    SELECT 
        ROW_NUMBER() OVER(ORDER BY (SELECT NULL)) AS Id,
        Category,
        Brand
    FROM Products
)
SELECT 
    x.Category,
    t.Brand
FROM cte t
OUTER APPLY
(
    SELECT Category
    FROM
    (
        SELECT 
            t2.Category,
            ROW_NUMBER() OVER(ORDER BY t2.Id DESC) AS rn
        FROM cte t2
        WHERE t2.Category IS NOT NULL
          AND t2.Id <= t.Id
    ) A
    WHERE rn = 1
) x;


/*
	4
*/

WITH Cte1 AS
(
    SELECT *,
           ROW_NUMBER() OVER(ORDER BY (SELECT NULL)) AS rn
    FROM Products
),
Cte2 AS
(
    SELECT *,
           COUNT(Category) OVER(ORDER BY rn) AS Grp
    FROM Cte1
)
SELECT
    MAX(Category) OVER(PARTITION BY Grp) AS Category,
    Brand
FROM Cte2;


/*
	5 
*/

WITH cte AS
(
    SELECT 
        ROW_NUMBER() OVER(ORDER BY (SELECT NULL)) AS Id,
        Category,
        Brand
    FROM Products
),
cte2 AS
(
    SELECT
        t1.Id,
        t1.Brand,
        t2.Category,
        ROW_NUMBER() OVER(
            PARTITION BY t1.Id
            ORDER BY t2.Id DESC
        ) AS rn
    FROM cte t1
    LEFT JOIN cte t2
        ON t2.Id <= t1.Id
       AND t2.Category IS NOT NULL
)
SELECT
    Category,
    Brand
FROM cte2
WHERE rn = 1;

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

with main(City,Amount)as( 

		select 'Salem', 1000 UNION ALL
		select 'Salem', 1000 UNION ALL
		select 'Salem', 4000 UNION ALL
		select 'CHN', 3000 UNION ALL
		select 'Chn', 2000 
	)
SELECT city, sum(Amount) Over (Partition by city ) 
FROM main
---------------------------------------------------------------------
CREATE TABLE course_completions (
    user_id INT,
    course_id INT,
    course_name VARCHAR(100),
    completion_date DATE,
    course_rating Decimal (5,2)
)
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('1', '101', 'Python Basics', '2024-01-05', '5')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('1', '102', 'SQL Fundamentals', '2024-02-10', '4')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('1', '103', 'JavaScript', '2024-03-15', '5')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('1', '104', 'React Basics', '2024-04-20', '4')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('1', '105', 'Node.js', '2024-05-25', '5')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('1', '106', 'Docker', '2024-06-30', '4')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('2', '101', 'Python Basics', '2024-01-08', '4')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('2', '104', 'React Basics', '2024-02-14', '5')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('2', '105', 'Node.js', '2024-03-20', '4')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('2', '106', 'Docker', '2024-04-25', '5')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('2', '107', 'AWS Fundamentals', '2024-05-30', '4')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('3', '101', 'Python Basics', '2024-01-10', '3')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('3', '102', 'SQL Fundamentals', '2024-02-12', '3')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('3', '103', 'JavaScript', '2024-03-18', '3')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('3', '104', 'React Basics', '2024-04-22', '2')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('3', '105', 'Node.js', '2024-05-28', '3')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('4', '101', 'Python Basics', '2024-01-12', '5')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('4', '108', 'Data Science', '2024-02-16', '5')
insert into course_completions (user_id, course_id, course_name, completion_date, course_rating) values ('4', '109', 'Machine Learning', '2024-03-22', '5')

SELECT * FROM course_completions


with top_performer as(
		Select   user_id, count(course_id) as courseCount, 
				 cast( AVG(course_rating) as float) AS avgRating
		From course_completions 
		Group by user_id
		having count(*) >=5 
	),
	seq_order as (
		SELECT c.user_id, t.courseCount, c.course_name as first_course, Lead(course_name) over( Partition by c.user_id order by completion_date asc) as second_course
		FROM course_completions c
			Inner Join top_performer t	
				on t.user_id = c.user_id
		Where avgRating >= 4
) 
SELECT	 first_course, second_course, count(*)   as transition_count
	
FROM seq_order
where second_course is not null
group by first_course, second_course
order by transition_count  desc, first_course asc, second_course asc