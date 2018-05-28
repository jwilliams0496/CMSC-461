# Query 1
SELECT * FROM student LEFT JOIN users ON (student.email = users.email) WHERE student.univ_name = 'UMBC';

# Query 2
SELECT * FROM student LEFT JOIN users ON (student.email = users.email) WHERE student.student_status = 'Grad';

# Query 3
SELECT *,
	(
    SELECT SUM(purchased.quantity)
    FROM purchased
    WHERE purchased.student_email = student.email
    ) AS num_books_purchased
FROM student JOIN users ON (student.email = users.email)
WHERE student.major = "Computer Science"
HAVING num_books_purchased > 2;

# Query 4
SELECT book.title,
	(
    SELECT SUM(purchased.quantity)
    FROM purchased
    WHERE purchased.book_title = book.title
    ) AS num_books_purchased
FROM book
HAVING num_books_purchased > 0
ORDER BY num_books_purchased DESC;

# Query 5
SELECT book.title,
	(
    SELECT GROUP_CONCAT(category.category)
    from category
    WHERE category.book_title = book.title
    ) AS all_categories
FROM book;

# Query 6
SELECT books_used.book_title, books_used.course_name
FROM books_used
JOIN category ON (books_used.book_title = category.book_title)
WHERE category.category != 'Computer Science';

# Query 7
SELECT purchased.book_title
FROM purchased
WHERE purchased.student_email NOT IN
	(
    SELECT taking_course.student_email
    FROM taking_course
    )
AND
	(
	SELECT COUNT(purchased.book_title)
	FROM purchased
	JOIN keyword ON (purchased.book_title = keyword.book_title)
	WHERE keyword.keyword IN
		(
		SELECT books_used.book_title
		FROM books_used
		JOIN keyword ON (books_used.book_title = keyword.book_title)
		)
	) >= 2;
    
# Query 8
SELECT book.title,
	(
    SELECT COUNT(books_used.book_title)
    FROM books_used
    WHERE book.title = books_used.book_title
    ) AS num_courses_used
FROM book;

# Query 9
SELECT book.title
FROM book
WHERE book.title IN
	(
	SELECT category.book_title
	FROM category
	JOIN keyword ON (category.book_title = keyword.book_title)
	WHERE category.category = 'Linear Algebra'
	OR keyword.keyword = 'Linear'
	OR keyword.keyword = 'Algebra'
    );

# Query 10
SELECT book.title
FROM book
WHERE book.rating > 3;

# Query 11
SELECT book.title,
	(
    SELECT COUNT(purchased.book_title)
    FROM purchased
    WHERE purchased.book_title = book.title
    ) AS num_purchased, book.rating
FROM book
ORDER BY book.rating DESC;

# Query 12
SELECT category.category AS cat,
	(
    SELECT AVG(purchased.quantity)
    FROM purchased
    JOIN category ON (purchased.book_title = category.book_title)
    WHERE category.category = cat
    ) AS avg_purchased
FROM category
ORDER BY avg_purchased DESC;

# Query 13
SELECT univ_name, dept_name,
	(
    SELECT GROUP_CONCAT(course.course_name)
    FROM course
    WHERE course.dept_name = department.dept_name
    ) AS courses,
	(
	SELECT COUNT(instructor.instr_email)
    FROM instructor
    WHERE instructor.instr_email IN
		(
        SELECT course.instr_email
        FROM course
        WHERE course.dept_name = department.dept_name
        )
    ) AS num_instr
FROM department;

# Query 14
SELECT university.univ_name,
	(
    SELECT COUNT(purchased.quantity)
    FROM purchased
    JOIN books_used ON (purchased.book_title = books_used.book_title)
    WHERE purchased.book_title = books_used.book_title
    AND books_used.univ_name = university.univ_name
    ) AS num_purchased,
    (
    SELECT SUM(book.price)
    FROM book
    JOIN books_used ON (book.title = books_used.book_title)
    JOIN purchased ON (book.title = purchased.book_title)
    WHERE book.title = books_used.book_title
    AND books_used.univ_name = university.univ_name
    ) AS total_price
FROM university;

# Query 15
SELECT users.first_name, users.last_name, 
	(
    SELECT COUNT(trouble_ticket.ticket_id)
    FROM trouble_ticket
    WHERE trouble_ticket.creator_name = users.first_name
    ) AS num_tickets_created
FROM customer_support_user
JOIN employee ON (customer_support_user.email = employee.email)
JOIN users ON (customer_support_user.email = users.email);

# Query 16
SELECT users.first_name, users.last_name, employee.salary FROM administrator
JOIN employee ON (administrator.email = employee.email)
JOIN users ON (administrator.email = users.email)
ORDER BY employee.salary DESC;

