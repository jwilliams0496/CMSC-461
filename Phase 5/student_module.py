########################################################################################
# File: student_module.py
# Author: James Williams
# Description: Provides the command line interface for the student users of Book Fetch
# Inc. to use when preforming actions and use cases associated with them
########################################################################################

import mysql.connector
from mysql.connector import errorcode
import datetime

# Global values
STUDENT_EMAIL = None
STUDENT_FIRST_NAME = None
STUDENT_LAST_NAME = None

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
    print "\t\'cart\': Show your current cart"
    print "\t\'browse\': Browse for books, and add them to your cart"
    print "\t\'remove cart\': Remove items from your cart"
    print "\t\'purchase\': Purchase the items in your cart"
    print "\t\'orders\': View all books you have ordered"
    print "\t\'remove order\': Remove items from an order"
    print "\t\'ticket\': Submit a Trouble Ticket to the Book Fetch Employees"

def signIn():
    global STUDENT_EMAIL, STUDENT_FIRST_NAME, STUDENT_LAST_NAME

    # Ask user for their email
    studentEmail = raw_input("Please enter your email: ")

    # Get connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except Exception as err:
        print err

    # Verify email is in the database
    try:
        cursor = connection.cursor()
        sql = 'SELECT * FROM student WHERE student.email = \'' + studentEmail + '\';'
        cursor.execute(sql)
        result = cursor.fetchone()

        # email wasn't found, print error
        if result == None:
            print "\nThe email " + studentEmail + " is not registered to the Book Fetch system!"
            return False

        # email was found, print greeting, set globals
        else:
            sql = 'SELECT first_name FROM users WHERE users.email = \'' + studentEmail + '\';'
            cursor.execute(sql)
            result = cursor.fetchone()
            STUDENT_FIRST_NAME = result[0]

            sql = 'SELECT last_name FROM users WHERE users.email = \'' + studentEmail + '\';'
            cursor.execute(sql)
            result = cursor.fetchone()           
            STUDENT_LAST_NAME = result[0]

            sql = 'SELECT email FROM users WHERE users.email = \'' + studentEmail + '\';'
            cursor.execute(sql)
            result = cursor.fetchone()           
            STUDENT_EMAIL = result[0]

            print "Welcome back " + STUDENT_FIRST_NAME + '!'
            return True

    except Exception as err:
        print err

    finally:
        connection.close()

def signedIn():
    return STUDENT_EMAIL != None

def status():
    print "\nUser Information:"
    print "Name: " + STUDENT_FIRST_NAME + " " + STUDENT_LAST_NAME
    print "Email: " + STUDENT_EMAIL

def greetUser():
    print "\nWelcome to Book Fetch!\n"
    hasAccount = ''

    # Pester user if they have an account
    while True:

        # ask first
        hasAccount = raw_input("Do you have an account with us? ('y' or 'n'... or 'exit' ): ")

        # user says they have an account
        if hasAccount == 'y':
            signIn()

            # user really does have an account
            if signedIn():
                break

            # user's email is wrong
            else:
                print "Perhaps you should register a new account\n"

        # user says they dont have an account
        elif hasAccount == 'n':
            signUp = raw_input("Would you like to make an account? ('y' or 'n'... or 'exit' ): ")

            # user wishes to make a new account
            if signUp == 'y':
                created = createAccount()

                if created == False:
                    print "\n*** Account was NOT registered! ***\n"

                else:
                    print "\n*** Your account has been registered. Now log in to access your account! ***\n"

            # user does not have account, and they dont want to make a new one, quit the program
            elif signUp == 'n':
                print "An account is required to use Book Fetch. The program will now terminate."
                break

            # Interrupt
            elif signUp == 'exit':
                print "The program will now terminate."
                return False

        # Interrupt
        elif (hasAccount == 'exit'):
            print "The program will now terminate."
            return False

    return hasAccount == 'y'

