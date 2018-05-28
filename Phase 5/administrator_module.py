########################################################################################
# File: administrator_module.py
# Author: James Williams
# Description: Provides the command line interface for the administrators of Book Fetch
# Inc. to use when preforming actions and use cases associated with them
########################################################################################

import mysql.connector
from mysql.connector import errorcode
import datetime

# Global values
EMPLOYEE_EMAIL = None
EMPLOYEE_FIRST_NAME = None
EMPLOYEE_LAST_NAME = None
IS_SUPER = None

def getConnection():
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

def printHelp():
    # todo: print more options as they become available
    print "Options:"
    print "\t\'exit\': Exits the program"
    print "\t\'status\': Prints current user information"
    print "\t\'ticket\': Submit a Trouble Ticket to the Book Fetch Employees"
    print "\t\'tickets\': View and edit tickets (new only) submitted to the Book Fetch system"
    print "\t\'new book\': Add a new book to the Book Fetch system"
    print "\t\'new university\': Add a new university"
    print "\t\'new department\': Add a new department"
    print "\t\'new course\': Add a new course"
    print "\t\'new book req\': Add a new book requirement to a course"
    print "\t\'new customer suppport user\': Create a new customer support user (SUPER ADMINS ONLY)"
    print "\t\'new administrator\': Create a new administrator (SUPER ADMINS ONLY)"
    print "\t\'remove employee\': Remove an employee (SUPER ADMINS ONLY)"

def signIn():
    global EMPLOYEE_EMAIL, EMPLOYEE_FIRST_NAME, EMPLOYEE_LAST_NAME, IS_SUPER

    # Ask user for their email
    employeeEmail = raw_input("Please enter your email: ")

    # Get connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except Exception as err:
        print err

    # Verify email is in the database
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM administrator\
                LEFT JOIN employee ON (administrator.email = employee.email)\
                WHERE administrator.email = \'' + employeeEmail + '\';'
        cursor.execute(sql)
        result = cursor.fetchone()

        # email wasn't found, print error
        if result == None:
            print "\nThe email \'" + employeeEmail + "\' is not registered to the Book Fetch system!"
            return False

        # email was found, print greeting, set globals
        else:
            IS_SUPER = result[0]

            sql = 'SELECT first_name FROM users WHERE users.email = \'' + employeeEmail + '\';'
            cursor.execute(sql)
            result = cursor.fetchone()
            EMPLOYEE_FIRST_NAME = result[0]

            sql = 'SELECT last_name FROM users WHERE users.email = \'' + employeeEmail + '\';'
            cursor.execute(sql)
            result = cursor.fetchone()           
            EMPLOYEE_LAST_NAME = result[0]

            sql = 'SELECT email FROM users WHERE users.email = \'' + employeeEmail + '\';'
            cursor.execute(sql)
            result = cursor.fetchone()           
            EMPLOYEE_EMAIL = result[0]

            print "Welcome back " + EMPLOYEE_FIRST_NAME + '!'
            return True

    except Exception as err:
        print err

    finally:
        connection.close()

def signedIn():
    global EMPLOYEE_EMAIL
    return EMPLOYEE_EMAIL != None

def status():
    global EMPLOYEE_EMAIL, EMPLOYEE_FIRST_NAME, EMPLOYEE_LAST_NAME
    print "\nUser Information:"
    print "Name: " + EMPLOYEE_FIRST_NAME + " " + EMPLOYEE_LAST_NAME
    print "Email: " + EMPLOYEE_EMAIL
    print "Super: " + str(IS_SUPER)

def greetUser():
    print "\nWelcome to the Book Fetch Inc Administrator Module"

    signIn()

    # user really does have an account
    if signedIn():
        return True

    # user's email is wrong
    else:
        print "You MUST be an employee of Book Fetch Inc to use this module"
        print "Check with an Administrator to make sure your registered\n"
        print "The program will now terminate"
        return False

