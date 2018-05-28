#CREATE DATABASE book_fetch;
#GRANT ALL ON book_fetch.* To root@'localhost';
USE book_fetch;

CREATE TABLE IF NOT EXISTS book
(
  isbn VARCHAR(50) NOT NULL,
  isbn13 VARCHAR(50) NOT NULL,
  book_type VARCHAR(30) NOT NULL CHECK (book_type IN ('new', 'used')),
  purchase_type VARCHAR(30) NOT NULL NOT NULL CHECK (purchase_type IN ('buy', 'rent')),
  price FLOAT NOT NULL,
  quantity INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  publisher VARCHAR(233) NOT NULL,
  publish_date VARCHAR(4) NOT NULL,
  edition_number INT NOT NULL,
  book_lang VARCHAR(30) NOT NULL,
  book_format VARCHAR(30) NOT NULL CHECK (book_format IN ('hardcover', 'paperback', 'electronic')),
  weight FLOAT NOT NULL,
  rating FLOAT NOT NULL,
  PRIMARY KEY (title)
);

CREATE TABLE IF NOT EXISTS university
(
  univ_name VARCHAR(20) NOT NULL,
  address VARCHAR(100) NOT NULL,
  PRIMARY KEY (univ_name)
);

CREATE TABLE IF NOT EXISTS department
(
  dept_name VARCHAR(100) NOT NULL,
  univ_name VARCHAR(20) NOT NULL,
  PRIMARY KEY (dept_name, univ_name),
  FOREIGN KEY (univ_name) REFERENCES university(univ_name)
);

CREATE TABLE IF NOT EXISTS instructor
(
  instr_email VARCHAR(30) NOT NULL,
  first_name VARCHAR(30) NOT NULL,
  last_name VARCHAR(30) NOT NULL,
  dept_name VARCHAR(100) NOT NULL,
  univ_name VARCHAR(20) NOT NULL,
  PRIMARY KEY (instr_email),
  FOREIGN KEY (dept_name) REFERENCES department(dept_name),
  FOREIGN KEY (univ_name) REFERENCES university(univ_name)
);

CREATE TABLE IF NOT EXISTS representative
(
  first_name VARCHAR(30) NOT NULL,
  last_name VARCHAR(30) NOT NULL,
  email VARCHAR(50) NOT NULL,
  gender VARCHAR(15),
  phone VARCHAR(15) NOT NULL,
  snn VARCHAR(20),
  univ_name VARCHAR(20) NOT NULL,
  PRIMARY KEY (univ_name),
  FOREIGN KEY (univ_name) REFERENCES university(univ_name)
);

CREATE TABLE IF NOT EXISTS keyword
(
  book_title VARCHAR(255) NOT NULL,
  keyword VARCHAR(20) NOT NULL,
  FOREIGN KEY (book_title) REFERENCES book(title)
);

CREATE TABLE IF NOT EXISTS authors
(
  author VARCHAR(50) NOT NULL,
  book_title VARCHAR(255) NOT NULL,
  FOREIGN KEY (book_title) REFERENCES book(title)
);

CREATE TABLE IF NOT EXISTS category
(
  book_title VARCHAR(255) NOT NULL,
  category VARCHAR(255) NOT NULL,
  PRIMARY KEY(book_title, category),
  FOREIGN KEY (book_title) REFERENCES book(title)
);

# Root of inheritance tree for all using the site, parent of employee and student
CREATE TABLE IF NOT EXISTS users
(
  first_name VARCHAR(30) NOT NULL,
  last_name VARCHAR(30) NOT NULL,
  email VARCHAR(50) NOT NULL,
  address VARCHAR(255) NOT NULL,
  phone VARCHAR(15) NOT NULL,
  PRIMARY KEY (email) # ***none of hte users have an id, so email will now be user primary key***
);

# Inherits from users
CREATE TABLE IF NOT EXISTS student
(
  email VARCHAR(50) PRIMARY KEY REFERENCES users (email),
  birth_date DATE NOT NULL,
  major VARCHAR(30) NOT NULL,
  student_status VARCHAR(20) NOT NULL CHECK (student_status IN ('Grad', 'UnderGrad')),
  student_year INT NOT NULL CHECK (student_year IN (1, 2, 3, 4)),
  univ_name VARCHAR(20) NOT NULL,
  FOREIGN KEY (univ_name) REFERENCES university(univ_name)
);

# Inherits from users, employee is parent of administrator and customer_support_user
CREATE TABLE IF NOT EXISTS employee
(
  email VARCHAR(50) PRIMARY KEY REFERENCES users (email),
  gender VARCHAR(15) NOT NULL,
  salary INT,
  ssn VARCHAR(20) NOT NULL
);

# Inherits from employee and user
CREATE TABLE IF NOT EXISTS customer_support_user
(
  email VARCHAR(50) PRIMARY KEY REFERENCES employee (email)
);

# Inherits from employee and user
CREATE TABLE IF NOT EXISTS administrator
(
  is_super BOOLEAN NOT NULL,
  email VARCHAR(50) PRIMARY KEY REFERENCES employee (email)
);

