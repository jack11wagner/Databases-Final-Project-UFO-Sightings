"""
Databases Final Project F2021
This project uses UFO report data from http://www.nuforc.org/webreports.html
Author: Nikolas Kovacs
"""

from __future__ import print_function
import mysql.connector


def connectToMySQL():
    """
    Establishes a connection to the database
    """
    cnx = mysql.connector.connect(password='project', user='project')
    cursor = cnx.cursor()
    return cursor, cnx


def createDatabase(cursor, database_name):
    """
    :param cursor: instance of the connection to the database
    :param database_name: name of the database to create
    Creates the database at cursor with the given name.
    """
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8';".format(database_name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def createTables(cursor):
    """
    This function creates the tables Report and Location to the UFO database
    :param cursor: instance of the connection to the database
    """
    try:

        sql = "CREATE TABLE Report (ID INT AUTO_INCREMENT PRIMARY KEY,city VARCHAR(35)," \
              "date DATE,time TIME, shape VARCHAR(10),posted DATE, summary VARCHAR(200), " \
              "duration TIME);"
        cursor.execute(sql)

        sql = "CREATE TABLE Location (city varchar(20) PRIMARY KEY,state char(2));"
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print("Failed creating tables: {}".format(err))
        exit(1)


def getYearFromUser():
    user_input = input("Enter a year: ")
    while not user_input.isdigit():
        user_input = input("Error... Enter a year: ")
    return user_input


def getStateFromUser():
    user_input = input("Enter a state (two letter abbreviation): ")
    while len(user_input) != 2 or user_input.isdigit():
        user_input = input("Error... Enter a state (two letter abbreviation): ")
    return user_input.upper()


def getShapeFromUser():
    user_input = input("Enter a shape (ex. circle, triangle, etc): ")
    while len(user_input) < 1 or user_input.isdigit():
        user_input = input("Error... Enter a shape (ex. circle, triangle, etc): ")
    return user_input.lower()


def isGoodDuration(duration):
    if duration.count(":") != 2:
        return False
    hours, minutes, seconds = duration.split(":")
    if not hours.isdigit() or not minutes.isdigit() or not seconds.isdigit():
        return False

    hours, minutes, seconds = int(hours), int(minutes), int(seconds)

    if 0 > hours or hours > 24:
        return False
    if 0 > minutes or minutes > 59:
        return False
    if 0 > seconds or seconds > 59:
        return False

    return True


def getDurationFromUser():
    print("Duration follows the format HH:MM:SS")
    user_input = input("Enter a duration: ")
    while not isGoodDuration(user_input):
        user_input = input("Error... Enter a duration: ")
    return user_input


def getPositiveIntegerFromUser():
    user_input = input("Enter a number greater than 0: ")
    while not user_input.isdigit() or int(user_input) < 1:
        user_input = input("Error... Enter a number greater than 0: ")
    return user_input


def executePartialQuery(cursor, query, option):
    if option == 0:
        year = getYearFromUser()
        query = query.format(year)
    elif option == 5:
        num = getPositiveIntegerFromUser()
        query = query.format(num)

    with open("questions.txt", 'r') as questions:
        question = ""
        for i, line in enumerate(questions):
            if i > option:
                break
        question = line.strip()
        print(question)
    print(query)
    print()

    cursor.execute(query)
    results = cursor.fetchone()
    while results is not None:
        for result in results:
            # if result is None:
            #     continue
            print(result)
        results = cursor.fetchone()
        print()


def executeQueryAllAttributes(cursor, query, option):
    """
    This function executes a query and prints out the results
    :param option: an index corresponding with the query being executed
    :param cursor: instance of the connection to the database
    :param query: the query to be executed
    """
    if option == 1:
        state = getStateFromUser()
        query = query.format(state)
    elif option == 2:
        shape = getShapeFromUser()
        query = query.format(shape)
    elif option == 3:
        duration = getDurationFromUser()
        query = query.format(duration)
    elif option == 4:
        year = getYearFromUser()
        query = query.format(year)

    attributeList = ["ID: ", "City: ", "State: ", "Date: ", "Time: ", "Shape: ", "Summary: ", "Duration: ", "Posted: "]
    # all other queries do not require user input

    with open("questions.txt", 'r') as questions:
        question = ""
        for i, line in enumerate(questions):
            if i > option:
                break
        question = line.strip()
        print(question)
    print(query)
    print()

    cursor.execute(query)
    results = cursor.fetchone()

    while results is not None:
        i = 0
        for result in results:
            # if result is None:
            #     continue
            print(attributeList[i], end="")
            i += 1
            print(result)
        results = cursor.fetchone()
        print()


def insertIntoDatabase(cursor, datafile):
    """
    This function takes attributes and inserts them into the database
    :param datafile: the file from which the data is read
    :param cursor: an instance of the connection to the database
    """
    print("Inserting data into database...")
    with open(datafile, "r") as data:
        data.readline()  # skip first line
        for line in data:
            line = line.strip().split("|")
            # print(line)
            date, time, city, state, shape, duration, summary, posted = line

            sql = "insert into report (date, time, city, shape, duration, summary, posted) " \
                  f"values ({date}, {time}, {city}, {shape}, {duration}, {summary}, {posted});"
            cursor.execute(sql)

            sql = "insert ignore into location (city, state) values" \
                  f"({city}, {state})"
            cursor.execute(sql)
    print("Complete!")
    
    
def getUserOption(alphabet):
    num_lines = 0
    print("a. Load Data Into Database")
    with open("questions.txt", 'r') as questions:
        for i, line in enumerate(questions):
            print(f"{alphabet[i]}. {line.strip()}")
            num_lines = i + 1
    alphabet = alphabet[:num_lines]
    user_input = input("Choose an option to execute or press q to quit: ").lower()
    if user_input == "q" or user_input == "a":
        return user_input
    while len(user_input) != 1 or user_input not in alphabet:
        user_input = input("Error... Choose a query to execute or press q to quit: ").lower()
        if user_input == "q" or user_input == "a":
            return user_input
    print()
    return user_input


def loadQueries():
    queries_list = []
    with open("queries.txt", 'r') as queries:
        for line in queries:
            queries_list.append(line.strip())
    return queries_list


def dropAndFill(cursor, database_name):
    sql = "DROP DATABASE IF EXISTS " + database_name + ";"
    cursor.execute(sql)
    createDatabase(cursor, database_name)
    cursor.execute("USE {}".format(database_name))
    createTables(cursor)
    insertIntoDatabase(cursor, "data.txt")


def main():
    database_name = "UFO"
    cursor, connection = connectToMySQL()

    # sql = "DROP DATABASE IF EXISTS " + database_name + ";"
    # cursor.execute(sql)
    # createDatabase(cursor, database_name)
    #
    # cursor.execute("USE {}".format(database_name))
    # createTables(cursor)

    # insertIntoDatabase(cursor, "data.txt")

    queries = loadQueries()

    try:
        cursor.execute("USE UFO")
    except mysql.connector.Error:
        print("Database does not exist. Please select option a.")
        print()

    partialQueryList = [0, 5, 6, 8, 9, 10, 11]

    alphabet = "bcdefghijklmnopqrstuvwxyz"
    user_option = getUserOption(alphabet)
    while user_option != "q":
        if user_option == "a":
            dropAndFill(cursor, database_name)
        else:
            option = alphabet.index(user_option)
            query = queries[alphabet.index(user_option)]
            if option not in partialQueryList:
                executeQueryAllAttributes(cursor, query, option)
            else:
                executePartialQuery(cursor, query, option)
        user_option = getUserOption(alphabet)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