def editTicket():
    now = datetime.datetime.now()
    date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)

    print "Here are all the tickets that have been assigned to you:"

    # show all tickets with the given category in the touble_ticket table

    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except AttributeError as err:
        raise err
        
    # Once connected try to get all the tickets
    try:
        cursor = connection.cursor()

        # get all tickets assigned
        sql = 'SELECT * FROM trouble_ticket WHERE administrator_name = \'' + EMPLOYEE_FIRST_NAME + '\';'
        cursor.execute(sql)
        assign = cursor.fetchall()

        # get all tickets assigned and completed
        sql = 'SELECT * FROM trouble_ticket WHERE administrator_name = \'' + EMPLOYEE_FIRST_NAME + '\' AND state = \'completed\';'
        cursor.execute(sql)
        complete = cursor.fetchall()

        # only add tickets that haven't been assigned yet
        new = []
        for newRow in assign:
            completed = False
            for completeRow in complete:
                if newRow[0] == completeRow[0]:
                    completed = True
                    break
            
            if completed == False:
                new.append(newRow)

        # removed assigned tickets if they are already in process
        temp = new
        for row in new:
            for tempRow in temp:
                if row[0] == tempRow[0]:
                    if row[1] == 'assigned' and tempRow[1] == 'in-process':
                        new.remove(row)

        # If there are now tickets in this category return
        if (len(new) == 0):
            print "\nHoray! You have no tickets assigned to you!"
            return

        for row in new:
            print "\n######################################################\n"
            print "Ticket ID: " + row[0]
            print "Title: " + row[4]
            print "Creator: A " + row[7] + " named " + row[6]
            print "Date Logged: " + str(row[3])
            print "State: " + row[1] + "\n"

            if row[5] != None:
                print "Description: " + row[5]

            if row[8] != None:
                print "\nThis ticket has been marked by " + row[8]
            else:
                print "\nThis ticket has not been marked yet"

            if row[9] != None:
                print 'This ticket has been assigned to: ' + row[9]
            else:
                print 'This ticket has not been assigned yet'
            
            if row[10] != None:
                print "Solution: " + row[10]

        ticket = raw_input("Enter the Ticket ID of the ticket you wish to edit (or 'exit'): ")

        if (ticket == 'exit'):
            print "Returning to the main menu"
            return

        # make sure the ticket that the user has entered is one of the new tickets shown
        exists = False
        for row in new:
            if ticket == row[0]:
                exists = True
                ticket_tuple = row
                break

        if exists == False:
            print "\nError: ticket " + ticket + " not assigned to you"
            return

        state = raw_input("What is the state of this ticket? ('in-process' or 'completed'... or 'exit': ")

        if state == 'exit':
            print "Returning to the main menu"
            return

        solution = ''
        if state == 'completed':
            giveSolution = ''
            while True:
                giveSolution = raw_input("Would you like to give a description of the solution to the ticket ('y' or 'n'): ")
                if giveSolution == 'y':
                    solution = raw_input("Provide a short description of the solution: ")
                    
                    # get existing ticket info here, and create a new ticket
                    sql = 'INSERT INTO trouble_ticket(ticket_id, state, category, date_logged, title, description,\
			            	creator_name, creator_type, customer_support_user_name, administrator_name, solution)\
                            VALUES (\'' + ticket + '\', \'' + state + '\', \'' + ticket_tuple[2] + '\', \'' + date + '\', \'' + ticket_tuple[4] + '\', \'' + ticket_tuple[5]\
                            + '\', \'' + ticket_tuple[6] + '\', \'' + ticket_tuple[7] + '\', \'' + ticket_tuple[8] + '\', \'' + EMPLOYEE_FIRST_NAME + '\', \'' + solution + '\');'

                    cursor.execute(sql)

                    print "Ticket " + ticket + " has been completed!"
                    return
                
                if giveSolution == 'n':
                    # get existing ticket info here, and create a new ticket
                    sql = 'INSERT INTO trouble_ticket(ticket_id, state, category, date_logged, title, description,\
			            	creator_name, creator_type, customer_support_user_name, administrator_name, solution)\
                            VALUES (\'' + ticket + '\', \'' + state + '\', \'' + ticket_tuple[2] + '\', \'' + date + '\', \'' + ticket_tuple[4] + '\', \'' + ticket_tuple[5]\
                            + '\', \'' + ticket_tuple[6] + '\', \'' + ticket_tuple[7] + '\', \'' + ticket_tuple[8] + '\', \'' + EMPLOYEE_FIRST_NAME + '\', null);'
                            
                    cursor.execute(sql)

                    print "Ticket " + ticket + " has been completed!"
                    return

        # get existing ticket info here, and create a new ticket
        sql = 'INSERT INTO trouble_ticket(ticket_id, state, category, date_logged, title, description,\
	    creator_name, creator_type, customer_support_user_name, administrator_name, solution)\
        VALUES (\'' + ticket + '\', \'' + state + '\', \'' + ticket_tuple[2] + '\', \'' + date + '\', \'' + ticket_tuple[4] + '\', \'' + ticket_tuple[5]\
        + '\', \'' + ticket_tuple[6] + '\', \'' + ticket_tuple[7] + '\', \'' + ticket_tuple[8] + '\', \'' + EMPLOYEE_FIRST_NAME + '\', null);'        

        cursor.execute(sql)
            
        print "Ticket " + ticket + " has been updated"
        print "Returning to main menu"

    except mysql.connector.Error as err:
        print err
        connection.close()
        return False

    # if it cant insert, abort
    except Exception as err:
        print err
        connection.rollback()
        connection.close()
        return False

    finally:
        connection.close()    

    return True

