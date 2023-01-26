# Tkinter Libraries
from tkinter import Menu
import tkinter as tk
from tkinter import ttk
import tkinter.ttk
from tkinter import messagebox
import tkinter.font as font

# Graph Libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# File handling Libraries
from hashtable import *
import csv

# Logging Libraries
import logging

# Other Libraries
import ast
import sys
import os

# Loging setup
global logger

logging.basicConfig(
    filename='./logs/main.log',
    level=logging.INFO,
    format=
    '%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s'
)

logger = logging.getLogger(__name__)


# Insert Frame
class Insert_Frame(ttk.LabelFrame):
    """
    https://www.youtube.com/watch?v=Fot3_9eDmOs
    
    Classes by defult create dynamic dictionaries to assign attributes to.
    Slots reduce the memory used to dynamically assign the attributes as they tell python to assign a static amount of memory to the attributes listed.
    """

    __slots__ = "stock_table"

    def __init__(self, container, stock_table):
        super().__init__(container)
        
        self.stock_table = stock_table

        self.result = ""

        self['text'] = 'Insert New Products'

        # Field options
        options = {'padx': 5, 'pady': 5}

        # Product label
        self.product_text_label = ttk.Label(self, text="Product:")
        self.product_text_label.grid(column=0, row=0, sticky='w', **options)

        # Product entry
        self.product = tk.StringVar()
        self.product_entry = ttk.Entry(self, textvariable=self.product)
        self.product_entry.grid(column=1, row=0, sticky='w', **options)
        self.product_entry.focus()

        # Stock label
        self.stock_text_label = ttk.Label(self, text="Stock:")
        self.stock_text_label.grid(column=0, row=1, sticky='w', **options)

        # Stock entry
        self.stock = tk.StringVar()
        self.stock_entry = ttk.Entry(self, textvariable=self.stock)
        self.stock_entry.grid(column=1, row=1, sticky='w', **options)
        self.stock_entry.focus()

        # Due date label
        self.due_date_text_label = ttk.Label(self, text="Due Date:")
        self.due_date_text_label.grid(column=0, row=2, sticky='w', **options)

        # Due date entry
        self.due_date = tk.StringVar()
        self.due_date_entry = ttk.Entry(self, textvariable=self.due_date)
        self.due_date_entry.grid(column=1, row=2, sticky='w', **options)
        self.due_date_entry.focus()

        # Cost label
        self.cost_text_label = ttk.Label(self, text="Cost per Unit (£):")
        self.cost_text_label.grid(column=0, row=3, sticky='w', **options)

        # Cost entry
        self.cost = tk.StringVar()
        self.cost_entry = ttk.Entry(self, textvariable=self.cost)
        self.cost_entry.grid(column=1, row=3, sticky='w', **options)
        self.cost_entry.focus()

        # Insert button
        self.insert_button = ttk.Button(self, cursor="mouse", text='Insert')
        self.insert_button.grid(column=0, row=4, sticky='w', **options)
        self.insert_button.configure(command=self.insert)

        # Result label
        self.result_label = ttk.Label(self)
        self.result_label.grid(row=4, column=1, columnspan=3, **options)

        # Add padding to the frame and show it
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def insert(self):
        # Attempts to insert data
        try:
            end = False
            try:
                # Fetches the data from the data entry areas
                product = self.product.get()
                stock = int(self.stock.get())
                due_date = self.due_date.get()
                temp_cost = self.cost.get()
                cost = float(temp_cost)

                if product == "":
                    raise ValueError('Attempted search for nothing')

            except ValueError as Verr:
                logger.warning(Verr, exc_info=True)
                messagebox.showerror("Error", "Can't insert nothing")
                end = True

            if end == True:
                pass
            elif end == False:

                # Saves the data to a txt file so that it can be loaded back automatically when the hashtable is stoped and then run again
                Save_Dictionary(product, stock, due_date, cost)

                # Preps the data to be loaded into the hashtable
                ED = Load_Dictionary(product)

                # Loads the dictionary
                dict = ED.send_dictionary()

                # Inserts the dictionary
                self.result = self.stock_table.insert(dict)

                # Logs what the user has inserted
                logger.info(f'User has inserted {product}')

                # Updates the result label
                self.result_label.config(text=self.result)

        # Exception that logs the error to a log file
        except Exception as err:
            logger.critical(err, exc_info=True)
            messagebox.showerror("Error", "Error inserting data")