CREATE TABLE IF NOT EXISTS trouble_ticket
(
  ticket_id VARCHAR(30) NOT NULL,
  state VARCHAR(30) NOT NULL CHECK (state IN ('new', 'in-process', 'assigned', 'completed')),
  category VARCHAR(30) NOT NULL CHECK (category IN ('user profile', 'products', 'cart', 'orders', 'other')),
  date_logged DATE NOT NULL,
  title VARCHAR(50) NOT NULL,
  description VARCHAR(255),
  creator_name VARCHAR(30) NOT NULL, # ticket must have a creator
  creator_type VARCHAR(30) NOT NULL CHECK (creator_type IN ('customer_support_user', 'student')), # type of use
  customer_support_user_name VARCHAR(30), # ticket may not be assigned yet
  administrator_name CHAR(30), # ticket may not be assigned yet
  solution CHAR(255),
  PRIMARY KEY (ticket_id, state)
  #FOREIGN KEY (administrator_name) REFERENCES users(first_name)
);

CREATE TABLE IF NOT EXISTS cart
(
  date_created DATE NOT NULL,
  last_updated DATE NOT NULL,
  student_email VARCHAR(50) NOT NULL,
  PRIMARY KEY (student_email),
  FOREIGN KEY (student_email) REFERENCES student(email)
);

CREATE TABLE IF NOT EXISTS orders
(
  student_email VARCHAR(50) NOT NULL,
  date_created DATE NOT NULL,
  INDEX (date_created), # mysql requires date columns to be index before they can be referenced
  date_fulfilled DATE, # order may not be complete yet
  shipping_type VARCHAR(20) NOT NULL CHECK (shipping_type IN ('standard', '2-day' ,'1-day')),
  card_num VARCHAR(20) NOT NULL,
  card_exp DATE,
  card_name VARCHAR(50) NOT NULL,
  card_type VARCHAR(20) NOT NULL,
  order_status VARCHAR(20) NOT NULL CHECK (order_status IN ('new', 'processed', 'awaiting', 'shipped', 'cancelled')),
  PRIMARY KEY (student_email, date_created),
  FOREIGN KEY (student_email) REFERENCES student(email)
);

CREATE TABLE IF NOT EXISTS being_purchased
(
  student_email VARCHAR(30) NOT NULL,
  book_title VARCHAR(255) NOT NULL,
  quantity int,
  PRIMARY KEY (student_email, book_title),
  FOREIGN KEY (student_email) REFERENCES cart(student_email),
  FOREIGN KEY (book_title) REFERENCES book(title)
);

# had to add new table, books in cart are different from books in order
CREATE TABLE IF NOT EXISTS purchased
(
  student_email VARCHAR(30) NOT NULL,
  book_title VARCHAR(255) NOT NULL,
  quantity int,
  date_purchased DATE NOT NULL,
  PRIMARY KEY (student_email, book_title, date_purchased),
  FOREIGN KEY (student_email) REFERENCES orders(student_email),
  FOREIGN KEY (date_purchased) REFERENCES orders(date_created),
  FOREIGN KEY (book_title) REFERENCES book(title)
);

CREATE TABLE IF NOT EXISTS recommendation
(
  student_email VARCHAR(50) NOT NULL,
  book_title VARCHAR(255) NOT NULL,
  PRIMARY KEY (student_email),
  FOREIGN KEY (student_email) REFERENCES student(email),
  FOREIGN KEY (book_title) REFERENCES book(title)
);

CREATE TABLE IF NOT EXISTS course
(
  course_name VARCHAR(100) NOT NULL,
  course_year CHAR(4) NOT NULL,
  semester VARCHAR(6) NOT NULL,
  dept_name VARCHAR(100) NOT NULL,
  univ_name VARCHAR(20) NOT NULL,
  instr_email VARCHAR(30) NOT NULL,
  PRIMARY KEY (course_name, instr_email),
  FOREIGN KEY (dept_name) REFERENCES department(dept_name),
  FOREIGN KEY (univ_name) REFERENCES university(univ_name),
  FOREIGN KEY (instr_email) REFERENCES instructor(instr_email)
);

CREATE TABLE IF NOT EXISTS taking_course
(
  student_email VARCHAR(50) NOT NULL,
  course_name VARCHAR(100) NOT NULL,
  PRIMARY KEY (student_email),
  FOREIGN KEY (student_email) REFERENCES student(email),
  FOREIGN KEY (course_name) REFERENCES course(course_name)
);

CREATE TABLE IF NOT EXISTS books_used
(
  book_title VARCHAR(255) NOT NULL,
  course_name VARCHAR(100) NOT NULL,
  univ_name VARCHAR(20) NOT NULL,
  PRIMARY KEY (course_name, univ_name, book_title),
  FOREIGN KEY (book_title) REFERENCES book(title),
  FOREIGN KEY (course_name) REFERENCES course(course_name),
  FOREIGN KEY (univ_name) REFERENCES university(univ_name)
);

CREATE TABLE IF NOT EXISTS student_reviews
(
  rating FLOAT,
  book_title VARCHAR(50) NOT NULL,
  student_email VARCHAR(50) NOT NULL,
  PRIMARY KEY (book_title, student_email),
  FOREIGN KEY (book_title) REFERENCES book(title),
  FOREIGN KEY (student_email) REFERENCES student(email)
);