# Authors: William Forber , Student ID: 22015706
# Lewis Quick , Student ID: 22016949
import copy
import datetime
import bcrypt
from dbFunctions import *
import tkinter.messagebox as tkm
from datetime import datetime, timedelta
import os
import subprocess
import pickle
import re

# defining file name to store the current user
FILE_NAME = "currentUser.pkl"
# defining object lists
restaurant_list = []
user_list = []
menu_dish_list = []
order_list = []
ingredient_list = []
menus_list = []
table_list = []
reservation_list = []
inventory_list = []
offer_list = []
# currently logged-in user
currentUser = None


# closing the current window and opening the main menu
def open_main_menu(app):
    initialize_objects(1)
    app.destroy()
    priv = currentUser.get_privilege()
    if priv == 0:
        os.system('python mainMenuAdmin.py')
    elif priv == 1:
        os.system('python ManagerMenu.py')
    else:
        os.system('python waiterMenu.py')


def open_order_manager(app):
    initialize_objects(1)
    app.destroy()
    os.system('python orderManager.py')


def open_add_order_gui(order_manager):
    # load current user from file as well as initialise the objects
    initialize_objects(1)
    # open new py file
    process = subprocess.Popen(['python', 'addOrder.py'])
    process.wait()
    order_manager.refresh()
    process.kill()


def close_window(app):
    app.destroy()
    os.remove(FILE_NAME)


# function logging out the user and returning back to the login screen
def logout(app):
    initialize_objects()
    global currentUser
    app.master.destroy()
    currentUser = None
    os.remove(FILE_NAME)
    os.system('python loginGUI.py')


def save_current_user():
    with open(FILE_NAME, 'wb') as file:
        pickle.dump(currentUser, file)


def load_current_user():
    with open(FILE_NAME, 'rb') as file:
        user = pickle.load(file)
        return user


def refresh_current_user():
    initialize_objects(1)
    user_id = currentUser.get_user_id()
    os.remove(FILE_NAME)
    login(user_id=user_id)


# function used to initialize all objects from the database
def initialize_objects(load=0):
    # resetting all the objects
    order_list.clear()
    menu_dish_list.clear()
    restaurant_list.clear()
    user_list.clear()
    ingredient_list.clear()
    menus_list.clear()
    reservation_list.clear()
    table_list.clear()
    inventory_list.clear()
    offer_list.clear()
    global currentUser
    admin_added = False
    # getting data from the database
    restaurants = select("restaurants")
    users = select("users")
    orders = select(table_name="orders")
    menus = select(table_name="menus")
    ingredients = select(table_name="ingredients")
    dishes = select(table_name="menudishes")
    dishes_to_orders = select(table_name="orders_to_menudishes")
    dishes_to_ingredients = select(table_name="menudishes_has_ingredients")
    tables = select(table_name="tables")
    reservations = select(table_name="reservations")
    inventories = select(table_name="inventories")
    offers = select(table_name="offers")
    # for every restaurant in database add a new restaurant object to list
    for restaurant in restaurants:
        restaurant_list.append(Restaurant(restaurant[0], restaurant[2]))
    for user in users:
        # for every user in database go through restaurants
        for restaurant in restaurant_list:
            # if the users restaurant id in database equals the restaurant object's id
            # then add that user to the list with the selected restaurant object
            if user[1] == restaurant.get_restaurant_id():
                user_list.append(User(user[0], user[2], user[3], user[4], user[5], restaurant))
            if user[2] == "Admin" and not admin_added:
                user_list.append(User(user[0], user[2], user[3], user[4], user[5], 0))
                admin_added = True

    for ingredient in ingredients:
        ingredient_list.append(Ingredient(ingredient[0], ingredient[2], ingredient[3]))

    for dish in dishes:
        ingredients_to_add = []
        for ingredient_db in dishes_to_ingredients:
            for ingredient in ingredient_list:
                if int(ingredient_db[1]) == ingredient.get_item_id() and ingredient_db[0] == dish[0]:
                    ingredients_to_add.append(ingredient)
        menu_dish_list.append(Menu_dish(dish[0], dish[1], ingredients_to_add, dish[3], dish[4]))

    order_dish_list = []
    # for every order clear the order dish list and find which menu dish objects belong to that order and
    # add order with the created order dish list
    for order in orders:
        order_dish_list = []
        for dish in dishes_to_orders:
            if order[0] == dish[0]:
                for menu_dish in menu_dish_list:
                    if menu_dish.get_dish_id() == dish[1]:
                        order_dish_list.append(menu_dish)
        order_list.append(Order(order[0], order_dish_list, order[2], order[3], order[4], order[5]))
    orders_to_restaurants = []
    # for every restaurant find orders belonging to that restaurant
    # construct a list of order objects and add them to that restaurant
    for r in restaurant_list:
        orders_to_restaurants.clear()
        for d in orders:
            if d[1] == r.get_restaurant_id():
                for o in order_list:
                    if o.get_order_id() == d[0]:
                        orders_to_restaurants.append(o)
        r.set_orders(copy.deepcopy(orders_to_restaurants))
    # if the load parameter is specified as one load the current user object
    # via the currentuser.pkl file
    if load == 1:
        try:
            currentUser = load_current_user()
        except:
            tkm.showerror("Not logged in", "You need to login first to view window!")
            return False
    # for every menu get the menu dishes belonging to that menu put them into a list and create the menu object
    for menu in menus:
        dishes_to_add = []
        for dish in dishes:
            if dish[2] == menu[0]:
                dish_id = dish[0]
                for d in menu_dish_list:
                    if d.get_dish_id() == dish_id:
                        dishes_to_add.append(d)
        menus_list.append(Menu(menu[0], dishes_to_add, menu[2]))
    # for every restaurant get the menus belonging to that restaurant
    # and add the list of menu objects to that restaurant object
    for restaurant in restaurant_list:
        menus_to_add = []
        for menu_db in menus:
            if int(menu_db[1]) == restaurant.get_restaurant_id():
                for menu in menus_list:
                    if menu.get_menu_id() == int(menu_db[0]):
                        menus_to_add.append(menu)
                        break
        restaurant.set_menus(menus_to_add)
    # for every table append a table object to the table_list
    for table in tables:
        table_list.append(Table(table[0], table[2]))

    for restaurant in restaurant_list:
        tables_to_add = []
        for table_db in tables:
            if table_db[1] == restaurant.get_restaurant_id():
                for table in table_list:
                    if table_db[0] == table.get_table_number():
                        tables_to_add.append(table)
        restaurant.set_tables(tables_to_add)

    # for every reservation make a table list for it and append it to the reservation object
    for reservation in reservations:
        tables_to_add = []
        for table in table_list:
            if table.get_table_number() == reservation[2]:
                tables_to_add.append(table)
        reservation_list.append(
            Reservation(reservation[0], reservation[3], reservation[4], tables_to_add[0], reservation[5]))

    # for every restaurant add a reservation list of every reservation belonging to that restaurant
    for restaurant in restaurant_list:
        reservations_to_add = []
        for reservation_db in reservations:
            if restaurant.get_restaurant_id() == reservation_db[1]:
                print("good")
                for reservation in reservation_list:
                    if reservation.get_reservation_ID() == reservation_db[0]:
                        reservations_to_add.append(reservation)
                        break
        restaurant.set_reservations(reservations_to_add)

    for inventory in inventories:
        ingredients_to_inventory = []
        for ingredient_db in ingredients:
            if int(ingredient_db[1]) == int(inventory[0]):
                for ingredient in ingredient_list:
                    if ingredient.get_item_id() == int(ingredient_db[0]):
                        ingredients_to_inventory.append(ingredient)
        inventory_list.append(Inventory(inventory[0], inventory[2], ingredients_to_inventory))
    for restaurant in restaurant_list:
        inventories_to_add = []
        for inventory_db in inventories:
            if restaurant.get_restaurant_id() == inventory_db[1]:
                for inventory in inventory_list:
                    if inventory.get_inventory_id() == int(inventory_db[0]):
                        inventories_to_add.append(inventory)
                        break
        restaurant.set_inventories(inventories_to_add)

    for offer in offers:
        offer_list.append(Offer(offer[0], offer[1], offer[2]))