def createAccount():

    while True:
        print "\nSupply the following information"
        print "Enter 'restart' to start over or type 'exit' to quit account creation\n"

        firstName = raw_input("\nWhat is your first name?: ")
        if firstName == 'exit':
            return False
        if firstName == 'restart':
            continue

        lastName = raw_input("\nWhat is your last name?: ")
        if lastName == 'exit':
            return False
        if lastName == 'restart':
            continue

        email = raw_input("\nWhat is your email address?: ")
        if email == 'exit':
            return False
        if email == 'restart':
            continue
    
        address = raw_input("\nWhat is your street address?: ")
        if address == 'exit':
            return False
        if address == 'restart':
            continue

        phone = raw_input("\nWhat is your phone number?: ")
        if phone == 'exit':
            return False
        if phone == 'restart':
            continue

        birth = raw_input("\nWhat is your birthday? (Please enter in format YYYY-MM-DD): ")
        if birth == 'exit':
            return False
        if birth == 'restart':
            continue

        major = raw_input("\nWhat is your college major?: ")
        if major == 'exit':
            return False
        if major == 'restart':
            continue

        status = raw_input("\n'Grad' or 'UnderGrad'?: ")
        if status == 'exit':
            return False
        if status == 'restart':
            continue

        year = raw_input("\nWhat year of college are you? (1, 2, 3, or 4): ")
        if year == 'exit':
            return False
        if year == 'restart':
            continue

        univ = raw_input("\nWhat is the name of the university you attend?: ")
        if univ == 'exit':
            return False
        if univ == 'restart':
            continue

        print "\n***Please verify the following information***"
        print "First Name: ", firstName
        print "Last Name: ", lastName
        print "Email: ", email
        print "Street Address: ", address
        print "Phone Number: ", phone
        print "Date of Birth: ", birth
        print "College Major: ", major
        print "Student Status: ", status
        print "Student Year: ", year
        print "University: ", univ

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

        sql = 'INSERT INTO student(email, birth_date, major, student_status, student_year, univ_name)' +\
                'VALUES (\'' + email + '\', \'' + birth + '\', \'' + major + '\', \'' + status + '\',' + year + ', \'' + univ + '\');'

        cursor.execute(sql)

        connection.commit()

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

def printCategories():
    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except AttributeError as err:
        raise err
        

    # Once connected try to get all categories
    try:
        cursor = connection.cursor()
        sql = 'SELECT category from category'
        cursor.execute(sql)
        result = cursor.fetchall()
        print "Here are all the available categories on Book Fetch:\n"
        
        for row in result:
            print str(row)[3:-3] + "   ",

        print "\n"

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

def browseBooks():
    print "\nWelcome to the book browser!"
    printCategories()
    category = ''
    
    while True:
        category = raw_input("Enter a category of book (or 'exit'): ")

        if category == 'exit':
            print "Returning to main menu\n"
            return

        else:
            # Open connection
            try:
                connection = getConnection()
                connection.autocommit = True
            except AttributeError as err:
                raise err
        

            # Once connected try to get books
            try:
                cursor = connection.cursor()
                sql = 'SELECT * from category LEFT JOIN book ON (book.title = category.book_title) WHERE category = \'' + category + '\';'
                cursor.execute(sql)
                result = cursor.fetchall()

                if (len(result) == 0):
                    print "Either there are no books available in " + category + " or the category " + category + " doesn't exist!"

                else:
                    print "Here are all books in the " + category + " category:"

                    for row in result:
                        print "Title: ", row[0], "\t\tBook Type: ", row[4], "\tPurchase type: ", row[5], "\tPrice: ", row[6], "\tCopies available: ", row[7], "\tRating: ", row[15]

                    addBook = raw_input("Would you like to add any of these to your cart? ('y' or 'n'... or 'exit' ): ")

                    if addBook == 'y':
                        bookTitle = raw_input("Enter the title of the book you wish to add to your cart: ")
                        quantity = raw_input("How many copies should be added to cart: ")
                        addToCart(bookTitle, int(quantity))

                        print ''
                        viewCart()
                        print ''
                    
                    if addBook == 'exit':
                        print "Returning to main menu\n"
                        return


            except mysql.connector.Error as err:
                print err
                connection.close()

            # if it cant get books, abort
            except Exception as err:
                print err
                connection.rollback()
                connection.close()

            finally:
                connection.close()    