# Search Frame
class Search_Frame(ttk.LabelFrame):

    __slots__ = "stock_table"

    def __init__(self, container, stock_table):
        super().__init__(container)

        self.stock_table = stock_table

        self['text'] = 'Search Existing Products'

        # Field options
        options = {'padx': 5, 'pady': 5}

        # Product label
        self.product_text_label = ttk.Label(self, text="Product:")
        self.product_text_label.grid(column=0, row=0, sticky='w', **options)

        # Product entry
        self.product = tk.StringVar()
        self.product_entry = ttk.Entry(self, textvariable=self.product)
        self.product_entry.grid(column=1, row=0, sticky='w', **options)
        self.product_entry.focus()

        # Search button
        self.search_button = ttk.Button(self, cursor="mouse", text='Search')
        self.search_button.grid(column=0, row=1, sticky='w', **options)
        self.search_button.configure(command=self.search)

        # Stock label
        self.stock_text_label = ttk.Label(self, text="Stock:")
        self.stock_text_label.grid(row=2, column=0, sticky='w', **options)

        # Stock result label
        self.stock_result_label = ttk.Label(self)
        self.stock_result_label.grid(row=2, column=1, columnspan=3, **options)

        # Due date label
        self.due_date_text_label = ttk.Label(self, text="Due Date:")
        self.due_date_text_label.grid(row=3, column=0, sticky='w', **options)

        # Due date result label
        self.due_date_result_label = ttk.Label(self)
        self.due_date_result_label.grid(row=3, column=1, columnspan=3, **options)

        # Cost label
        self.due_date_text_label = ttk.Label(self, text="Cost per Unit (£):")
        self.due_date_text_label.grid(row=4, column=0, sticky='w', **options)

        # Cost result label
        self.cost_result_label = ttk.Label(self)
        self.cost_result_label.grid(row=4, column=1, columnspan=3, **options)

        # Add padding to the frame and show it
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def search(self):

        # Attempts to search for data
        try:

            end = False

            try:
                # Fetches the data from manual data entry
                product = self.product.get()

                if product == "":
                    raise ValueError('Attempted search for nothing')

            except ValueError as Verr:
                logger.warning(Verr, exc_info=True)
                messagebox.showerror("Error", "Can't insert nothing")
                end = True

            if end == True:
                pass

            elif end == False:

                # Logs what the user has searched for
                logger.info(f'User searched for {product}')

                # Searches for the product
                result = self.stock_table.search(product)

                # Assigns the data to variables
                self.stock_results = result['Stock']
                self.due_date_results = result['Due Date']
                self.cost_results = result['Cost']

                # Displays the data on the GUI
                self.stock_result_label.config(text=self.stock_results)
                self.due_date_result_label.config(text=self.due_date_results)
                self.cost_result_label.config(text=self.cost_results)

        # Exception that logs the error to a log file
        except Exception as err:
            logger.critical(err, exc_info=True)
            messagebox.showerror("Error", "Error finding data")