class Offer:
    def __init__(self, offer_id, discount, menu_dish_id):
        self.offer_id = offer_id
        self.discount = discount
        self.menu_dish_id = menu_dish_id

    def get_offer_id(self):
        return self.offer_id

    def get_discount(self):
        return self.discount

    def get_menu_dish_id(self):
        return self.menu_dish_id

    def set_offer_id(self, off_id):
        self.offer_id = off_id

    def set_discount(self, discount):
        self.discount = discount

    def set_menu_dish_id(self, men_d_id):
        self.menu_dish_id = men_d_id


# defining restaurant class
class Restaurant:
    def __init__(self, restaurant_id, restaurant_name, orders=None, menus=None, tables=None, reservations=None,
                 inventories=None):
        self.__restaurant_ID = restaurant_id
        self.__restaurant_name = restaurant_name
        self.__orders = orders
        self.__menus = menus
        self.__tables = tables
        self.__reservations = reservations
        self.__inventories = inventories

    def get_restaurant_id(self):
        return self.__restaurant_ID

    def get_restaurant_name(self):
        return self.__restaurant_name

    def set_orders(self, orders):
        self.__orders = orders

    def get_orders(self):
        return self.__orders

    def set_menus(self, menus):
        self.__menus = menus

    def get_menus(self):
        return self.__menus

    def set_reservations(self, reservations):
        self.__reservations = reservations

    def get_reservations(self):
        return self.__reservations

    def set_tables(self, tables):
        self.__tables = tables

    def get_tables(self):
        return self.__tables

    def set_inventories(self, inventories):
        self.__inventories = inventories

    def get_inventories(self):
        return self.__inventories


# defining ingredient class
class Ingredient:
    def __init__(self, item_id, ing_name, quantity):
        self.__item_ID = item_id
        self.__ing_name = ing_name
        self.__quantity = quantity

    def get_item_id(self):
        return self.__item_ID

    def get_name(self):
        return self.__ing_name

    def get_quantity(self):
        return self.__quantity

    def set_name(self, new_name):
        self.__ing_name = new_name

    def increase_ingredient(self, num):
        self.__quantity += num

    def decrease_ingredient(self, num):
        self.__quantity -= num