def addToCart(bookTitle, quantity):
    now = datetime.datetime.now()

    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = False
    except AttributeError as err:
        raise err
        
    # Once connected try to update cart
    try:
        cursor = connection.cursor()

        # current date
        date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)

        sql = 'SELECT quantity FROM book WHERE title = \'' + bookTitle + '\';'
        cursor.execute(sql)
        result = cursor.fetchone()

        # cannot add to cart, quantity too high
        if quantity > int(result[0]):
            print "\nCannot add", quantity, "to cart. There are only", result[0], "copies of", bookTitle, "left."
            return

        # reduce quantity of books in stock
        else:
            newQuantity = int(result[0]) - quantity
            sql = 'UPDATE book SET quantity = ' + str(newQuantity) + ' WHERE title = \'' + bookTitle + '\';'
            cursor.execute(sql)
            connection.commit()

        # if user has a cart already, only update the cart and add book
        if hasCart():
            sql = 'UPDATE cart SET last_updated = \'' + date + '\' WHERE student_email = \'' + STUDENT_EMAIL + '\';'
            
            cursor.execute(sql)

            sql = 'INSERT INTO being_purchased (student_email, book_title, quantity)\
                    VALUES (\'' + STUDENT_EMAIL + '\', \'' + bookTitle + '\', ' + str(quantity) + ');'

            cursor.execute(sql)
            connection.commit()

        # if the user does not have a cart, create a new one, and add the book
        else:
            sql = 'INSERT INTO cart(date_created, last_updated, student_email)\
                    VALUES (\'' + date +  '\', \'' + date + '\', \'' + STUDENT_EMAIL + '\');'
            
            cursor.execute(sql)

            sql = 'INSERT INTO being_purchased (student_email, book_title, quantity)\
                    VALUES (\'' + STUDENT_EMAIL + '\', \'' + bookTitle + '\', ' + str(quantity) + ');'

            cursor.execute(sql)
            connection.commit()

    except mysql.connector.Error as err:
        print err
        connection.close()
        return

    # if it cant find cart, abort
    except Exception as err:
        print err
        connection.rollback()
        connection.close()
        return

    finally:
        connection.close()

def hasCart():
    cartBool = None
    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except AttributeError as err:
        raise err
        

    # Once connected try to see if the student has a cart
    try:
        cursor = connection.cursor()
        sql = 'SELECT * from cart WHERE student_email = \'' + STUDENT_EMAIL + '\';'
        cursor.execute(sql)
        result = cursor.fetchall()
        cartBool = (len(result) != 0)

    except mysql.connector.Error as err:
        print err
        connection.close()
        return None


    # if it cant find cart, abort
    except Exception as err:
        print err
        connection.rollback()
        connection.close()
        return None

    finally:
        connection.close()
        return cartBool

def removeFromCart():
    # return if cart doesn't exist
    if (hasCart() == False):
        print "You don't have a cart to remove items from"
        return

    cartOption = ''

    while True:
        print ''
        viewCart()
        print ''

        cartOption = raw_input("Enter the title of the book you wish to remove (or 'exit'): ")

        if cartOption == 'exit':
            print "Returning to main menu\n"
            return

        else:

            now = datetime.datetime.now()

            # Open connection
            try:
                connection = getConnection()
                connection.autocommit = False

            except AttributeError as err:
                raise err
        
            # Once connected try to update cart
            try:
                # current date
                date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
                cursor = connection.cursor()
                sql = 'UPDATE cart SET last_updated = \'' + date + '\' WHERE student_email = \'' + STUDENT_EMAIL + '\';'
                cursor.execute(sql)

                # add quantity back to stock
                sql = 'SELECT quantity FROM being_purchased WHERE student_email = \'' + STUDENT_EMAIL + '\' AND book_title = \'' + cartOption + '\';'
                cursor.execute(sql)
                removed = cursor.fetchone()

                sql = 'SELECT quantity FROM book WHERE title = \'' + cartOption + '\';'
                cursor.execute(sql)
                stock = cursor.fetchone()

                newStock = int(removed[0]) + int(stock[0])
                sql = 'UPDATE book SET quantity = ' + str(newStock) + ' WHERE title = \'' + cartOption + '\';'
                cursor.execute(sql)

                sql = 'DELETE FROM being_purchased WHERE student_email = \'' + STUDENT_EMAIL + '\' AND book_title = \'' + cartOption + '\';'
                cursor.execute(sql)
                connection.commit()

                sql = 'SELECT book_title, quantity from being_purchased WHERE student_email = \'' + STUDENT_EMAIL + '\';'
                cursor.execute(sql)
                connection.commit
                result = cursor.fetchall()

                # if that was the last book in the cart, then delete the cart
                if len(result) == 0:
                    sql = 'DELETE FROM cart WHERE student_email = \'' + STUDENT_EMAIL + '\';'
                    cursor.execute(sql)
                    connection.commit()
                    print "\nYour cart is now empty, returning to main menu\n"
                    return

            except mysql.connector.Error as err:
                print err
                connection.close()
                return None

            # if it cant find cart, abort
            except Exception as err:
                print err
                connection.rollback()
                connection.close()
                return None

            finally:
                connection.close()

