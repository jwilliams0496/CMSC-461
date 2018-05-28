USE book_fetch;

ALTER TABLE book DROP INDEX
book_title;

ALTER TABLE keyword DROP INDEX
book_keyword;

ALTER TABLE category DROP INDEX
book_category;

ALTER TABLE users DROP INDEX
users_email;

ALTER TABLE being_purchased DROP INDEX
student_and_book;

ALTER TABLE purchased DROP INDEX
student_book_and_date;

ALTER TABLE books_used DROP INDEX
book_and_course;