class Menu:
    def __init__(self, menu_id, dishes, category):
        self.__menu_ID = menu_id
        self.__dishes = dishes
        self.__category = category

    def set_menu_id(self, menu_id):
        self.__menu_ID = menu_id

    def get_menu_id(self):
        return self.__menu_ID

    def set_dishes(self, dishes):
        self.__dishes = dishes

    def get_dishes(self):
        return self.__dishes

    def set_category(self, category):
        self.__category = category

    def get_category(self):
        return self.__category

    def add_dish(self, dish):
        self.__dishes.append(dish)

    def remove_dish(self, dish):
        self.__dishes.remove(dish)


# defining the menu dish class
class Menu_dish:
    def __init__(self, dish_id, dish_name, ingredients, price, time_to_cook):
        self.__dish_ID = dish_id
        self.__dish_name = dish_name
        self.__ingredients = ingredients
        self.__price = price
        self.__time_to_cook = time_to_cook

    def get_name(self):
        return self.__dish_name

    def get_dish_id(self):
        return self.__dish_ID

    def get_ingredients(self):
        return self.__ingredients

    def get_price(self):
        return self.__price

    def set_name(self, name):
        self.__dish_name = name

    def set_ingredients(self, ingredients):
        self.__ingredients = ingredients

    def set_price(self, price):
        self.__price = price

    def get_time_to_cook(self):
        return self.__time_to_cook

    def set_time_to_cook(self, time):
        self.__time_to_cook = time

    # def get_offer():


# defining the order class
class Order:
    def __init__(self, order_id, menu_dishes, order_price, order_start, order_estend, order_status):
        self.__order_ID = order_id
        self.__menu_dishes = menu_dishes
        self.__order_price = order_price
        self.__order_start = order_start
        self.__order_estend = order_estend
        self.__order_status = order_status

    def get_order_id(self):
        return self.__order_ID

    def get_dishes(self):
        return self.__menu_dishes

    def get_order_estend(self):
        return self.__order_estend

    def get_order_start(self):
        return self.__order_start

    def set_dish(self, dish):
        self.__menu_dishes.append(dish)

    def remove_dish(self, dish):
        self.__menu_dishes.remove(dish)

    def set_order_start(self, order_start):
        self.__order_start = order_start

    def set_order_end(self, order_end):
        self.__order_estend = order_end

    def set_order_price(self, price):
        self.__order_price = price

    def calculate_order_price(self):
        total = 0
        for dish in self.__menu_dishes:
            total += dish.get_price()
        return total

    def get_price(self):
        return self.__order_price

    def set_order_status(self, status):
        self.__order_status = status

    def get_order_status(self):
        return self.__order_status

    # def cancel_order(self):


# defining user class
class User:
    def __init__(self, user_id=None, user_name=None, passwd=None, level=None, salt=None, restaurant=None):
        self.__user_ID = user_id
        self.__user_name = user_name
        self.__password = passwd
        self.__privilege = level
        self.__salt = salt
        self.__restaurant = restaurant

    # setters and getters for attributes
    def get_user_id(self):
        return self.__user_ID

    def get_user_name(self):
        return self.__user_name

    def get_password(self):
        return self.__password

    def get_restaurant(self):
        return self.__restaurant

    def get_salt(self):
        return self.__salt

    def get_privilege(self):
        return self.__privilege

    def set_user_id(self, u_id):
        self.__user_ID = u_id

    def set_user_name(self, user_name):
        self.__user_name = user_name

    def set_password(self, new_password):
        self.__password = new_password

    def set_restaurant(self, restaurant):
        self.__restaurant = restaurant

    def set_privilege(self, new_privilege):
        self.__privilege = new_privilege

    def set_salt(self, salt):
        self.__salt = salt


class Reservation:

    # Constructor Declaration
    def __init__(self, reservation_ID, customer_name, time, table, num_people):
        self.__reservation_ID = reservation_ID
        self.__customer_name = customer_name
        self.__time = time
        self.__table = table
        self.__num_people = num_people

    # get methode for reservation_ID
    def get_reservation_ID(self):
        return self.__reservation_ID

    # set methode for reservation_ID
    def set_reservation_ID(self, reservation_ID):
        self.__reservation_ID = reservation_ID

    # get methode for customer_name
    def get_customer_name(self):
        return self.__customer_name

    # set methode for customer_name
    def set_customer_name(self, customer_name):
        self.__customer_name = customer_name

    # get methode for time
    def get_time(self):
        return self.__time

    # set methode for time
    def set_time(self, time):
        self.__time = time

    # get methode for num_people
    def get_num_people(self):
        return self.__num_people

    # set methode for num_people
    def set_num_people(self, num_people):
        self.__num_people = num_people

    def set_table(self, table):
        self.__table = table

    def get_table(self):
        return self.__table


'''
    def add_reservation(self):
    def cancel_reservation(self):
        print("F")
        
        '''


class Table:
    def __init__(self, table_number, capacity):
        self.__table_number = table_number
        self.__capacity = capacity

    def get_table_number(self):
        return self.__table_number

    def get_capacity(self):
        return self.__capacity

    def set_table_number(self, new_number):
        self.__table_number = new_number

    def set_capacity(self, new_capacity):
        self.__capacity = new_capacity