def createOrder():
    now = datetime.datetime.now()
    date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)

    if (hasCart() == False):
        print "You don't have a cart to make an order. Returning to the main menu"
        return False

    print "Here are the books that you wish to purchase:"
    print ""
    viewCart()
    print ""

    optOut = raw_input("Would you like to purchase these, or continue shopping?: ('y' or 'n'): ")

    if optOut == 'n':
        return False

    while True:
        print "\nSupply the following information"
        print "Enter 'restart' to start over or type 'exit' to quit ordering\n"

        cardNum = raw_input("What is your credit card number: ")
        if cardNum == 'exit':
            return False
        if cardNum == 'restart':
            continue

        cardExp = raw_input("What is your card expiration date? (YYYY-MM-DD): ")
        if cardExp == 'exit':
            return False
        if cardExp == 'restart':
            continue

        cardName = raw_input("What is the name of your card?: ")
        if cardName == 'exit':
            return False
        if cardName == 'restart':
            continue

        cardType = raw_input("what is the type of your card?: ")
        if cardType == 'exit':
            return False
        if cardType == 'restart':
            continue

        shipType = raw_input("What shipping type would you like? ('1-day', '2-day' or 'standard'): ")
        if shipType == 'exit':
            return False
        if shipType == 'restart':
            continue


        print 'Please verify the following information:'
        print "Credit Card Number: ", cardNum
        print "Credit Card Expiration date: ", cardExp
        print "Credit Card Name: ", cardName
        print "Credit Card Type: ", cardType
        print "Shipping type: ", shipType

        verify = ''

        while True:
            verify = raw_input("\nIs this information correct? ('y' or 'n'): ")
            if verify == 'n':
                return False
            if verify == 'y':
                break

        break

    # Now insert all this information into the orders table

    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = False
    except AttributeError as err:
        raise err
        

    # Once connected try to insert
    try:
        cursor = connection.cursor()

        # create order
        sql = 'INSERT INTO orders(student_email, date_created, date_fulfilled, shipping_type, card_num, card_exp, card_name, card_type, order_status)\
                VALUES (\'' + STUDENT_EMAIL + '\', \'' + date + '\', null, \'' + shipType + '\', \'' + cardNum + '\', \'' + cardExp + '\', \'' + cardName  + '\', \'' + cardType + '\', \'new\');'

        cursor.execute(sql)

        # Move the books in being_purchased to purchased
        sql = 'SELECT * FROM being_purchased WHERE student_email = \'' + STUDENT_EMAIL + '\';'
        cursor.execute(sql)
        result = cursor.fetchall()

        for row in result:
            title = row[1]
            quantity = str(row[2])

            sql = 'INSERT INTO purchased (student_email, book_title, quantity, date_purchased)\
                    VALUES (\'' + STUDENT_EMAIL + '\', \'' + title + '\', ' + quantity + ', \'' + date + '\');'
            
            cursor.execute(sql)

        sql = 'DELETE FROM being_purchased WHERE student_email = \'' + STUDENT_EMAIL + '\';'
        cursor.execute(sql)

        # delete cart
        sql = 'DELETE FROM cart WHERE student_email = \'' + STUDENT_EMAIL + '\';'
        cursor.execute(sql)

        connection.commit()


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