class Edit_Frame(ttk.LabelFrame):
    
    """
    There are no slots in this class as it proved 13.0179% faster without them 
    Where as everywhere else it was faster with the slots
    """

    def __init__(self, container, stock_table):
        super().__init__(container)

        self.stock_table = stock_table

        self['text'] = 'Edit Existing Products'

        # Field options
        options = {'padx': 5, 'pady': 5}

        # Product label
        self.product_text_label_1 = ttk.Label(self, text="Product:")
        self.product_text_label_1.grid(column=0, row=0, sticky='w', **options)

        # Product entry
        self.product_1 = tk.StringVar()
        self.product_entry_1 = ttk.Entry(self, textvariable=self.product_1)
        self.product_entry_1.grid(column=1, row=0, sticky='w', **options)
        self.product_entry_1.focus()

        # Search button
        self.search_button = ttk.Button(self, cursor="mouse", text='Search')
        self.search_button.grid(column=0, row=1, sticky='w', **options)
        self.search_button.configure(command=self.search)

        # Product label
        self.product_text_label = ttk.Label(self, text="Product:")
        self.product_text_label.grid(column=0, row=2, sticky='w', **options)

        # Product entry
        self.product = tk.StringVar()
        self.product_entry = ttk.Entry(self, textvariable=self.product)
        self.product_entry.grid(column=1, row=2, sticky='w', **options)
        self.product_entry.focus()

        # Stock label
        self.stock_text_label = ttk.Label(self, text="Stock:")
        self.stock_text_label.grid(column=0, row=3, sticky='w', **options)

        # Stock entry
        self.stock = tk.StringVar()
        self.stock_entry = ttk.Entry(self, textvariable=self.stock)
        self.stock_entry.grid(column=1, row=3, sticky='w', **options)
        self.stock_entry.focus()

        # Due date label
        self.due_date_text_label = ttk.Label(self, text="Due Date:")
        self.due_date_text_label.grid(column=0, row=4, sticky='w', **options)

        # Due date entry
        self.due_date = tk.StringVar()
        self.due_date_entry = ttk.Entry(self, textvariable=self.due_date)
        self.due_date_entry.grid(column=1, row=4, sticky='w', **options)
        self.due_date_entry.focus()

        # Cost label
        self.cost_text_label = ttk.Label(self, text="Cost per Unit (£):")
        self.cost_text_label.grid(column=0, row=5, sticky='w', **options)

        # Cost entry
        self.cost = tk.StringVar()
        self.cost_entry = ttk.Entry(self, textvariable=self.cost)
        self.cost_entry.grid(column=1, row=5, sticky='w', **options)
        self.cost_entry.focus()

        # Update button
        self.update_button = ttk.Button(self, cursor="mouse", text='Update')
        self.update_button.grid(column=0, row=6, sticky='w', **options)
        self.update_button.configure(command=self.update)

        # Result label
        self.result_label = ttk.Label(self)
        self.result_label.grid(row=6, column=1, columnspan=3, **options)

        # Field options
        options = {'padx': 5, 'pady': 5}

        # Add padding to the frame and show it
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def search(self):
        # Attempts to search for data
        try:
            end = False
            try:
                product = self.product_1.get()
                if product == "":
                    raise ValueError('Attempted search for nothing')

            except ValueError as Verr:
                logger.warning(Verr, exc_info=True)
                messagebox.showerror("Error", "Can't insert nothing")
                end = True

            if end == True:
                pass

            # Searches for the product
            elif end == False:

                # Logs what the user searched for
                logger.info(f'User searched for {product}')

                # Gets the result from the search
                result = self.stock_table.search(product)

                # Extracts the data from that location
                self.Lproduct = result['Product']
                self.Lstock = result['Stock']
                self.Ldue_date = result['Due Date']
                self.Lcost = result['Cost']

                # Removes any data previously in the data entry points
                self.product_entry.delete(0, -1)
                self.stock_entry.delete(0, -1)
                self.due_date_entry.delete(0, -1)

                # Adds the data to the entry points so that it can be editted
                self.product_entry.insert(0, self.Lproduct)
                self.stock_entry.insert(0, self.Lstock)
                self.due_date_entry.insert(0, self.Ldue_date)
                self.cost_entry.insert(0, self.Lcost)

        # Exception that logs the error to a log file
        except Exception as err:
            logger.critical(err, exc_info=True)
            messagebox.showerror("Error", "Error searching for data")

    def update(self):
        # Attempts to update the data
        try:
            end_1 = False
            end_2 = False
            try:
                # Fetches the data
                product = self.product_entry_1.get()
                if product == "":
                    raise ValueError('Attempted search for nothing')
            except ValueError as Verr:
                logger.warning(Verr, exc_info=True)
                messagebox.showerror("Error", "Can't search nothing")
                end_1 = True

            if end_1 == True:
                pass

            elif end_1 == False:
                try:
                    temp_product = self.product_entry.get()

                    if temp_product == "":
                        raise ValueError('Attempted search for nothing')

                except ValueError as Verr:
                    logger.warning(Verr, exc_info=True)
                    messagebox.showerror("Error", "Can't insert nothing")
                    end_2 = True

                if end_2 == True:
                    pass
                elif end_2 == False:
                    flt_cost = float(self.cost_entry.get())

                    # Saves the updated data to a local dictionary
                    data = {
                        'Product': self.product_entry.get(),
                        'Stock': self.stock_entry.get(),
                        'Due Date': self.due_date_entry.get(),
                        'Cost': flt_cost
                    }

                    # Appends the data to the hashtable
                    result = self.stock_table.append(data, product)

                    # Loads ths file with the old data
                    ED = Load_Dictionary(product)

                    # Updates the file to contain the new data
                    LD = ED.edit(data)

                    # Logs the update in data
                    logger.info(f'User updated {product}')

                    # Updates the result label
                    self.result_label.config(text=result)

        # Exception that logs the error to a log file
        except Exception as err:
            logger.critical(err, exc_info=True)
            messagebox.showerror("Error", "Error updating data")