class Inventory:
    def __init__(self, inventory_id, inventory_name, ingredients=None):
        self.__inventory_id = inventory_id
        self.__inventory_name = inventory_name
        self.__ingredients = ingredients

    def get_inventory_id(self):
        return self.__inventory_id

    def get_inventory_name(self):
        return self.__inventory_name

    def add_ingredient(self):
        pass

    def remove_ingredient(self):
        pass

    def get_ingredients(self):
        return self.__ingredients


# function for logging in
def login(user_name=None, password=None, restaurant_id=None, app=0, user_id=None):
    # making sure current user is assigned correctly
    global currentUser
    user_to_login = None
    # for loop looking for the username inputted with the restaurant id
    # and assigning the userToLogin variable to that user object
    for user in user_list:
        if user_id is not None:
            if user.get_user_id() == user_id:
                currentUser = user
                user_to_login = user
                save_current_user()
                break
        if user_name == "Admin" and user.get_user_name() == user_name:
            user_to_login = user
            break
        if user.get_user_name() == "Admin":
            continue
        if user.get_restaurant().get_restaurant_id() == restaurant_id:
            if user.get_user_name() == user_name:
                user_to_login = user
                break
            else:
                continue
        else:
            continue
    # if no user to login is found then the user does not exist
    if user_to_login is None:
        tkm.showerror("Error", "User not found!")
    else:
        if user_id is not None:
            return True
        # checking if the password is correct
        password = password.encode('utf-8')
        salt = user_to_login.get_salt()
        salt = salt.encode('utf-8')
        salt = salt[2:len(salt) - 1]
        hashedpw = bcrypt.hashpw(password, salt)
        password_to_check = user_to_login.get_password()
        # converting the password to bytes for hashing
        password_to_check = password_to_check.encode('utf-8')
        password_to_check = password_to_check[2:len(password_to_check) - 1]
        if password_to_check == hashedpw:
            # if password is correct assign the current user to the selected user object
            currentUser = user_to_login
            save_current_user()
            open_main_menu(app)
            return True
        else:
            tkm.showerror("Failure", "Password incorrect!")
            return False


# function allowing for the creation of new accounts
def create_account(user_name, password, privilege):
    # checking if the logged-in user has permission to perform the request
    if currentUser.get_privilege() > 1:
        print("User does not have permission to add accounts")
        return False
    else:
        # generate a salt and hash the password
        salt = bcrypt.gensalt()
        password = password.encode('utf-8')
        hashedpw = bcrypt.hashpw(password, salt)
        # create a new user object and add it to the userList
        user_list.append(User(user_name=user_name, passwd=hashedpw, level=privilege, salt=salt,
                              resturant=currentUser.get_resturant()))
        user = (user_list[len(user_list) - 1])
        # add new user to the database
        insert("users (resturantId,userName,password,privilege,salt)",
               "(" + user.get_restaurant().get_restaurant_id() + "),(" + user.get_user_name() + "),(" + user.get_password() + "),(" + user.get_privilege() + "),(" + user.get_salt() + ");")
        initialize_objects()
        return True


# function for getting the user id to delete
def remove_account(user_name="", restaurant_id=0):
    # if the logged-in user is either a manager or higher than delete the desired username
    if currentUser.get_privilege() <= 1:
        user_id = select("users", "userId", "userName =" + user_name + " AND restaurantId = " + restaurant_id)
        # if logged-in user is a higher privilege than manager then use the restaurantId parameter
        user_id = user_id[0]
        delete("users", "userId = " + user_id)
        initialize_objects()
    else:
        # if logged-in user is not a manager or admin then delete the logged-in users account
        delete("users", "userId = " + currentUser.get_user_ID())


# function for changing the users password
def change_password(old_pswd, new_pswd, new_pswd2):
    current_user = load_current_user()
    old_pswd = old_pswd.get()
    new_pswd = new_pswd.get()
    new_pswd2 = new_pswd2.get()
    password = old_pswd
    password = password.encode('utf-8')
    salt = current_user.get_salt()
    salt = salt.encode('utf-8')
    salt = salt[2:len(salt) - 1]
    hashedpw = bcrypt.hashpw(password, salt)
    password_to_check = current_user.get_password()
    # converting the password to bytes for hashing
    password_to_check = password_to_check.encode('utf-8')
    password_to_check = password_to_check[2:len(password_to_check) - 1]
    if password_to_check != hashedpw:
        tkm.showerror("Old password incorrect", "The old password was not correct!")
        return False
    elif (str(new_pswd) != str(new_pswd2)):
        tkm.showerror("Passwords don't match", "The inputted passwords do not match!")
        return False
    else:
        passwd = new_pswd
        # generating salt and hashing the password
        salt = bcrypt.gensalt()
        passwd = passwd.encode('utf-8')
        hashedpw = bcrypt.hashpw(passwd, salt)
        hashedpw = str(hashedpw)
        salt = str(salt)
        try:
            # updating the users password
            update("users", f' password = "{hashedpw}",'
                            f'salt = "{salt}"',
                   f"userId = {currentUser.get_user_id()}")
        except Exception as e:
            tkm.showerror("Password not changed!", "The password was not changed! " + str(e))
            return False
        else:
            tkm.showinfo("Password Changed!", "The password was successfully changed!")
            return True