def order():
    orderMade = createOrder()

    if orderMade == False:
        print "Your order was not created"

    else:
        print "Your order has been created"

def viewCart():
    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except AttributeError as err:
        raise err
        

    # Once connected try to get student's cart
    try:
        cursor = connection.cursor()
        sql = 'SELECT book_title, quantity from being_purchased WHERE student_email = \'' + STUDENT_EMAIL + '\';' 
        cursor.execute(sql)
        result = cursor.fetchall()

        if (len(result) == 0):
            print("Your cart is empty")

        else:
            print "Here is your cart:\n"

            totalPrice = 0
            for row in result:
                sql = 'SELECT * from book WHERE title = \'' + row[0] + '\';'
                cursor.execute(sql)
                book = cursor.fetchone()

                print "Book Title: ", row[0], "\tQuantity: ", row[1], "\tBook Type: ", book[2], "\tPurchase Type: ", book[3], "\tPrice: ", book[4]
                totalPrice += int(book[4])

            print "\nTotal Price: ", totalPrice

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

def viewOrders():
    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except AttributeError as err:
        raise err
        

    # Once connected try to get student's cart
    try:
        cursor = connection.cursor()
        sql = 'SELECT * from purchased left join orders ON (purchased.student_email = orders.student_email AND purchased.date_purchased = orders.date_created)\
        WHERE purchased.student_email = \'' + STUDENT_EMAIL + '\';' 
        cursor.execute(sql)
        result = cursor.fetchall()

        if (len(result) == 0):
            print("You have no orders")

        else:
            print "Here are your orders:\n"
        
            orders = []
            for row in result:
                if row[3] not in orders:
                    orders.append(row[3])
                    print "Order on", row[3], ":"
                print "\tBook Title: ", row[1], "\t Quantity: ", row[2], "\tPurchased on: ", row[3]


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

def removeOrder():
    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except AttributeError as err:
        raise err
        

    # Once connected try to get student's cart
    try:
        cursor = connection.cursor()
        sql = 'SELECT * from purchased left join orders ON (purchased.student_email = orders.student_email AND purchased.date_purchased = orders.date_created)\
        WHERE purchased.student_email = \'' + STUDENT_EMAIL + '\';' 
        cursor.execute(sql)
        result = cursor.fetchall()

        if (len(result) == 0):
            print("You have no orders")

        else:
            orderOption = ''
            dateOption = ''

            while True:
                viewOrders()

                orderOption = raw_input("Enter the name of the book you wish to remove from your orders (or 'exit'): ")
                if orderOption == 'exit':
                    print 'Returning to main menu'
                    return

                dateOption = raw_input("Enter the date of the order (or 'exit'): ")
                if dateOption == 'exit':
                    print 'Return to main menu'
                    return

                # add quantity back to stock
                sql = 'SELECT quantity FROM purchased WHERE student_email = \'' + STUDENT_EMAIL + '\' AND book_title = \'' + orderOption + '\' AND date_purchased = \'' + dateOption + '\';'
                cursor.execute(sql)
                removed = cursor.fetchone()

                sql = 'SELECT quantity FROM book WHERE title = \'' + orderOption + '\';'
                cursor.execute(sql)
                stock = cursor.fetchone()

                newStock = int(removed[0]) + int(stock[0])
                sql = 'UPDATE book SET quantity = ' + str(newStock) + ' WHERE title = \'' + orderOption + '\';'
                cursor.execute(sql)

                sql = 'DELETE FROM purchased WHERE student_email = \'' + STUDENT_EMAIL + '\' AND book_title = \'' + orderOption + '\' AND date_purchased = \'' + dateOption + '\';'
                cursor.execute(sql)

                sql = 'SELECT book_title, quantity from purchased WHERE student_email = \'' + STUDENT_EMAIL + '\' AND date_purchased = \'' + dateOption + '\';'
                cursor.execute(sql)
                connection.commit
                result = cursor.fetchall()

                # if that was the last book in the order, then delete the order
                if len(result) == 0:
                    sql = 'DELETE FROM orders WHERE student_email = \'' + STUDENT_EMAIL + '\' AND date_created = \'' + dateOption +'\';'
                    cursor.execute(sql)
                    connection.commit()

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

