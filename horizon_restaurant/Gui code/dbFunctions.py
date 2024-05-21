# Author: William Forber, Student ID: 22015706
import tkinter.messagebox as tkm
import mysql.connector
from mysql.connector import errorcode

DATABASE_NAME = "horizonrestaurants"
HOST_ADDRESS = "localhost"
USERNAME = "root"
# change this to your root password for your DBMS (MySql)
PASSWD = "root"


# connecting to the database
def connect_to_database():
    try:
        conn = mysql.connector.connect(host=HOST_ADDRESS,
                                       user=USERNAME,
                                       password=PASSWD,
                                       database=DATABASE_NAME)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("User name and password incorrect")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("database name invalid")
        else:
            print(err)
    else:
        if conn is None:
            print("Connection not established")
        else:
            return conn


# select function used to operate the select sql query
def select(table_name, operator="*", where=None):
    conn = connect_to_database()
    try:
        dbcursor = conn.cursor()
    except:
        tkm.showerror(
            "Connection error!", "Unable to connect to the database; please check credentials!"
        )
    else:
        if where is None:
            statement = "SELECT {} FROM {};".format(operator, table_name)
        else:
            # formatting function parameters into sql query
            statement = "SELECT {} FROM {} WHERE {};".format(operator, table_name, where)
        dbcursor.execute(statement)
        result = dbcursor.fetchall()
        return result


# select count

def select_count(table_name, operator="*", where=None):
    conn = connect_to_database()
    try:
        dbcursor = conn.cursor()
    except:
        tkm.showerror(
            "Connection error!", "Unable to connect to the database; please check credentials!"
        )
    else:
        if where is None:
            statement = "SELECT COUNT(*) {} FROM {};".format(operator, table_name)
        else:
            # formatting function parameters into sql query
            statement = "SELECT COUNT(*) FROM {} WHERE {};".format(table_name, where)
        dbcursor.execute(statement)
        result = dbcursor.fetchall()
        #   print(result[0][0])
        return result


def update(table_name, set, where):
    conn = connect_to_database()
    # Checking to see if the connection was successful and if not output an error message
    try:
        dbcursor = conn.cursor()
    except Exception as e:
        tkm.showerror("Connection error!", f"Unable to connect to the database; {e}")
        return False
    else:
        if not dbcursor:
            return False
        statement = f"UPDATE {table_name} SET {set} WHERE {where};"
        try:
            dbcursor.execute(statement)
            conn.commit()
        except Exception as e:
            tkm.showerror("Error", f"Error inserting record; {e}")
        finally:
            dbcursor.close()
            conn.close()


def insert(table_name, columns, values):
    conn = connect_to_database()
    # Checking to see if the connection was successful and if not output an error message
    try:
        dbcursor = conn.cursor()
    except Exception as e:
        tkm.showerror("Connection error!", f"Unable to connect to the database; {e}")
        return False
    else:
        if not dbcursor:
            return False
        placeholders = ', '.join(['%s'] * len(values))
        statement = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        try:
            dbcursor.execute(statement, values)
            conn.commit()
        except Exception as e:
            tkm.showerror("Error", f"Error inserting record; {e}")
        finally:
            dbcursor.close()
            conn.close()


# Example usage


# select function used to operate the delete sql query
def delete(table_name, where):
    conn = connect_to_database()
    # checking to see if the connection was successful and if not output an error message
    try:
        dbcursor = conn.cursor()
    except:
        tkm.showerror(
            "Connection error!", "Unable to connect to the database; please check credentials!"
        )
    if not dbcursor:
        return False
    # formatting function parameters into sql query
    statement = "DELETE FROM {} WHERE {}".format(table_name, where)
    dbcursor.execute(statement)
    conn.commit()
    result = dbcursor.fetchall()
    return result