def list_restaurants(get_id=None, rest_name=None):
    # If no id or name is specified return all restaurants
    if get_id is None and rest_name is None:
        restaurant_names = []
        for restaurant in restaurant_list:
            restaurant_names.append(restaurant.get_restaurant_name())
        return restaurant_names
    elif not (get_id is None and rest_name is None):
        for restaurant in restaurant_list:
            if restaurant.get_restaurant_name() == rest_name:
                return restaurant.get_restaurant_id()
    else:
        print("invalid parameters!")


def find_dishes(dish_list):
    # gets the MenuDish objects from an inputted dish id list
    returned_list = []
    for dish in dish_list:
        for menuDish in menu_dish_list:
            if menuDish.get_name() == dish:
                returned_list.append(menuDish)
    return returned_list


def get_order_price(dish_list):
    # calculates the order price given the menu dish list
    total = 0.00
    for dish in dish_list:
        total += float(dish.get_price())
    return total


def find_order_time(dish_list):
    # calculates the estimated time for an order to be completed
    # by returning the menu dish with the longest time to cook
    max_time = 0
    for dish in dish_list:
        if dish.get_time_to_cook() > max_time:
            time_change = timedelta(minutes=dish.get_time_to_cook())
    return time_change


def decrement_ingredients(dish):
    # for every ingredient in the menu dish decrement their quantity by 1
    for ingredient in dish.get_ingredients():
        ing_id = ingredient.get_item_id()
        ing_name = ingredient.get_name()
        quantity = ingredient.get_quantity() - 1
        if quantity < 0:
            tkm.showerror("Stock not enough!", "There is insufficient stock to add this dish: " + dish.get_name())
            return False
        update_ingredient(ing_id, ing_name, quantity, True)
    return True


def add_order(menu_dishes):
    # getting the current time
    current_time = datetime.now()
    dishes_to_add = []
    # adding the dish id's selected in the gui to a list
    for i in menu_dishes.curselection():
        dishes_to_add.append(menu_dishes.get(i))
    # if no dishes are selected output an error message
    if not dishes_to_add:
        tkm.showerror("Dish not selected!", "Menu dish not selected!")
        return False
    # converting the list of dish id's into menu dish object list
    dish_list = find_dishes(dishes_to_add)
    # getting the time to cook
    time_change = find_order_time(dish_list)
    # getting the order price
    price = get_order_price(dish_list)
    # if no orders then set order id as 1
    if len(order_list) == 0:
        order_id = 1
    else:
        # set the order id to the length of the order list
        order_id = order_list[len(order_list) - 1].get_order_id() + 1
    # add the order to the list of order objects
    order_list.append(Order(order_id, dish_list, price, current_time, current_time + time_change, "preparing"))
    length = len(order_list) - 1
    # using the order list add the order to the database
    insert("orders", ["restaurantId", "orderPrice", "orderStart", "orderEstEnd", "orderStatus"], [
        str(currentUser.get_restaurant().get_restaurant_id()),
        str(order_list[length].get_price()),
        str(order_list[length].get_order_start()),
        str(order_list[length].get_order_estend()),
        order_list[length].get_order_status()
    ])
    initialize_objects()
    # using the order and menu dish lists add the order id mapping to the dish id to the database
    for dish in dish_list:
        insert("orders_to_menudishes", ["OrderId", "dishId"],
               [str(order_list[length].get_order_id()), str(dish.get_dish_id())])
        if decrement_ingredients(dish):
            pass
        else:
            order_in = [order_id]
            delete_order(order_in[0], True)
            return False
        # output a success message to the user and close the window
    tkm.showinfo("Successful added order", "Order added successfully!")


def update_order(order_in, price=None, time_placed=None, complete_time=None, status=None):
    # initialize the objects
    initialize_objects()
    order_id = int(order_in[0])
    order_to_update = None
    # if nothing is inputted show an error message
    if price == "" and time_placed == "" and complete_time == "" and status == "":
        tkm.showerror("No values to update!", "To update an order one or more values need to be inputted!")
        return False
    # for every order in the order list find the desired order to update and
    # set each attribute of the order
    for order in order_list:
        print(order.get_order_id())
        if order.get_order_id() == order_id:
            order.set_order_price(price)
            order.set_order_start(time_placed)
            order.set_order_end(complete_time)
            order.set_order_status(status)
            order_to_update = order
            break
    # update the orders table in the database with the new values
    try:
        update("orders", f" orderPrice = {order_to_update.get_price()}, "
                         f'orderStart = "{order_to_update.get_order_start()}",'
                         f'orderEstEnd = "{order_to_update.get_order_estend()}",'
                         f'orderStatus = "{order_to_update.get_order_status()}"',
               f"orderId = {order_to_update.get_order_id()}")
    # if there is an error show an error message
    except Exception as e:
        tkm.showerror("Order not updated!", str(e))
    # if no exception show an info message saying the order is successfully updated
    else:
        tkm.showinfo("Order updated", "Order successfully updated!")