# Query 17
SELECT users.first_name, users.last_name, 
	(
    SELECT COUNT(trouble_ticket.ticket_id)
    FROM trouble_ticket
    WHERE trouble_ticket.administrator_name = users.first_name
    AND trouble_ticket.state = 'completed'
    ) AS num_tickets_completed
FROM administrator
JOIN employee ON (administrator.email = employee.email)
JOIN users ON (administrator.email = users.email);

# Query 18
SELECT DISTINCT trouble_ticket.state as ticket_state,
	(
    SELECT COUNT(trouble_ticket.creator_type)
    FROM trouble_ticket
    WHERE trouble_ticket.creator_type = 'student'
    AND trouble_ticket.state = ticket_state
    ) AS num_student,
    (
    SELECT COUNT(trouble_ticket.creator_type)
    FROM trouble_ticket
    WHERE trouble_ticket.creator_type = 'customer_support_user'
    AND trouble_ticket.state = ticket_state
    ) AS num_customer_support_user
FROM trouble_ticket;

# Query 19
SELECT AVG(B.date_logged - A.date_logged) AS avg_time
FROM trouble_ticket AS A INNER JOIN trouble_ticket AS B ON (B.ticket_id = A.ticket_id)
WHERE A.state = 'new' AND B.state = 'completed'
ORDER BY A.ticket_id ASC;

# Query 20
SELECT A.ticket_id AS ticket_id, D.title AS title, D.description AS description,
D.creator_type AS creator_type, D.creator_name AS creator_name, D.date_logged AS date_created,
C.customer_support_user_name AS customer_support_user, C.administrator_name AS administrator_assigned, C.date_logged AS date_assigned,
B.date_logged AS date_inprocess,
A.date_logged AS date_completed, A.solution AS solution
FROM trouble_ticket AS A
INNER JOIN trouble_ticket AS B ON (B.ticket_id = A.ticket_id)
INNER JOIN trouble_ticket AS C ON (C.ticket_id = A.ticket_id)
INNER JOIN trouble_ticket AS D ON (D.ticket_id = A.ticket_id)
WHERE A.state = 'completed' AND B.state = 'in-process'
AND C.state = 'assigned' AND D.state = 'new';

# Query 21 *** Doesn't work. This one is just too difficult ***
SELECT DISTINCT P.student_email, B.title AS recomendation
FROM book as B
JOIN purchased AS P ON (P.book_title = B.title)
WHERE P.student_email IN
	(
    SELECT purchased.student_email
	FROM purchased
    WHERE purchased.student_email = P.student_email
    AND purchased.student_email IN
		(
        SELECT (current_date() - purchased.date_purchased) AS time_difference
		FROM purchased
		WHERE purchased.student_email = P.student_email
		HAVING time_difference < 30
        )
    )
AND B.title NOT IN
	(
    SELECT purchased.book_title
    FROM purchased
    )
AND B.title IN
	(
    SELECT DISTINCT category.book_title
    FROM category
    WHERE B.title = category.book_title
    )
AND B.title IN
	(
	SELECT keyword.book_title
    FROM keyword
    WHERE B.title = keyword.book_title
    );
    
# Query 22 *** Doesn't work. This one is just too difficult ***
SELECT book.title,
	(
    SELECT COUNT(purchased.student_email)
    FROM purchased
    WHERE purchased.book_title IN
		(
        SELECT keyword.book_title
        FROM keyword JOIN purchased ON (purchased.book_title = keyword.book_title)
        )
	) AS num_students
FROM book;

# Query 23
SELECT book.title, book.rating,
	(
    SELECT COUNT(student_reviews.book_title)
    FROM student_reviews
    WHERE book.title = student_reviews.book_title
    ) AS num_students
FROM book
ORDER BY num_students DESC;

# Query 24
SELECT book.title, book.rating,
    (
    SELECT users.first_name FROM student
	LEFT JOIN users ON (student.email = users.email)
    LEFT JOIN student_reviews ON (student.email = student_reviews.student_email)
    WHERE student.email = users.email = student_reviews.student_email
    ) AS student_first_name,
	(
    SELECT users.last_name FROM student
	LEFT JOIN users ON (student.email = users.email)
    LEFT JOIN student_reviews ON (student.email = student_reviews.student_email)
    WHERE student.email = users.email = student_reviews.student_email
    ) AS student_last_name,
	(
    SELECT student.univ_name FROM student
	LEFT JOIN users ON (student.email = users.email)
    LEFT JOIN student_reviews ON (student.email = student_reviews.student_email)
    WHERE student.email = users.email = student_reviews.student_email
    ) AS student_univ_name
FROM book
WHERE book.rating = 5.0;