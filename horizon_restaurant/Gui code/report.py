# Author: Zahin Hussain, Student ID: 22016373
import tkinter as tkk
import tkinter as ttk
from tkinter import *
import tkinter as tk
from main import *
from orderManager import OrderViewer
from reservationViewer import ReservationViewer
from tableViewer import TableViewer
from tkcalendar import Calendar

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus.tables import TableStyle


def generate_sales():
    print("Working pdf")
    # Create a PDF document
    pdf = SimpleDocTemplate("table_example.pdf", pagesize=letter)
    # Create a table with data
    data = [['restaurant id', 'restaurant id', 'No reservation','City']]
    tempData = []
    for restaurant_obj in restaurant_list:
        tempData.clear()

        ri = restaurant_obj.get_restaurant_id()
        rn = restaurant_obj.get_restaurant_name()
        ci = select('restaurants', 'cityId', 'restaurantId=' + str(restaurant_obj.get_restaurant_id()))
        count = select_count('reservations', '', 'restaurantId=' + str(restaurant_obj.get_restaurant_id()))
        cityName = select('cities','cityName','cityId='+str(ci[0][0]))
       # print( str(restaurant_obj.get_restaurant_id()))
        print(str(cityName[0][0]))

        temp_data = [str(ri), str(rn), count[0][0],cityName[0][0]]
        data.append(temp_data)



    table = Table(data)

    # Style the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Build the PDF
    elements = [table]
    pdf.build(elements)

def generate_orders():
    print("Working pdf")
    # Create a PDF document
    pdf = SimpleDocTemplate("orders.pdf", pagesize=letter)
    # Create a table with data
    data = [['restaurant id', 'restaurant id', 'No orders','City']]
    tempData = []
    for restaurant_obj in restaurant_list:
        tempData.clear()

        ri = restaurant_obj.get_restaurant_id()
        rn = restaurant_obj.get_restaurant_name()
        ci = select('restaurants', 'cityId', 'restaurantId=' + str(restaurant_obj.get_restaurant_id()))
        count = select_count('orders', '', 'restaurantId=' + str(restaurant_obj.get_restaurant_id()))
        cityName = select('cities','cityName','cityId='+str(ci[0][0]))
       # print( str(restaurant_obj.get_restaurant_id()))
        print(str(cityName[0][0]))

        temp_data = [str(ri), str(rn), count[0][0],cityName[0][0]]
        data.append(temp_data)



    table = Table(data)

    # Style the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Build the PDF
    elements = [table]
    pdf.build(elements)



generate_orders()