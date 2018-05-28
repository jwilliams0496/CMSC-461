USE book_fetch;

ALTER TABLE book ADD INDEX
book_title(title);

ALTER TABLE keyword ADD INDEX
book_keyword(keyword);

ALTER TABLE category ADD INDEX
book_category(category);

ALTER TABLE users ADD INDEX
users_email(email);

ALTER TABLE being_purchased ADD INDEX
student_and_book(student_email, book_title);

ALTER TABLE purchased ADD INDEX
student_book_and_date(student_email, book_title, date_purchased);

ALTER TABLE books_used ADD INDEX
book_and_course(book_title, course_name);