def rateBook():
    print "Welcome to the book rating browser!"
    printCategories()
    category = ''
    
    while True:
        category = raw_input("Enter a category of book (or 'exit'): ")

        if category == 'exit':
            print "Returning to main menu\n"
            return

        else:
            # Open connection
            try:
                connection = getConnection()
                connection.autocommit = True
            except AttributeError as err:
                raise err
        

            # Once connected try to get books
            try:
                cursor = connection.cursor()
                sql = 'SELECT * from category LEFT JOIN book ON (book.title = category.book_title) WHERE category = \'' + category + '\';'
                cursor.execute(sql)
                result = cursor.fetchall()

                if (len(result) == 0):
                    print "Either there are no books available in " + category + " or the category " + category + " doesn't exist!"

                else:
                    print "Here are all books in the " + category + " category:"

                    for row in result:
                        print "Title: ", row[0], "\t\tBook Type: ", row[4], "\tPurchase type: ", row[5], "\tPrice: ", row[6], "\tCopies available: ", row[7], "\tRating: ", row[15]

                    rateBook = raw_input("Would you like to rate any of these books? ('y' or 'n'... or 'exit' ): ")

                    if rateBook == 'y':
                        bookTitle = raw_input("Enter the title of the book you wish to rate: ")
                        bookRating = raw_input("Please enter a rating between 1 and 5: ")

                        # Update the student ratings table
                        sql = 'INSERT INTO student_reviews (rating, book_title, student_email)\
                                 VALUES (' + bookRating + ', \'' + bookTitle + '\', \'' + STUDENT_EMAIL + '\');'

                        cursor.execute(sql)

                        sql = 'SELECT rating FROM student_reviews WHERE book_title = \'' + bookTitle + '\';'
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        numReviews = len(result)

                        sql = 'SELECT rating FROM book WHERE title = \'' + bookTitle + '\';'
                        cursor.execute(sql)
                        result = cursor.fetchone()
                        currentRating = result[0]

                        newRating = (int(currentRating) * numReviews)  + int(bookRating) / (numReviews + 1)

                        sql = 'UPDATE book SET rating = ' + str(newRating) + ' WHERE title = \'' + bookTitle + '\';'
                        cursor.execute(sql)

                        print "Success! You have rated", bookTitle, "with a", bookRating, "out of 5!"
                        return
                        
                    
                    if rateBook == 'exit':
                        print "Returning to main menu\n"
                        return


            except mysql.connector.Error as err:
                print err
                connection.close()

            # if it cant get books, abort
            except Exception as err:
                print err
                connection.rollback()
                connection.close()

            finally:
                connection.close()

def getSkips():
    return ["and", ",", ".", "to", "the", "for", "in", "of", "that", "a", "on", "is", "get", "you", "has", "as",
         "at", "are", "", "an", "with", "will", "not", "have", "would", "so", "", "but", ":", "be", "like",
         "if", "should", "also", "there", "or", "by", "per", "they", "only", "can", "I", "who", "this",
         "it", "from", "one", "their", "The", "then", "his", "J", "we", "If", "?", "!"]