def createBook():
    while True:
        print "\nSupply the following information"
        print "Enter 'restart' to start over or type 'exit' to quit book creation\n"

        title = raw_input("\nWhat is the title of the book?: ")
        if title == 'exit':
            return False
        if title == 'restart':
            continue

        isbn = raw_input("\nWhat is the ISBN of the book?: ")
        if isbn == 'exit':
            return False
        if isbn == 'restart':
            continue

        isbn13 = raw_input("\nWhat is the ISBN13 of the book?: ")
        if isbn13 == 'exit':
            return False
        if isbn13 == 'restart':
            continue

        bookType = raw_input("\nIs the book 'new' or 'used'?: ")
        if bookType == 'exit':
            return False
        if bookType == 'restart':
            continue

        purchaseType = raw_input("\nIs the book 'buy' or 'rent'?: ")
        if isbn == 'exit':
            return False
        if isbn == 'restart':
            continue

        price = raw_input("\nWhat is the price of the book?: ")
        if price == 'exit':
            return False
        if price == 'restart':
            continue

        quantity = raw_input("\nWhat is the quantity of the book?: ")
        if quantity == 'exit':
            return False
        if quantity == 'restart':
            continue

        publisher = raw_input("\nWhat is the publisher of the book?: ")
        if publisher == 'exit':
            return False
        if publisher == 'restart':
            continue

        publishDate = raw_input("\nWhat is the publish date of the book?: ")
        if publishDate == 'exit':
            return False
        if publishDate == 'restart':
            continue

        edition = raw_input("\nWhat is the edition number of the book?: ")
        if edition == 'exit':
            return False
        if edition == 'restart':
            continue

        lang = raw_input("\nWhat language is the book?: ")
        if lang == 'exit':
            return False
        if lang == 'restart':
            continue

        bookFormat = raw_input("\nIs the book 'hardcover', 'paperback', or 'electronic'?: ")
        if bookFormat == 'exit':
            return False
        if bookFormat == 'restart':
            continue

        weight = raw_input("\nHow much does the book weigh?: ")
        if weight == 'exit':
            return False
        if weight == 'restart':
            continue

        rating = raw_input("\nWhat is the book's rating?: ")
        if rating == 'exit':
            return False
        if rating == 'restart':
            continue

        print "\n***Please verify the following information***"
        print "Title: " + title
        print "ISBN: " + isbn
        print "ISBN13: " + isbn13
        print "Type: " + bookType
        print "Price: " + price
        print "Quantity: " + quantity
        print "Publisher: " + publisher
        print "Edition Number: " + edition
        print "Language: " + lang
        print "Format: " + bookFormat
        print "Weight: " + weight
        print "Rating: " + rating

        verify = ''

        while True:
            verify = raw_input("\nIs this information correct? ('y' or 'n'): ")
            if verify == 'n':
                return False
            if verify == 'y':
                break

        break
    
    print "\nNow supply the following information"
    print "Enter 'restart' to start over or type 'exit' to quit book creation\n"

    authors = []
    while True:
        author = raw_input("\nEnter all authors (Enter 'done' when finished): ")
        if author == 'exit':
            return False
        if author == 'restart':
            continue
        if author == 'done':
            break
        else:
            authors.append(author)
        
    categories = []
    while True:
        category = raw_input("\nEnter all categories (Enter 'done' when finished): ")
        if category == 'exit':
            return False
        if category == 'restart':
            continue
        if category == 'done':
            break
        else:
            categories.append(category)

    keywords = []
    while True:
        keyword = raw_input("\nEnter all keywords (Enter 'done' when finished): ")
        if keyword == 'exit':
            return False
        if keyword == 'restart':
            continue
        if keyword == 'done':
            break
        else:
            keywords.append(keyword)

    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = False
    except AttributeError as err:
        raise err

    # Once connected try to insert new book
    try:
        cursor = connection.cursor()

        # insert new book
        sql = 'INSERT INTO book(isbn, isbn13, book_type, purchase_type, price, quantity, title, publisher,\
                publish_date, edition_number, book_lang, book_format, weight, rating)\
                VALUES (\'' + isbn + '\', \'' + isbn13 + '\', \'' + bookType + '\', \'' + purchaseType + '\', \''\
                + price + '\', \'' + quantity + '\', \'' + title + '\', \'' + publisher + '\', \'' + publishDate\
                + '\', ' + edition + ', \'' + lang + '\', \'' + bookFormat + '\', \''\
                + weight + '\', \'' + rating + '\');'

        cursor.execute(sql)

        # insert all the authors in table authors
        for author in authors:
            sql = 'INSERT INTO authors(author, book_title) VALUES (\'' + author + '\', \'' + title + '\');'
            cursor.execute(sql)

        # insert all the categories in table categories
        for category in categories:
            sql = 'INSERT INTO category(book_title, category) VALUES (\'' + title + '\', \'' + category + '\');'
            cursor.execute(sql)

        # insert all the keywords in table keywords
        for keyword in keywords:
            sql = 'INSERT INTO keyword(book_title, keyword) VALUES (\'' + title + '\', \'' + keyword + '\');'
            cursor.execute(sql)

        connection.commit()

        print "\n" + title + " has been added to the book table."

    except mysql.connector.Error as err:
        print err
        connection.close()
        return False

    # if it cant insert, abort
    except Exception as err:
        print err
        connection.rollback()
        connection.close()
        return False

    finally:
        connection.close()    

    return True  

