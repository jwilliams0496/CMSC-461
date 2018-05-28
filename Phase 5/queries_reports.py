import mysql.connector
from mysql.connector import errorcode
import datetime
from prettytable import PrettyTable

class Query:
    def getConnection(self):
        try:
            cnx = mysql.connector.connect(user = 'root', password = 'YOUR_PASSWORD_HERE', host = 'localhost', database = 'book_fetch')

    
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print "Something is wrong with your user name or password"

            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print "Database does not exist"

            else:
                print err

        return cnx

    def query1(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT * FROM student LEFT JOIN users ON (student.email = users.email) WHERE student.univ_name = 'UMBC';"
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Email', 'Birthdate', 'Major', 'Status', 'Year', 'University', 'First Name', 'Last Name', 'email', 'Address', 'Phone'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query2(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT * FROM student LEFT JOIN users ON (student.email = users.email) WHERE student.student_status = 'Grad';"
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Email', 'Birthdate', 'Major', 'Status', 'Year', 'University', 'First Name', 'Last Name', 'email', 'Address', 'Phone'])
            for row in result:
                resultTable.add_row(row)

            print resultTable
        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query3(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT *,\
	                    (\
                        SELECT SUM(purchased.quantity)\
                        FROM purchased\
                        WHERE purchased.student_email = student.email\
                        ) AS num_books_purchased\
                    FROM student JOIN users ON (student.email = users.email)\
                    WHERE student.major = 'Computer Science'\
                    HAVING num_books_purchased > 2;"
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Email', 'Birthdate', 'Major', 'Status', 'Year', 'University', 'First Name', 'Last Name', 'email', 'Address', 'Phone', 'Number of Books Purchased'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query4(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = 'SELECT book.title,\
	                    (\
                        SELECT SUM(purchased.quantity)\
                        FROM purchased\
                        WHERE purchased.book_title = book.title\
                        ) AS num_books_purchased\
                    FROM book\
                    HAVING num_books_purchased > 0\
                    ORDER BY num_books_purchased DESC;' 
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Book Title', 'Number Bought or Rented'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        # if it select categories, abort
        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query5(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = 'SELECT book.title,\
                    	(\
                        SELECT GROUP_CONCAT(category.category)\
                        from category\
                        WHERE category.book_title = book.title\
                        ) as all_categories\
                    FROM book;' 
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Book Title', 'Categories'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query6(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT books_used.book_title, books_used.course_name\
                    FROM books_used\
                    JOIN category ON (books_used.book_title = category.book_title)\
                    WHERE category.category != 'Computer Science';" 
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Course', 'Book Required'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query7(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = 'SELECT purchased.book_title\
                    FROM purchased\
                    WHERE purchased.student_email NOT IN\
	                    (\
                        SELECT taking_course.student_email\
                        FROM taking_course\
                        )\
                    AND\
	                    (\
	                    SELECT COUNT(purchased.book_title)\
	                    FROM purchased\
	                    JOIN keyword ON (purchased.book_title = keyword.book_title)\
	                    WHERE keyword.keyword IN\
		                    (\
		                    SELECT books_used.book_title\
		                    FROM books_used\
		                    JOIN keyword ON (books_used.book_title = keyword.book_title)\
		                    )\
	                    ) >= 2;' 
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Book Title'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query8(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = 'SELECT book.title,\
                    	(\
                        SELECT COUNT(books_used.book_title)\
                        FROM books_used\
                        WHERE book.title = books_used.book_title\
                        ) AS num_courses_used\
                    FROM book;' 
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Book Title', 'Number of Courses Associated with Book'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query9(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT book.title\
                    FROM book\
                    WHERE book.title IN\
	                    (\
	                    SELECT category.book_title\
	                    FROM category\
	                    JOIN keyword ON (category.book_title = keyword.book_title)\
	                    WHERE category.category = 'Linear Algebra'\
	                    OR keyword.keyword = 'Linear'\
	                    OR keyword.keyword = 'Algebra'\
                        )\
                    ;" 
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Books Related to \'Linear Algebra\''])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query10(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err

        try:
            cursor = connection.cursor()
            sql = "SELECT book.title\
                    FROM book\
                    WHERE book.rating > 3;" 
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Books with a rating higher than 3'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query11(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT book.title,\
	                    (\
                        SELECT COUNT(purchased.book_title)\
                        FROM purchased\
                        WHERE purchased.book_title = book.title\
                        ) AS num_purchased, book.rating\
                    FROM book\
                    ORDER BY book.rating DESC;"
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Book Title', 'Number Purchased', 'Rating'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query12(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT category.category AS cat,\
                    	(\
                        SELECT AVG(purchased.quantity)\
                        FROM purchased\
                        JOIN category ON (purchased.book_title = category.book_title)\
                        WHERE category.category = cat\
                        ) AS avg_purchased\
                    FROM category\
                    ORDER BY avg_purchased DESC;"
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Category', 'Average Number Purchased'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query13(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err

        try:
            cursor = connection.cursor()
            sql = "SELECT univ_name, dept_name,\
                    	(\
                        SELECT GROUP_CONCAT(course.course_name)\
                        FROM course\
                        WHERE course.dept_name = department.dept_name\
                        ) AS courses,\
                    	(\
                    	SELECT COUNT(instructor.instr_email)\
                        FROM instructor\
                        WHERE instructor.instr_email IN\
                    		(\
                            SELECT course.instr_email\
                            FROM course\
                            WHERE course.dept_name = department.dept_name\
                            )\
                            ) AS num_instr\
                    FROM department;" 
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['University', 'Departments', 'Courses', 'Number of Professors'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query14(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT university.univ_name,\
                    	(\
                        SELECT COUNT(purchased.quantity)\
                        FROM purchased\
                        JOIN books_used ON (purchased.book_title = books_used.book_title)\
                        WHERE purchased.book_title = books_used.book_title\
                        AND books_used.univ_name = university.univ_name\
                        ) AS num_purchased,\
                        (\
                        SELECT SUM(book.price)\
                        FROM book\
                        JOIN books_used ON (book.title = books_used.book_title)\
                        JOIN purchased ON (book.title = purchased.book_title)\
                        WHERE book.title = books_used.book_title\
                        AND books_used.univ_name = university.univ_name\
                        ) AS total_price\
                    FROM university;" 
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['University', 'Number of Books Purchased Associated with the University', 'Total Price of Books Purchased Associated with the University'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query15(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT users.first_name, users.last_name,\
                    	(\
                        SELECT COUNT(trouble_ticket.ticket_id)\
                        FROM trouble_ticket\
                        WHERE trouble_ticket.creator_name = users.first_name\
                        ) AS num_tickets_created\
                    FROM customer_support_user\
                    JOIN employee ON (customer_support_user.email = employee.email)\
                    JOIN users ON (customer_support_user.email = users.email);"
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Customer Support User\'s First Name', 'Customer Support User\'s Last Name', 'Number of Tickets Created'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query16(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err

        try:
            cursor = connection.cursor()
            sql = "SELECT users.first_name, users.last_name, employee.salary FROM administrator\
                    JOIN employee ON (administrator.email = employee.email)\
                    JOIN users ON (administrator.email = users.email)\
                    ORDER BY employee.salary DESC;"
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Administrator\'s First Name', 'Administrator\'s Last Name', 'Administrator\'s Salary'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query17(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT users.first_name, users.last_name,\
                    	(\
                        SELECT COUNT(trouble_ticket.ticket_id)\
                        FROM trouble_ticket\
                        WHERE trouble_ticket.administrator_name = users.first_name\
                        AND trouble_ticket.state = 'completed'\
                        ) AS num_tickets_completed\
                    FROM administrator\
                    JOIN employee ON (administrator.email = employee.email)\
                    JOIN users ON (administrator.email = users.email);" 
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Administrator\'s First Name', 'Administrator\'s Last Name', 'Number of Tickets Completed'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query18(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT DISTINCT trouble_ticket.state as ticket_state,\
                    	(\
                        SELECT COUNT(trouble_ticket.creator_type)\
                        FROM trouble_ticket\
                        WHERE trouble_ticket.creator_type = 'student'\
                        AND trouble_ticket.state = ticket_state\
                        ) AS num_student,\
                        (\
                        SELECT COUNT(trouble_ticket.creator_type)\
                        FROM trouble_ticket\
                        WHERE trouble_ticket.creator_type = 'customer_support_user'\
                        AND trouble_ticket.state = ticket_state\
                        ) AS num_customer_support_user\
                    FROM trouble_ticket;"
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Ticket State', 'Number of Tickets Creeated by a Student', 'Number of Tickets Created by a Customer Support User'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query19(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT AVG(B.date_logged - A.date_logged) AS avg_time\
                    FROM trouble_ticket AS A INNER JOIN trouble_ticket AS B ON (B.ticket_id = A.ticket_id)\
                    WHERE A.state = 'new' AND B.state = 'completed'\
                    ORDER BY A.ticket_id ASC;"
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Average Number of Days for a Ticket to go from \'new\' to \'completed\''])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query20(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT A.ticket_id AS ticket_id, D.title AS title, D.description AS description,\
                    D.creator_type AS creator_type, D.creator_name AS creator_name, D.date_logged AS date_created,\
                    C.customer_support_user_name AS customer_support_user, C.administrator_name AS administrator_assigned, C.date_logged AS date_assigned,\
                    B.date_logged AS date_inprocess,\
                    A.date_logged AS date_completed, A.solution AS solution\
                    FROM trouble_ticket AS A\
                    INNER JOIN trouble_ticket AS B ON (B.ticket_id = A.ticket_id)\
                    INNER JOIN trouble_ticket AS C ON (C.ticket_id = A.ticket_id)\
                    INNER JOIN trouble_ticket AS D ON (D.ticket_id = A.ticket_id)\
                    WHERE A.state = 'completed' AND B.state = 'in-process'\
                    AND C.state = 'assigned' AND D.state = 'new';" 
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Ticket ID', 'Title', 'Description', 'Creator Type', 'Creator Name', 'Date Created', 'Customer Support User Name', 'Administrator Name', 'Date Assigned', 'Date In-process', 'Date Completed', 'Solution'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query21(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            print "\n*** Note: this one definitely doesn't work. Just too difficult\n"
            cursor = connection.cursor()
            sql = "SELECT DISTINCT P.student_email, B.title AS recomendation\
                    FROM book as B\
                    JOIN purchased AS P ON (P.book_title = B.title)\
                    WHERE P.student_email IN\
	                    (\
                        SELECT purchased.student_email\
	                    FROM purchased\
                        WHERE purchased.student_email = P.student_email\
                        AND purchased.student_email IN\
		                    (\
                            SELECT (current_date() - purchased.date_purchased) AS time_difference\
		                    FROM purchased\
		                    WHERE purchased.student_email = P.student_email\
		                    HAVING time_difference < 30\
                            )\
                        )\
                    AND B.title NOT IN\
	                    (\
                        SELECT purchased.book_title\
                        FROM purchased\
                        )\
                    AND B.title IN\
	                    (\
                        SELECT DISTINCT category.book_title\
                        FROM category\
                        WHERE B.title = category.book_title\
                        )\
                    AND B.title IN\
	                    (\
	                    SELECT keyword.book_title\
                        FROM keyword\
                        WHERE B.title = keyword.book_title\
                        );"

            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Student Email', 'Recomended Book'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query22(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            print "\n*** Note: this one definitely doesn't work. Just too difficult\n"
            cursor = connection.cursor()
            sql = "SELECT book.title,\
                    	(\
                        SELECT COUNT(purchased.student_email)\
                        FROM purchased\
                        WHERE purchased.book_title IN\
                            (\
                            SELECT keyword.book_title\
                            FROM keyword JOIN purchased ON (purchased.book_title = keyword.book_title)\
                            )\
                        ) AS num_students\
                    FROM book;"
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Book Title', 'Students Who Purchased a Book with the Same Keyword but Not Including the Same Book'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query23(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err
        
        try:
            cursor = connection.cursor()
            sql = "SELECT book.title, book.rating,\
                        (\
                        SELECT COUNT(student_reviews.book_title)\
                        FROM student_reviews\
                        WHERE book.title = student_reviews.book_title\
                        ) AS num_students\
                    FROM book\
                    ORDER BY num_students DESC;" 
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Book Title', 'Rating', 'Number of Student Reviews'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()

    def query24(self):
        try:
            connection = self.getConnection()
            connection.autocommit = True
        except AttributeError as err:
            raise err

        try:
            cursor = connection.cursor()
            sql = "SELECT book.title, book.rating,\
                        (\
                        SELECT users.first_name FROM student\
                        LEFT JOIN users ON (student.email = users.email)\
                        LEFT JOIN student_reviews ON (student.email = student_reviews.student_email)\
                        WHERE student.email = users.email = student_reviews.student_email\
                        ) AS student_first_name,\
                        (\
                        SELECT users.last_name FROM student\
                        LEFT JOIN users ON (student.email = users.email)\
                        LEFT JOIN student_reviews ON (student.email = student_reviews.student_email)\
                        WHERE student.email = users.email = student_reviews.student_email\
                        ) AS student_last_name,\
                        (\
                        SELECT student.univ_name FROM student\
                        LEFT JOIN users ON (student.email = users.email)\
                        LEFT JOIN student_reviews ON (student.email = student_reviews.student_email)\
                        WHERE student.email = users.email = student_reviews.student_email\
                        ) AS student_univ_name\
                    FROM book\
                    WHERE book.rating = 5.0;" 
            cursor.execute(sql)
            result = cursor.fetchall()

            resultTable = PrettyTable(['Book Title', 'Rating', 'Student First Name', 'Student Last Name', 'Student University'])
            for row in result:
                resultTable.add_row(row)

            print resultTable

        except mysql.connector.Error as err:
            print err
            connection.close()

        except Exception as err:
            print err
            connection.rollback()
            connection.close()

        finally:
            connection.close()


def main():
    query = Query()
    userOption = ''
    while True:
        userOption = raw_input("Enter a number between 1 and 24 (or 'exit'): ")

        # exit
        if userOption == 'exit':
            break

        # invalid input
        try:
            if int(userOption) not in range(1, 25):
                print "That's not a number between 1 and 24"
                continue

        except Exception:
            print "That's not a number between 1 and 24"
            continue

        # valid input
        funcName = "query" + userOption
        getattr(query, funcName)()

main()