class Graph_Frame(ttk.LabelFrame):

    """
    There are no slots in this class as it proved 27.0707% faster without them 
    Where as everywhere else it was faster with the slots
    """

    def __init__(self, container, stock_table):
        super().__init__(container)

        # Loads the stock table
        self.stock_table = stock_table

        self.files = []
        self.names = []
        self.prices = []

        self.result = ""

        self['text'] = 'Price Changes'

        try:

            # Fetches all the products from the Stock dir
            self.files = [
                x for x in os.listdir("./Stock/") if x.endswith(".txt")
            ]

            #Extract ths data from the file steched
            for file in self.files:
                with open(f"./Stock/{file}", "r") as file:
                    contents = file.read()
                    pre_load_data = ast.literal_eval(contents)
                    temp_name = pre_load_data['Product']
                    temp_price = pre_load_data['Cost']

                    self.names.append(temp_name)
                    self.prices.append(temp_price)

        except Exception as err:
            logger.critical(err, exc_info=True)
            messagebox.showerror("Error", "Error checking stock")

        # Sets the dictionary to hold the values

        data = {'Product': [], 'Price': []}

        # Adds the data to the dictionary

        data['Product'] = self.names
        data['Price'] = self.prices

        # Turns the dictionary into a dataframe which Matolib can read

        df1 = pd.DataFrame(data)

        # Plots the graph
        try:
            figure = plt.Figure(figsize=(6, 7), dpi=100)
            ax = figure.add_subplot(111)
            chart_type = FigureCanvasTkAgg(figure, self)
            chart_type.get_tk_widget().pack()
            df1 = df1[['Product', 'Price']].groupby('Product').sum()
            df1.plot(kind='bar',
                     legend=True,
                     ax=ax,
                     color='#1ac6ff',
                     width=0.5,
                     align='center')
            ax.set_title('Price Comparison')
        
        except Exception as err:
            logger.critical(err, exc_info=True)
            messagebox.showerror("Error", "Error plotting graph")