def createUniversity():
    while True:
        print "\nSupply the following information"
        print "Enter 'restart' to start over or type 'exit' to quit book creation\n"

        univName = raw_input("\nWhat is the name of the University?: ")
        if univName == 'exit':
            return False
        if univName == 'restart':
            continue

        address = raw_input("\nWhat is the address of the University?: ")
        if address == 'exit':
            return False
        if address == 'restart':
            continue

        print "\n***Please verify the following information***"
        print "University Name: " + univName
        print "University Address: " + address

        verify = ''

        while True:
            verify = raw_input("\nIs this information correct? ('y' or 'n'): ")
            if verify == 'n':
                return False
            if verify == 'y':
                break

        break

    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except AttributeError as err:
        raise err

    # Once connected try to insert new 
    try:
        cursor = connection.cursor()

        # insert new university
        sql = 'INSERT INTO university(univ_name, address)\
                VALUES (\'' + univName + '\', \'' + address + '\' );'

        cursor.execute(sql)

        print "\n" + univName + " has been added to the university table"

    except mysql.connector.Error as err:
        print err
        connection.close()
        return False

    # if it cant insert, abort
    except Exception as err:
        print err
        connection.rollback()
        connection.close()
        return False

    finally:
        connection.close()    

    return True  

def createDepartment():
    while True:
        print "\nSupply the following information"
        print "Enter 'restart' to start over or type 'exit' to quit book creation\n"

        univName = raw_input("\nWhat is the name of the University?: ")
        if univName == 'exit':
            return False
        if univName == 'restart':
            continue

        department = raw_input("\nWhat is the name of the department?: ")
        if department == 'exit':
            return False
        if department == 'restart':
            continue

        print "\n***Please verify the following information***"
        print "University Name: " + univName
        print "Department: " + department

        verify = ''

        while True:
            verify = raw_input("\nIs this information correct? ('y' or 'n'): ")
            if verify == 'n':
                return False
            if verify == 'y':
                break

        break

    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except AttributeError as err:
        raise err

    # Once connected try to insert new 
    try:
        cursor = connection.cursor()

        # insert new university
        sql = 'INSERT INTO department(univ_name, dept_name)\
                VALUES (\'' + univName + '\', \'' + department + '\' );'

        cursor.execute(sql)

        print "\n" + department + " has been added to " + univName

    except mysql.connector.Error as err:
        print err
        connection.close()
        return False

    # if it cant insert, abort
    except Exception as err:
        print err
        connection.rollback()
        connection.close()
        return False

    finally:
        connection.close()    

    return True