def printRecomendations():
    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = True
    except AttributeError as err:
        raise err
        

    # Once connected try to get student's cart
    try:

        # get all categories that have been purchased
        cursor = connection.cursor()
        sql = 'SELECT category from purchased LEFT JOIN category ON (purchased.book_title = category.book_title)\
                WHERE purchased.student_email = \'' + STUDENT_EMAIL + '\';' 
        cursor.execute(sql)
        result = cursor.fetchall()

        recomended = []
        categories = []
        purchased = []
        for row in result:
            categories.append(row[0])

        # get all keywords that have been purchased
        sql = 'SELECT keyword, purchased.book_title FROM purchased LEFT JOIN keyword ON (purchased.book_title = keyword.book_title)\
                WHERE purchased.student_email = \'' + STUDENT_EMAIL + '\';'
        cursor.execute(sql)
        result = cursor.fetchall()

        keywords = []
        for row in result:
            keywords.append(row[0])
            purchased.append(row[1])

        # no recomendations to give because no previous orders
        if (len(categories) == 0 or len(keywords) == 0):
            return

        # recomendations can be genereated off previous order
        else:
            sameCategory = []
            sameKeyword = []

            # get all books with the same category
            for category in categories:
                sql = 'SELECT book_title FROM category WHERE category = \'' + category + '\';'
                cursor.execute(sql)
                result = cursor.fetchall()

                for row in result:
                    sameCategory.append(row[0])

            for book in sameCategory:
                if book not in purchased:
                    recomended.append(book)

            # get all books with the same keywords
            for keyword in keywords:
                # skip keywords that are common
                if keyword not in getSkips():
                    sql = 'SELECT book_title from keyword WHERE keyword = \'' + keyword + '\';'
                    cursor.execute(sql)
                    result = cursor.fetchall()

                    for row in result:
                        sameKeyword.append(row[0])
            
            for book in sameKeyword:
                if book not in purchased:
                    recomended.append(book)

            # if there are at least 3 recomendations
            if len(recomended) >= 3:
                print "\nHere are a few recomendations for you based on you last purchases: "

                for numRecs in range(0,3):
                    print str(numRecs + 1) + '. ' + recomended[numRecs]

            # not enough recomendations generated to print them
            else:
                return
                
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

def createTicket():
    now = datetime.datetime.now()
    date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)

    while True:
        print "\nSupply the following information"
        print "Enter 'restart' to start over or type 'exit' to quit submitting a trouble ticket\n"

        category = raw_input("What is the category of this issue ('user profile', 'products', 'cart', 'orders', 'other'): ")
        if category == 'exit':
            return
        if category == 'restart':
            continue
        
        title = raw_input("Give your trouble ticket a title: ")
        if title == 'exit':
            return
        if title == 'restart':
            continue

        desc = raw_input("Give a description of the issue: ")
        if desc == 'exit':
            return
        if desc == 'restart':
            continue

        print 'Please verify the following information:'
        print "Category: ", category
        print "title: ", title
        print "Description: ", desc

        verify = ''

        while True:
            verify = raw_input("\nIs this information correct? ('y' or 'n'): ")
            if verify == 'n':
                return False
            if verify == 'y':
                break

        break

    # Now insert all this information into the touble_ticket table

    # Open connection
    try:
        connection = getConnection()
        connection.autocommit = False
    except AttributeError as err:
        raise err
        

    # Once connected try to insert
    try:
        cursor = connection.cursor()

        # get the max ticket id\
        sql = 'SELECT MAX(ticket_id) FROM trouble_ticket;'
        cursor.execute(sql)
        result = cursor.fetchone()
        currentMax = result[0][1:]
        newId = 'T' + str(int(currentMax) + 1)

        # create ticket
        sql = 'INSERT INTO trouble_ticket(ticket_id, state, category, date_logged, title, description,\
					creator_name, creator_type, customer_support_user_name, administrator_name, solution)\
                VALUES (\'' + newId + '\', \'new\', \'' + category + '\', \'' + date + '\', \'' + title + '\', \'' + desc\
                + '\', \'' + STUDENT_FIRST_NAME + '\', \'student\', null, null, null);'

        cursor.execute(sql)
        connection.commit()

        print "Your ticket has been submitted!"

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

    printRecomendations()

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

        if userOption == 'browse':
            browseBooks()
            continue

        if userOption == 'cart':
            viewCart()
            continue

        if userOption == 'remove cart':
            removeFromCart()
            continue

        if userOption == 'remove order':
            removeOrder()
            continue

        if userOption == 'purchase':
            order()
            continue

        if userOption == 'orders':
            viewOrders()
            continue

        if userOption == 'rate':
            rateBook()
            continue

        if userOption == 'ticket':
            createTicket()
            continue

        else:
            print 'Unknown command: \'' + userOption + '\''

main()