class Customer_Orders_Frame(ttk.LabelFrame):

    __slots__ = "stock_table"

    def __init__(self, container, stock_table):
        super().__init__(container)

        self.stock_table = stock_table

        self['text'] = 'Customer Orders'

        # Field options
        options = {'padx': 5, 'pady': 5}

        # Define columns
        columns = ('Order_ID', 'Name', 'Email', 'Product', 'Amount_Ordered',
                   'Price')

        tree = ttk.Treeview(self, columns=columns, show='headings')

        # Define headings
        tree.heading('Order_ID', text='Order ID')
        tree.heading('Name', text='Name')
        tree.heading('Email', text='Email')
        tree.heading('Product', text='Product')
        tree.heading('Amount_Ordered', text='Amount Ordered')
        tree.heading('Price', text='Price')

        try:
            with open('Orders.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    tree.insert('', tk.END, values=row)

            logger.info('Data successfully read from csv file')

        except Exception as err:
            logger.critical(err, exc_info=True)
            messagebox.showerror("Error", "Error traversing the database")

        tree.bind('<<TreeviewSelect>>')

        tree.grid(row=0, column=0, sticky='nsew', **options)

        # Add padding to the frame and show it
        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")


class App(tk.Tk):

    __slots__ = "stock_table"

    def __init__(self, stock_table):

        super().__init__()

        self.stock_table = stock_table

        # Sets Title
        self.title('Stock Management System')
        # Sets Window Size
        self.geometry('310x180')

        menubar = Menu(self)
        self.config(menu=menubar)

        # Create a menu
        options_menu = Menu(menubar)
        # Creates 3 submenus
        insert_sub = Menu(options_menu)
        search_sub = Menu(options_menu)
        update_sub = Menu(options_menu)

        # Add an item to a submenu
        insert_sub.add_command(label='New Product', command=self.NP)

        # Add an item to a submenu
        search_sub.add_command(label='Search Products', command=self.SP)

        # Add an item to a submenu
        update_sub.add_command(label='Edit Products', command=self.EP)

        # Add a submenu
        options_menu.add_cascade(label='Insert', menu=insert_sub)

        # Add a submenu
        options_menu.add_cascade(label='Search', menu=search_sub)

        # Add a submenu
        options_menu.add_cascade(label='Update', menu=update_sub)

        options_menu.add_separator()

        # Adds a menu item to the menu
        options_menu.add_command(label='Price Comparison', command=self.PC)

        # Adds a menu item to the menu
        options_menu.add_command(label='Customer Orders', command=self.CO)

        options_menu.add_separator()

        # Adds a menu item to the menu
        options_menu.add_command(label='Exit', command=self.exit_program)

        # Adds the File menu to the menubar
        menubar.add_cascade(label="Options", menu=options_menu)

    def NP(self):
        # Deletes the graph frame due to it appearing behind the other containers
        try:
            self.frame_4.destroy()
        except:
            pass
        try:
            self.frame_5.destroy()
        except:
            pass

        self.frame_1 = Insert_Frame(app, self.stock_table)
        # Assigns the variable to a set opition on the Main Window
        self.frame_1.grid(row=0, column=0)

        self.geometry('310x180')

    def SP(self):
        # Deletes the graph frame due to it appearing behind the other containers
        try:
            self.frame_4.destroy()
        except:
            pass
        try:
            self.frame_5.destroy()
        except:
            pass

        self.frame_2 = Search_Frame(app, self.stock_table)
        # Assigns the variable to a set opition on the Main Window
        self.frame_2.grid(row=0, column=0)

        self.geometry('310x180')

    def EP(self):
        # Deletes the graph frame due to it appearing behind the other containers
        try:
            self.frame_4.destroy()
        except:
            pass
        try:
            self.frame_5.destroy()
        except:
            pass

        # Assigns class to varible
        self.frame_3 = Edit_Frame(app, self.stock_table)
        # Assigns the variable to a set opition on the Main Window
        self.frame_3.grid(row=0, column=0)

        self.geometry('330x245')

    def PC(self):
        try:
            self.frame_5.destroy()
        except:
            pass

        # Assigns class to varible
        self.frame_4 = Graph_Frame(app, self.stock_table)
        # Assigns the variable to a set opition on the Main Window
        self.frame_4.grid(row=0, column=0)

        self.geometry('600x750')

    def CO(self):
        # Deletes the graph frame due to it appearing behind the other containers
        try:
            self.frame_4.destroy()
        except:
            pass

        # Assigns class to varible
        self.frame_5 = Customer_Orders_Frame(app, self.stock_table)
        # Assigns the variable to a set opition on the Main Window
        self.frame_5.grid(row=0, column=0)

        self.geometry('1400x300')

    def exit_program(self):
        logger.info('User closed the program')
        sys.exit(0)


# Handles a closing event
def closing_event():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()
        logger.info('User closed the program')


if __name__ == "__main__":

    logger.info('Program started')

    stock_table = HashTable()

    app = App(stock_table)

    frame_1 = Insert_Frame(app, stock_table)
    # Assigns the variable to a set opition on the Main Window
    frame_1.grid(row=0, column=0)

    # Sets the function to handle a closing event
    app.protocol("WM_DELETE_WINDOW", closing_event)

    app.mainloop()