def createInstructor():
    while True:
        print "\nSupply the following information"
        print "Enter 'restart' to start over or type 'exit' to quit book creation\n"

        univName = raw_input("\nWhat is the name of the University?: ")
        if univName == 'exit':
            return False
        if univName == 'restart':
            continue

        firstName = raw_input("\nWhat is the first name of the instructor?: ")
        if firstName == 'exit':
            return False
        if firstName == 'restart':
            continue

        lastName = raw_input("\nWhat is the last name of the instructor?: ")
        if lastName == 'exit':
            return False
        if lastName == 'restart':
            continue

        email = raw_input("\nWhat is the instructor's email?: ")
        if email == 'exit':
            return False
        if email == 'restart':
            continue

        department = raw_input("\nWhat department does the instructor belong to?: ")
        if department == 'exit':
            return False
        if department == 'restart':
            continue

        print "\n***Please verify the following information***"
        print "University Name: " + univName
        print "Instructor's Name: " + firstName + " " + lastName
        print "Instructor's Email: " + email
        print "Department: " + department

        verify = ''

        while True:
            verify = raw_input("\nIs this information correct? ('y' or 'n'): ")
            if verify == 'n':
                return False
            if verify == 'y':
                break

        break

    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except AttributeError as err:
        raise err

    # Once connected try to insert new 
    try:
        cursor = connection.cursor()

        # insert new university
        sql = 'INSERT INTO instructor(instr_email, first_name, last_name, dept_name, univ_name)\
                VALUES (\'' + email + '\', \'' + firstName + '\', \'' + lastName + '\', \'' + department + '\', \'' + univName + '\');'

        cursor.execute(sql)

        print "\n" + firstName + ' ' + lastName + " has been added to " + univName

    except mysql.connector.Error as err:
        print err
        connection.close()
        return False

    # if it cant insert, abort
    except Exception as err:
        print err
        connection.rollback()
        connection.close()
        return False

    finally:
        connection.close()    

    return True

def createCourse():
    while True:
        print "\nSupply the following information"
        print "Enter 'restart' to start over or type 'exit' to quit book creation\n"

        univName = raw_input("\nWhat is the name of the University?: ")
        if univName == 'exit':
            return False
        if univName == 'restart':
            continue

        email = raw_input("\nWhat is the email of the instructor?: ")
        if email == 'exit':
            return False
        if email == 'restart':
            continue

        department = raw_input("\nWhat is the name of the department?: ")
        if department == 'exit':
            return False
        if department == 'restart':
            continue

        courseName = raw_input("\nWhat is the name of the course?: ")
        if courseName == 'exit':
            return False
        if courseName == 'restart':
            continue

        year = raw_input("\nWhat year was this course taught?: ")
        if year == 'exit':
            return False
        if year == 'restart':
            continue

        semester = raw_input("\nWhat semester was this course taught?: ")
        if department == 'exit':
            return False
        if department == 'restart':
            continue

        print "\n***Please verify the following information***"
        print "University Name: " + univName
        print "Instructor Email: " + email
        print "Department: " + department
        print "Course Name: " + courseName
        print "Course Year: " + year
        print "Course Semester: " + semester

        verify = ''

        while True:
            verify = raw_input("\nIs this information correct? ('y' or 'n'): ")
            if verify == 'n':
                return False
            if verify == 'y':
                break

        break

    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except AttributeError as err:
        raise err

    # Once connected try to insert new 
    try:
        cursor = connection.cursor()

        # insert new university
        sql = 'INSERT INTO course(course_name, course_year, semester, dept_name, univ_name, instr_email)\
                VALUES (\'' + courseName + '\', \'' + year + '\', \'' + semester + '\', \'' + department + '\', \'' + univName + '\', \'' + email + '\');'

        cursor.execute(sql)

        print "\n" + courseName + " has been added to " + univName

    except mysql.connector.Error as err:
        print err
        connection.close()
        return False

    # if it cant insert, abort
    except Exception as err:
        print err
        connection.rollback()
        connection.close()
        return False

    finally:
        connection.close()    

    return True