# function for deleting orders
def delete_order(order_in, silence=False):
    order_id = int(order_in[0])
    # find the order to delete and delete that order from the order list
    for order in order_list:
        if order.get_order_id() == order_id:
            order_list.remove(order)
            break
    # deleting that order from the orders table in the database
    try:
        delete("orders", f"orderId = {order_id}")
    # if there is an error when deleting show an error message to the user
    except Exception as e:
        tkm.showerror("Failed to delete order:", "The order was not deleted: " + e)
        return False
    if not silence:
        tkm.showinfo("Order deleted:", "The order was deleted successfully")


def add_table(capacity):
    initialize_objects(1)
    table_number = len(table_list) + 1
    table_list.append(Table(table_number, capacity))
    table_to_add = table_list[len(table_list) - 1]
    try:
        insert("tables", ["restaurantId,capacity"], [str(currentUser.get_restaurant().get_restaurant_id()),
                                                     str(table_to_add.get_capacity())])
    except Exception as e:
        tkm.showerror("Table not inserted!", "Table was not added! " + str(e))
        return False
    else:
        tkm.showinfo("Table added!", "The table was added successfully!")
        initialize_objects()


def add_reservation(date, time, customer_name, num_people, table):
    initialize_objects(1)
    dateandtime = str(date) + ' ' + str(time) + ':00:00'
    for i in table.curselection():
        table = table.get(i)
    dateandtime = datetime.strptime(dateandtime, '%m/%d/%y %H:%M:%S')
    if not (isinstance(table, str)):
        tkm.showerror("Error creating reservation!", "All fields need to be inputted to add a reservation!")
        return False
    table_search = re.findall("[0-9]", table)
    table_num = ""
    for i in range(len(table_search)):
        table_num += str(table_search[i])
    table_num = int(table_num)
    table_to_add = []
    for table_obj in table_list:
        if table_obj.get_table_number() == table_num:
            table_to_add.append(table_obj)
    reservation_list.append(Reservation(len(reservation_list) + 1, customer_name, dateandtime, table_to_add[0],
                                        num_people))
    try:
        insert("reservations", ["restaurantId", "tableNumber", "customerName", "time", "numPeople"],
               [currentUser.get_restaurant().get_restaurant_id(),
                table_num, customer_name, dateandtime, num_people])
    except Exception as e:
        tkm.showerror("Failed to add reservation:", "The reservation was not added! " + str(e))
        return False
    else:
        tkm.showinfo("Reservation Added!", "The reservation was added successfully!")
        initialize_objects()


def update_reservation(customer_name, date, time, num_people, table_num, res_id):
    initialize_objects(1)
    res_id = int(res_id)
    table_num = int(table_num)
    print(table_num)
    dateandtime = str(date) + ' ' + str(time) + ':00:00'
    dateandtime = datetime.strptime(dateandtime, '%m/%d/%y %H:%M:%S')
    table_to_set = []
    for table in table_list:
        if table.get_table_number() == table_num:
            table_to_set.append(table)
            break
    for reservation in reservation_list:
        if reservation.get_reservation_ID() == res_id:
            reservation.set_customer_name(customer_name)
            reservation.set_time(dateandtime)
            reservation.set_num_people(num_people)
            reservation.set_table(table_to_set[0])
            try:
                update("reservations", f"restaurantId = {currentUser.get_restaurant().get_restaurant_id()}, "
                                       f"tableNumber = {reservation.get_table().get_table_number()},"
                                       f'customerName = "{reservation.get_customer_name()}",'
                                       f'time = "{reservation.get_time()}",'
                                       f"numPeople = {reservation.get_num_people()}",
                       f"reservationId = {reservation.get_reservation_ID()}")
            except Exception as e:
                tkm.showerror("Reservation Failed to update!", "Reservation update failed " + str(e))
                break
            else:
                tkm.showinfo("Successfully Updated Reservation!", "The reservation was successfully updated!")
                initialize_objects()
            finally:
                break


def delete_reservation(reservation_details):
    reservation_id = int(reservation_details[0])
    for reservation in reservation_list:
        if reservation.get_reservation_ID() == reservation_id:
            reservation_list.remove(reservation)
            break
    try:
        delete("reservations", "reservationId = " + str(reservation_id))
    except Exception as e:
        tkm.showerror("Error deleting reservation", "An error occurred while deleting the reservation! " + str(e))
    else:
        tkm.showinfo("Reservation Deleted!", "The reservation was deleted successfully!")


def update_table(table_details, capacity):
    table_num = int(table_details[0])
    for table in table_list:
        if table.get_table_number() == table_num:
            table.set_capacity(int(capacity))
            break
    try:
        update("tables", f"capacity = {int(capacity)}", f"tableNumber = {table_num}")
    except Exception as e:
        tkm.showerror("Update failure", "Failed to update that table!" + str(e))
    else:
        tkm.showinfo("Update success!", "Table updated successfully")


def delete_table(table_num):
    table_num = int(table_num)
    for table in table_list:
        if table.get_table_number() == table_num:
            table_list.remove(table)
            break
    try:
        delete("tables", f"tableNumber = {table_num}")
    except Exception as e:
        tkm.showerror("Failed to delete table!", "The table was not deleted! " + str(e))
    else:
        tkm.showinfo("Delete successful!", "The table was deleted successfully!")


