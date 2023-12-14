USE employees;

SELECT 
    departments.dept_name,
    AVG(salaries.salary) AS átlagfizu_részleg
FROM
    employees
        JOIN
    dept_emp ON employees.emp_no = dept_emp.emp_no
        JOIN
    departments ON dept_emp.dept_no = departments.dept_no
        JOIN
    salaries ON employees.emp_no = salaries.emp_no
GROUP BY departments.dept_name
ORDER BY átlagfizu_részleg DESC;

SELECT 
    employees.*,
    MAX(titles.to_date),
    TIMESTAMPDIFF(YEAR,
        MIN(titles.from_date),
        CURDATE()) AS eltoltott_evek
FROM
    employees
        JOIN
    titles ON employees.emp_no = titles.emp_no
WHERE
    titles.to_date = (SELECT 
            MAX(to_date)
        FROM
            titles)
GROUP BY employees.emp_no
ORDER BY eltoltott_evek DESC;

SELECT 
    employees.emp_no,
    employees.first_name,
    employees.last_name,
    COUNT(DISTINCT titles.title) AS hany_darab_title
FROM
    employees
        JOIN
    titles ON employees.emp_no = titles.emp_no
GROUP BY employees.emp_no;

SELECT 
    employees.first_name,
    employees.last_name,
    titles.title,
    departments.dept_name
FROM
    employees
        JOIN
    titles ON employees.emp_no = titles.emp_no
        JOIN
    dept_emp ON employees.emp_no = dept_emp.emp_no
        JOIN
    departments ON dept_emp.dept_no = departments.dept_no
WHERE
    titles.to_date = '9999-01-01' AND departments.dept_name = 'Research';
   
SELECT 
    employees.first_name,
    employees.last_name,
    departments.dept_name AS ahol_menedzser_volt
FROM
    employees
        JOIN
    dept_manager ON employees.emp_no = dept_manager.emp_no
        JOIN
    departments ON dept_manager.dept_no = departments.dept_no
  
DELIMITER //

CREATE PROCEDURE atlagfizu_reszleg (IN reszleg_nev VARCHAR(50), OUT atlagfizu DECIMAL(15,4))
BEGIN
    DECLARE dept_id VARCHAR(4);

SELECT 
    dept_no
INTO dept_id FROM
    departments
WHERE
    dept_name = reszleg_nev;

SELECT 
    AVG(salary)
INTO atlagfizu FROM
    employees
        JOIN
    dept_emp ON employees.emp_no = dept_emp.emp_no
        JOIN
    salaries ON employees.emp_no = salaries.emp_no
WHERE
    dept_emp.dept_no = dept_id
        AND salaries.to_date = '9999-01-01';
END //

DELIMITER ;

CALL atlagfizu_reszleg('Production', @atlagfizu);
SELECT @atlagfizu AS atlagfizu;

DELIMITER //

CREATE FUNCTION atlagfizu_reszleg_2(dept_id VARCHAR(4))
RETURNS DECIMAL(15,4) DETERMINISTIC
BEGIN
    DECLARE atlagfizu DECIMAL(15,4);

SELECT 
    AVG(salary)
INTO atlagfizu FROM
    employees
        JOIN
    dept_emp ON employees.emp_no = dept_emp.emp_no
        JOIN
    salaries ON employees.emp_no = salaries.emp_no
WHERE
    dept_emp.dept_no = dept_id
        AND salaries.to_date = '9999-01-01';

    RETURN atlagfizu;
END //

DELIMITER ;

SELECT atlagfizu_reszleg_2('d008') AS átlagfizetés;