def createBookAssoc():
    while True:
        print "\nSupply the following information"
        print "Enter 'restart' to start over or type 'exit' to quit book creation\n"

        univName = raw_input("\nWhat is the name of the University?: ")
        if univName == 'exit':
            return False
        if univName == 'restart':
            continue

        courseName = raw_input("\nWhat is the name of the course?: ")
        if courseName == 'exit':
            return False
        if courseName == 'restart':
            continue

        title = raw_input("\nWhat is the name of the book used?: ")
        if title == 'exit':
            return False
        if title == 'restart':
            continue

        print "\n***Please verify the following information***"
        print "University Name: " + univName
        print "Course Name: " + courseName
        print "Book Name: " + title

        verify = ''

        while True:
            verify = raw_input("\nIs this information correct? ('y' or 'n'): ")
            if verify == 'n':
                return False
            if verify == 'y':
                break

        break

    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except AttributeError as err:
        raise err

    # Once connected try to insert new 
    try:
        cursor = connection.cursor()

        # insert new university
        sql = 'INSERT INTO books_used(book_title, course_name, univ_name)\
                VALUES (\'' + title + '\', \'' + courseName + '\', \'' + univName + '\');'

        cursor.execute(sql)

        print "\n" + title + " has been added as a required book to " + courseName + " at " + univName

    except mysql.connector.Error as err:
        print err
        connection.close()
        return False

    # if it cant insert, abort
    except Exception as err:
        print err
        connection.rollback()
        connection.close()
        return False

    finally:
        connection.close()    

    return True

def createCustomerSupportUser():
    if IS_SUPER == 0:
        print "YOU MUST BE THE SUPER ADMINISTRATOR TO PERFORM THIS ACTION"
        return
    
    while True:
        print "\nSupply the following information"
        print "Enter 'restart' to start over or type 'exit' to quit customer support user creation\n"

        firstName = raw_input("\nWhat is the customer support user's first name?: ")
        if firstName == 'exit':
            return False
        if firstName == 'restart':
            continue

        lastName = raw_input("\nWhat is the customer support user's last name?: ")
        if lastName == 'exit':
            return False
        if lastName == 'restart':
            continue

        email = raw_input("\nWhat is the customer support user's email address?: ")
        if email == 'exit':
            return False
        if email == 'restart':
            continue
    
        address = raw_input("\nWhat is the customer support user's street address?: ")
        if address == 'exit':
            return False
        if address == 'restart':
            continue

        phone = raw_input("\nWhat is the customer support user's phone number?: ")
        if phone == 'exit':
            return False
        if phone == 'restart':
            continue

        gender = raw_input("\nWhat is the customer support user's gender? ('male' or 'female'): ")
        if gender == 'exit':
            return False
        if gender == 'restart':
            continue

        salary = raw_input("\nWhat is the customer support user's salary?: ")
        if salary == 'exit':
            return False
        if salary == 'restart':
            continue

        ssn = raw_input("\nWhat is the customer support user's Social Security Number?: ")
        if ssn == 'exit':
            return False
        if ssn == 'restart':
            continue

        print "\n***Please verify the following information***"
        print "First Name: ", firstName
        print "Last Name: ", lastName
        print "Email: ", email
        print "Street Address: ", address
        print "Phone Number: ", phone
        print "Gender: ", gender
        print "Salary: ", salary
        print "Social Security Number: ", ssn

        verify = ''

        while True:
            verify = raw_input("\nIs this information correct? ('y' or 'n'): ")
            if verify == 'n':
                return False
            if verify == 'y':
                break

        break

    # Now insert all this information into the bookfetch db

    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = False
    except AttributeError as err:
        raise err
        

    # Once connected try to insert
    try:
        cursor = connection.cursor()

        sql = 'INSERT INTO users (first_name, last_name, email, address, phone)\
                VALUES (\'' + firstName + '\', \'' + lastName + '\', \'' + email + '\', \'' + address + '\', \'' + phone + '\');'

        cursor.execute(sql)

        sql = 'INSERT INTO employee(email, gender, salary, ssn)\
        VALUES (\'' + email + '\', \'' + gender + '\', ' + salary + ', \'' + ssn + '\');'

        cursor.execute(sql)

        sql = 'INSERT INTO customer_support_user(email) VALUES (\'' + email + '\');'

        cursor.execute(sql)

        connection.commit()

        print "\nThe customer support user " + firstName + " " + lastName + " has been created!\n"

    except mysql.connector.Error as err:
        print err
        connection.close()
        return False

    # if it cant insert, abort
    except Exception as err:
        print err
        connection.rollback()
        connection.close()
        return False

    finally:
        connection.close()    

    return True