def check_input(num, is_float=False):
    if not is_float:
        try:
            int(num)
        except ValueError:
            return False
        else:
            return True
    else:
        try:
            float(num)
        except ValueError:
            return False
        else:
            return True


def search_ingredients(inv_id, stock_name):
    initialize_objects(1)
    for inventory in currentUser.get_restaurant().get_inventories():
        if inventory.get_inventory_id() == inv_id:
            for ingredient in inventory.get_ingredients():
                if ingredient.get_name() == stock_name:
                    return ingredient

        return False


def add_inventory(inventory_name):
    inventory_list.append(Inventory(len(inventory_list) + 1, inventory_name))
    try:
        insert("inventories", ["inventoryName", "restaurantId"],
               [inventory_name, currentUser.get_restaurant().get_restaurant_id()])

    except Exception as e:
        tkm.showerror("Failed to add inventory!", "The inventory was not added! " + str(e))
    else:
        tkm.showinfo("Inventory added!", "The inventory was added successfully!")


def add_ingredient(inv_id, ing_name, quantity):
    ingredient_list.append(Ingredient(len(ingredient_list) + 1, ing_name, quantity))
    try:
        insert("ingredients", ["inventoryId", "ingName", "quantity"], [inv_id, ing_name, quantity])
    except Exception as e:
        tkm.showerror("Failed to add ingredient!", "The ingredient was not added " + str(e))
    else:
        tkm.showinfo("Added Ingredient", "The ingredient was added successfully!")


def update_ingredient(ing_id, ing_name, quantity, silence=False):
    try:
        update("ingredients", f' ingName = "{ing_name}",'
                              f" quantity = {quantity}", f"itemId = {ing_id}")
    except Exception as e:
        tkm.showerror("Failed to update!", "The ingredient failed to update! " + str(e))
        return False
    if not silence:
        tkm.showinfo("Update successful!", "The ingredient was updated successfully!")


def delete_ingredient(ing_name):
    initialize_objects(1)
    for inventory in currentUser.get_restaurant().get_inventories():
        for ingredient in inventory.get_ingredients():
            if ingredient.get_name() == ing_name:
                try:
                    delete("ingredients", f" itemId = {ingredient.get_item_id()}")
                except Exception as e:
                    tkm.showerror("Failed to delete", "The ingredient was not deleted! " + str(e))
                    break
                else:
                    tkm.showinfo("Delete Successful", "The ingredient was deleted successfully!")
                    break


def check_stock(inv_id, stock_name=None):
    initialize_objects(1)
    low_stock = []
    if stock_name is None:
        for inventory in currentUser.get_restaurant().get_inventories():
            if inventory.get_inventory_id() == int(inv_id):
                for ingredient in inventory.get_ingredients():
                    if ingredient.get_quantity() <= 4:
                        low_stock.append(ingredient)
        if len(low_stock) == 0:
            tkm.showinfo("No low stock", "There are currently no items that are low on stock!")
            return False
        return low_stock
    else:
        for inventory in currentUser.get_restaurant().get_inventories():
            if inventory.get_inventory_id() == int(inv_id):
                for ingredient in inventory.get_ingredients():
                    if ingredient.get_name() == stock_name:
                        if ingredient.get_quantity() <= 4:
                            tkm.showinfo("Stock Low!",
                                         "The stock for " + stock_name + " is low! The quantity is: " + str(
                                             ingredient.get_quantity()) + " consider re-ordering!")
                        else:
                            tkm.showinfo("Stock Ok!", "The stock for " + stock_name + " is ok! The quantity is: " + str(
                                ingredient.get_quantity()))
                        break
        return False


def add_dish(dish_name, menu_id, price, time, ingredients):
    initialize_objects(1)
    ingredient_selection = []
    ingredient_ids = []
    dish_to_get = []
    for i in ingredients.curselection():
        ingredient_selection.append(ingredients.get(i))

    for inventory in currentUser.get_restaurant().get_inventories():
        for ingredient in inventory.get_ingredients():
            for selection in ingredient_selection:
                if ingredient.get_name() == selection:
                    ingredient_ids.append(ingredient.get_item_id())
    try:
        insert("menudishes", ["dishName", "menuId", "price", "timeToCook"], [dish_name, menu_id, price, time])
    except Exception as e:
        tkm.showerror("Failed to add dish!", "The dish was not added! " + str(e))
        return False
    refresh_current_user()
    initialize_objects(1)
    for menu in currentUser.get_restaurant().get_menus():
        if menu.get_menu_id() == int(menu_id):
            for dish in menu.get_dishes():
                dish_to_get.clear()
                dish_to_get.append(dish)
            break
    dish_id = dish_to_get[0].get_dish_id()
    print("Dish id: " + str(dish_id))
    try:
        for id in ingredient_ids:
            insert("menudishes_has_ingredients", ["dishId", "itemId"], [dish_id, id])
    except Exception as e:
        tkm.showerror("Failed to add dish!", "The dish was not added! " + str(e))
        return False

    tkm.showinfo("Add successful!", "The dish was added successfully!")


