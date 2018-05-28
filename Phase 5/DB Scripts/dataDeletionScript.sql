USE book_fetch;
SET SQL_SAFE_UPDATES = 0;

DELETE FROM keyword;
DELETE FROM authors;
DELETE FROM category;
DELETE FROM being_purchased;
DELETE FROM purchased;
DELETE FROM books_used;
DELETE FROM recommendation;
DELETE FROM employee;
DELETE FROM representative;
DELETE FROM orders;
DELETE FROM taking_course;
DELETE FROM student_reviews;
DELETE FROM book;
DELETE FROM cart;
DELETE FROM course;
DELETE FROM instructor;
DELETE FROM trouble_ticket;
DELETE FROM department;
DELETE FROM student;
DELETE FROM customer_support_user;
DELETE FROM university;
DELETE FROM administrator;
DELETE FROM users;

SET SQL_SAFE_UPDATES = 1;