def createAdministrator():
    if IS_SUPER == 0:
        print "YOU MUST BE THE SUPER ADMINISTRATOR TO PERFORM THIS ACTION"
        return

    while True:
        print "\nSupply the following information"
        print "Enter 'restart' to start over or type 'exit' to quit Administrator creation\n"

        firstName = raw_input("\nWhat is the Administrator's first name?: ")
        if firstName == 'exit':
            return False
        if firstName == 'restart':
            continue

        lastName = raw_input("\nWhat is the Administrator's last name?: ")
        if lastName == 'exit':
            return False
        if lastName == 'restart':
            continue

        email = raw_input("\nWhat is the Administrator's email address?: ")
        if email == 'exit':
            return False
        if email == 'restart':
            continue
    
        address = raw_input("\nWhat is the Administrator's street address?: ")
        if address == 'exit':
            return False
        if address == 'restart':
            continue

        phone = raw_input("\nWhat is the Administrator's phone number?: ")
        if phone == 'exit':
            return False
        if phone == 'restart':
            continue

        gender = raw_input("\nWhat is the Administrator's gender? ('male' or 'female'): ")
        if gender == 'exit':
            return False
        if gender == 'restart':
            continue

        salary = raw_input("\nWhat is the Administrator's salary?: ")
        if salary == 'exit':
            return False
        if salary == 'restart':
            continue

        ssn = raw_input("\nWhat is the Administrator's Social Security Number?: ")
        if ssn == 'exit':
            return False
        if ssn == 'restart':
            continue

        isSuper = raw_input("\nIs this a Super Administrator? ('0' or '1'): ")
        if isSuper == 'exit':
            return False
        if isSuper == 'restart':
            continue

        print "\n***Please verify the following information***"
        print "First Name: ", firstName
        print "Last Name: ", lastName
        print "Email: ", email
        print "Street Address: ", address
        print "Phone Number: ", phone
        print "Gender: ", gender
        print "Salary: ", salary
        print "Social Security Number: ", ssn
        print "Super Administrator: ", isSuper 

        verify = ''

        while True:
            verify = raw_input("\nIs this information correct? ('y' or 'n'): ")
            if verify == 'n':
                return False
            if verify == 'y':
                break

        break

    # Now insert all this information into the bookfetch db

    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = False
    except AttributeError as err:
        raise err
        

    # Once connected try to insert
    try:
        cursor = connection.cursor()

        sql = 'INSERT INTO users (first_name, last_name, email, address, phone)' +\
                'VALUES (\'' + firstName + '\', \'' + lastName + '\', \'' + email + '\', \'' + address + '\', \'' + phone + '\');'

        cursor.execute(sql)

        sql = 'INSERT INTO employee(email, gender, salary, ssn)\
        VALUES (\'' + email + '\', \'' + gender + '\', ' + salary + ', \'' + ssn + '\');'

        cursor.execute(sql)

        sql = 'INSERT INTO administrator(is_super, email) VALUES (\'' + isSuper + '\', \'' + email + '\');'

        cursor.execute(sql)

        connection.commit()

        print "\nThe Administrator " + firstName + " " + lastName + " has been created!\n"

    except mysql.connector.Error as err:
        print err
        connection.close()
        return False

    # if it cant insert, abort
    except Exception as err:
        print err
        connection.rollback()
        connection.close()
        return False

    finally:
        connection.close()    

    return True