def remove_dish(dish_id):
    try:
        delete("menudishes", f"dishId = {dish_id}")
    except Exception as e:
        tkm.showerror("Failed to remove dish!", "The dish was not removed! " + str(e))
    else:
        tkm.showinfo("Removal successful!", "The dish was removed successfully!")


def set_menu_category(menu_id, category):
    try:
        update("menus", f'category = "{category}"', f"menuId = {menu_id}")
    except Exception as e:
        tkm.showerror("Failed to update category!", "The category was not updated! " + str(e))
    else:
        tkm.showinfo("Update Successful!", "The category was updated successfully!")


def create_menu(category):
    initialize_objects(1)
    try:
        insert("menus", ["restaurantId", "category"], [currentUser.get_restaurant().get_restaurant_id(), category])
    except Exception as e:
        tkm.showerror("Failed to add menu!", "The menu was not added! " + str(e))
    else:
        tkm.showinfo("Add successful!", "The menu was added successfully!")


def create_offer(discount, menu_dish):
    initialize_objects(1)
    x = 1
    for i in menu_dish_list:
        x += i

    try:
        insert("offers", ["offerId", "discount", "MenuDishes_dishId"], [x, discount, menu_dish])
    except Exception as e:
        tkm.showerror("Failed to add offer!", "The offer was not added! " + str(e))
    else:
        tkm.showinfo("Add successful!", "The offer was added successfully!")


def remove_menu(menu_id):
    try:
        delete("menus", f"menuId = {menu_id}")
    except Exception as e:
        tkm.showerror("Failed to delete menu!", "The menu was not deleted! " + str(e))
    else:
        tkm.showinfo("Delete successful!", "The menu was deleted successfully!")


def remove_offer(offer_id):
    try:
        delete("offers", f"offerId = {offer_id}")
    except Exception as e:
        tkm.showerror("Failed to delete offer!", "The offer was not deleted! " + str(e))
    else:
        tkm.showinfo("Offer successful!", "The offer was deleted successfully!")


def set_username(user, newusername):
    user.set_user_name(newusername)
    for i in user_list:
        if i.get_id() == user.get_id():
            user_id = i.get_id()
            break
    try:
        update("users", f"user_name = {newusername}", f"userID = {user_id}")
    except Exception as e:
        tkm.showerror("Failed to change username!", "The username was not changed! " + str(e))
    else:
        tkm.showinfo("Change successful!", "The username was changed successfully!")


def set_password(user, password):
    user.set_password(password)
    for i in user_list:
        if i.get_id() == user.get_id():
            user_id = i.get_id()
            break
    try:
        update("users", f"password = {password}", f"userID = {user_id}")
    except Exception as e:
        tkm.showerror("Failed to change password!", "The password was not changed! " + str(e))
    else:
        tkm.showinfo("Change successful!", "The password was changed successfully!")


def set_privilege(user, privilege):
    user.set_privilege(privilege)
    for i in user_list:
        if i.get_id() == user.get_id():
            user_id = i.get_id()
            break
    try:
        update("users", f"privilege = {privilege}", f"userID = {user_id}")
    except Exception as e:
        tkm.showerror("Failed to change privilege!", "The privilege was not changed! " + str(e))
    else:
        tkm.showinfo("Change successful!", "The password was changed successfully!")


def set_restaurant(user, restaurant_name):
    for i in user_list:
        if i.get_id() == user.get_id():
            user_id = i.get_id()
            break

    for i in restaurant_list:
        if i.get_restaurant_name() == restaurant_name:
            rest = i
            rest_id = i.get_id()
            break

    user.set_restaurant(rest)

    try:
        update("users", f"restaurantId = {rest_id}", f"userID = {user_id}")
    except Exception as e:
        tkm.showerror("Failed to change restaurant!", "The restaurant was not changed! " + str(e))
    else:
        tkm.showinfo("Change successful!", "The restaurant was changed successfully!")


def create_user(user, pswd, priv, rest_name):
    for i in restaurant_list:
        if i.get_restaurant_name() == rest_name:
            rest_id = i.get_id()
            break
    salt = bcrypt.gensalt()
    pswd = pswd.encode('utf-8')
    pswd = bcrypt.hashpw(pswd, salt)
    x = 0
    for i in user_list:
        if i.get_id() > x:
            x = i
    x += 1
    new_user = User(x, pswd, priv, salt, rest_id)
    user_list.append(new_user)
    try:
        insert("users", "(userId, restaurantId, userName, password, privilege, salt)",
               (x, rest_id, user, pswd, priv, salt))
    except Exception as e:
        tkm.showerror("Failed to add user!", "The user was not added! " + str(e))
    else:
        tkm.showinfo("Add successful!", "The user was added successfully!")


def delete_inventory(inv_name):
    initialize_objects(1)
    inv_id = []
    for inventory in currentUser.get_restaurant().get_inventories():
        if inventory.get_inventory_name() == inv_name:
            inv_id.append(inventory.get_inventory_id())
            break
    try:
        delete("inventories", f"inventoryId = {inv_id[0]}")
    except Exception as e:
        tkm.showerror("Delete Failed!", "The inventory was not deleted! " + str(e))
        return False
    tkm.showinfo("Delete Success!", "The inventory was deleted successfully!")
