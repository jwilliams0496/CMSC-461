########################################################################################
# File: customer_support_module.py
# Author: James Williams
# Description: Provides the command line interface for the customer support users of Book Fetch
# Inc. to use when preforming actions and use cases associated with them
########################################################################################

import mysql.connector
from mysql.connector import errorcode
import datetime

# Global values
EMPLOYEE_EMAIL = None
EMPLOYEE_FIRST_NAME = None
EMPLOYEE_LAST_NAME = None

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

def signIn():
    global EMPLOYEE_EMAIL, EMPLOYEE_FIRST_NAME, EMPLOYEE_LAST_NAME

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
        sql = 'SELECT * FROM customer_support_user\
                LEFT JOIN employee ON (customer_support_user.email = employee.email)\
                WHERE customer_support_user.email = \'' + employeeEmail + '\';'
        cursor.execute(sql)
        result = cursor.fetchone()

        # email wasn't found, print error
        if result == None:
            print "\nThe email \'" + employeeEmail + "\' is not registered to the Book Fetch system!"
            return False

        # email was found, print greeting, set globals
        else:
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

def greetUser():
    print "\nWelcome to the Book Fetch Inc Customer Support Module"

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

def createTicket():
    global EMPLOYEE_EMAIL, EMPLOYEE_FIRST_NAME, EMPLOYEE_LAST_NAME

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
                + '\', \'' + EMPLOYEE_FIRST_NAME + '\', \'customer_support_user\', \'' + EMPLOYEE_FIRST_NAME + '\', null, null);'

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

def viewTickets():
    print "\nWelcome to the ticket viewer."

    edit = ''
    while True:
        edit = raw_input("View all tickets? or edit only 'new' tickets? ('view' or 'edit'... or 'exit' ): ")

        if edit == 'exit':
            print "Returning to the main menu."
            return
        
        if edit == 'view' or edit == 'edit':
            break

    viewType = ''
    while True:
        viewType = raw_input("Enter the ceategory of tickets you would like to view ('user profile', 'products', 'cart', 'orders', 'other'): ")

        # coerce correct input from user
        if (viewType == 'user profile' or viewType == 'products' or viewType == 'cart' or viewType == 'orders' or viewType == 'other'):
            if edit == 'view':
                printTickets(viewType)
            elif edit == 'edit':
                editTicket(viewType)
            break

        else:
            print "Unknown category " + viewType

def printTickets(category):
    print "Here are all the tickets in " + category + ":"

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
        sql = 'SELECT * FROM trouble_ticket WHERE category = \'' + category + '\';'
        cursor.execute(sql)
        
        result = cursor.fetchall()

        for row in result:
            print "\n######################################################\n"
            print "Ticket ID: " + row[0]
            print "Title: " + row[4]
            print "Creator: A " + row[7] + " named " + row[6]
            print "Date Logged: " + str(row[3])
            print "State: " + row[1] + "\n"

            if row[5] != None:
                print "Description: " + row[5]

            if row[8] != None:
                print "\nThe ticket has been marked by " + row[8]
            else:
                print "\nThis ticket has not been marked yet"

            if row[9] != None:
                print 'This ticket has been assigned to: ' + row[9]
            else:
                print 'This ticket has not been assigned yet'
            
            if row[10] != None:
                print "\nSolution: " + row[10]

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

def editTicket(category):
    now = datetime.datetime.now()
    date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    print "Here are all new the tickets in " + category + ":"

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

        # get all new tickets
        sql = 'SELECT * FROM trouble_ticket WHERE state = \'new\' AND category = \'' + category + '\';'
        cursor.execute(sql)
        allnew = cursor.fetchall()

        # get all tickets that aren't new
        sql = 'SELECT * FROM trouble_ticket WHERE state != \'new\' AND category = \'' + category + '\';'
        cursor.execute(sql)
        assign = cursor.fetchall()

        # only add tickets that haven't been assigned yet
        new = []
        for newRow in allnew:
            assigned = False
            for assignedRow in assign:
                if newRow[0] == assignedRow[0]:
                    assigned = True
                    break
            
            if assigned == False:
                new.append(newRow)

        # If there are now tickets in this category return
        if (len(new) == 0):
            print "\nHooray! There are no new trouble tickets to mark in " + category + '\n'
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

        admin = raw_input("Enter the first name of the administrator you would like to assign to this ticket (or 'exit'): ")

        if admin == 'exit':
            print "Returning to the main menu"
            return

        sql = 'SELECT * FROM administrator JOIN employee ON (administrator.email = employee.email) JOIN users ON (administrator.email = users.email)\
                WHERE users.first_name = \'' + admin + '\';'

        cursor.execute(sql)
        result = cursor.fetchall()

        if len(result) == 0:
            print "\nError: The administrator name " + admin + " doesn't exist in the Book Fetch Employee table."
            return

        # make sure the ticket that the user has entered is one of the new tickets shown
        exists = False
        for row in new:
            if ticket == row[0]:
                exists = True
                ticket_tuple = row
                break

        if exists == False:
            print "\nError: ticket " + ticket + " not a 'new' ticket in the category " + category
            return

        # get existing ticket info here, and create a new ticket
        sql = 'INSERT INTO trouble_ticket(ticket_id, state, category, date_logged, title, description,\
				creator_name, creator_type, customer_support_user_name, administrator_name, solution)\
                VALUES (\'' + ticket + '\', \'assigned\', \'' + category + '\', \'' + date + '\', \'' + ticket_tuple[4] + '\', \'' + ticket_tuple[5]\
                + '\', \'' + ticket_tuple[6] + '\', \'' + ticket_tuple[7] + '\', \'' + EMPLOYEE_FIRST_NAME + '\', \'' + admin + '\', null);'

        cursor.execute(sql)

        print "Ticket " + ticket + " has been assigned to " + admin
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

        if userOption == 'ticket':
            createTicket()
            continue

        if userOption == 'tickets':
            viewTickets()
            continue

        # todo: more options here

        else:
            print 'Unknown command: \'' + userOption + '\''

main()