def deleteEmployee():
    if IS_SUPER == 0:
        print "YOU MUST BE THE SUPER ADMINISTRATOR TO PERFORM THIS ACTION"
        return

    while True:
        print "\nSupply the following information"
        print "Enter 'restart' to start over or type 'exit' to quit Administrator creation\n"

        employeeType = ''
        while True:
            employeeType = raw_input("\nEnter '1' to delete a Customer Support User or Enter '2' to remove an Administrator: ")
            if employeeType in ['exit', 'restart', '1', '2']:
                break

        if employeeType == 'exit':
            return False
        if employeeType == 'restart':
            continue

        email = raw_input("\nWhat is the employee's email address?: ")
        if email == 'exit':
            return False
        if email == 'restart':
            continue

        if email == EMPLOYEE_EMAIL and employeeType == '2':
            print "\nYou cannot delete yourself\n"
            print "There must always be at least ONE Super Administrator registered to the Book Fetch system."
            print "To enforce this rule, a Super Administrator can only be deleted by another Super Administrator."
            print "(Hint: new Super Administrators can be created using \'new administrator\'\n"
            return

        break

    # Now insert all this information into the bookfetch db

    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = False
    except AttributeError as err:
        raise err
        

    # Once connected try to insert
    try:
        cursor = connection.cursor()

        # delete customer support user
        if (employeeType == '1'):
            sql = 'SELECT * FROM customer_support_user JOIN employee ON (customer_support_user.email = employee.email)\
            JOIN users ON (customer_support_user.email = users.email) WHERE customer_support_user.email = \'' + email + '\';' 
            cursor.execute(sql)
            result = cursor.fetchone()

            if result == None:
                print "\nThe customer support user with the email", email, "was not found in the book fetch system\n"
                return False

            print "\n***The following customer support user will be deleted***"
            print "Employee Name: ", result[5] + " " + result[6]
            print "Email: ", email

            verify = ''

            while True:
                verify = raw_input("\nIs this information correct? ('y' or 'n'): ")
                if verify == 'n':
                    return False
                if verify == 'y':
                    break
            
            firstName = result[5]

            sql = 'DELETE FROM customer_support_user WHERE email = \'' + email + '\';'
            cursor.execute(sql)
            sql = 'DELETE FROM employee WHERE email = \'' + email + '\';'
            cursor.execute(sql)
            sql = 'DELETE FROM users WHERE email = \'' + email + '\';'
            cursor.execute(sql)

            # remove any trouble tickets that were associated to them, only ticket left should be new ticket
            sql = 'DELETE FROM trouble_ticket where customer_support_user_name = \'' + firstName + '\';'
            cursor.execute(sql)

        if (employeeType == '2'):
            sql = 'SELECT * FROM administrator JOIN employee ON (administrator.email = employee.email)\
                    JOIN users ON (administrator.email = users.email) WHERE administrator.email = \'' + email + '\';' 
            cursor.execute(sql)
            result = cursor.fetchone()

            if result == None:
                print "\nThe Administrator with the email", email, "was not found in the book fetch system\n"
                return False

            print "\n***The following Administrator will be deleted***"
            print "Employee Name: ", result[6] + " " + result[7]
            print "Email: ", email

            verify = ''

            while True:
                verify = raw_input("\nIs this information correct? ('y' or 'n'): ")
                if verify == 'n':
                    return False
                if verify == 'y':
                    break
            
            firstName = result[6]

            sql = 'DELETE FROM administrator WHERE email = \'' + email + '\';'
            cursor.execute(sql)
            sql = 'DELETE FROM employee WHERE email = \'' + email + '\';'
            cursor.execute(sql)
            sql = 'DELETE FROM users WHERE email = \'' + email + '\';'
            cursor.execute(sql)

            # remove any trouble tickets that were associated to them, only ticket left should be new ticket
            sql = 'DELETE FROM trouble_ticket where administrator_name = \'' + firstName + '\';'
            cursor.execute(sql)

        connection.commit()

        print firstName + ' was deleted from the Book Fetch System'

    except mysql.connector.Error as err:
        print err
        connection.close()
        return False

    # if it cant insert, abort
    except Exception as err:
        print err
        connection.rollback()
        connection.close()
        return False

    finally:
        connection.close()    

    return True

def main():
    hasAccount = greetUser()

    if hasAccount == False:
        return

    userOption = ''

    print '\nUse \'help\' to get started, or \'exit\' to quit to program'
    # todo: print options to the user

    while True:
        if signedIn() == False:
            break

        userOption = raw_input('-> ')

        if userOption == 'exit':
            print "Goodbye!"
            break

        # Option checks start here

        if userOption == '':
            continue

        if userOption == 'status':
            status()
            continue

        if userOption == 'help':
            printHelp()
            continue

        if userOption == 'tickets':
            editTicket()
            continue

        if userOption == 'new book':
            createBook()
            continue

        if userOption == 'new university':
            createUniversity()
            continue

        if userOption == 'new department':
            createDepartment()
            continue

        if userOption == 'new instructor':
            createInstructor()
            continue

        if userOption == 'new course':
            createCourse()
            continue

        if userOption == 'new book req':
            createBookAssoc()
            continue

        if userOption == 'new customer support user':
            createCustomerSupportUser()
            continue

        if userOption == 'new administrator':
            createAdministrator()
            continue

        if userOption == 'remove employee':
            deleteEmployee()
            continue
        
        # todo: more options here

        else:
            print 'Unknown command: \'' + userOption + '\''

main()