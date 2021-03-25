from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
import datetime
import requests
import traceback
import os
from decimal import Decimal

""" 
Retrieve the exchange rate information from the sever and calculate exchange rates based on the user's inputs
"""

# Connect to the API and retrieve the JSON data
# Initialise attribute with our conversion rate data and retrieve the keys of our currency code
class ServerCommunication:
    def __init__(self):

        self.base_currency = None
        self.counter_currency = None
        self.amount = None
        self.total = None
        self.TWOPLACES = Decimal(10) ** -2
        self.EXCHANGE_R_API_KEY = os.environ.get("SECRET_KEY")
        self.endpoint = "https://v6.exchangerate-api.com/v6/"
        self.url = f"{self.endpoint}/{self.EXCHANGE_R_API_KEY}/latest"
        self.response = requests.get(url=f"{self.url}/GBP")
        self.data = self.response.json()
        self.conversion_rates = self.data["conversion_rates"]
        self.currency_codes = self.conversion_rates.keys()


# Inherit ServerCommunication class to access attributes
class App(ServerCommunication):
    def __init__(self):
        super().__init__()
        # Create our root window
        self.root = Tk()
        self.root.report_callback_exception = self.show_error
        self.root.config(bg="#536162")
        self.root.minsize(height=250, width=150)
        self.root.title("Live currency converter")

        self.date_today = datetime.date.today()

        # labels
        self.title_label = Label(text="Welcome to the real-time currency converter!",
                                 compound="center",
                                 font=("Verdana", 16, "bold"),
                                 bg="#31326f",
                                 width=60,
                                 fg="#f9fcfb")

        self.title_label.grid(column=0, row=0, columnspan=3)

        self.exchange_output_label = Label(bg="#536162",
                                           text="Enter the amount:",
                                           font=("Verdana", 16, "bold"),
                                           fg="#f9fcfb",
                                           compound="center")

        self.exchange_output_label.grid(column=1, row=1, pady=25)

        self.base_currency_input_label = Label(text="Base Currency",
                                               font=("Verdana", 14, "bold"),
                                               bg="#536162",
                                               fg="#f9fcfb")

        self.base_currency_input_label.grid(column=0, row=1)

        self.counter_currency_input_label = Label(text="Counter Currency",
                                                  font=("Verdana", 14, "bold"),
                                                  bg="#536162",
                                                  fg="#f9fcfb")
        self.counter_currency_input_label.grid(column=2, row=1)

        # dropdown
        self.list_of_currencies = [currency_code for currency_code in self.currency_codes]
        self.base_drop_down_menu = Combobox(self.root, width=15, textvariable=StringVar)
        self.base_drop_down_menu["values"] = self.list_of_currencies
        self.base_drop_down_menu.grid(column=0, row=2)
        self.counter_drop_down_menu = Combobox(self.root, width=15, textvariable=StringVar)
        self.counter_drop_down_menu["values"] = self.list_of_currencies
        self.counter_drop_down_menu.grid(column=2, row=2)

        # entry widget
        self.base_entry = Entry(self.root, width=20)
        self.base_entry.grid(column=1, row=2, pady=25)

        # buttons
        self.convert_button = Button(self.root,
                                     bg="#31326f",
                                     text="Convert",
                                     fg="#f9fcfb",
                                     font=("Verdana", 12, "bold"),
                                     command=self.get_values)
        self.convert_button.grid(column=1, row=3)

        self.root.mainloop()

    # Retrieve real time exchange rate data and show the user the conversion rate
    def get_values(self):
        self.base_currency = self.base_drop_down_menu.get()
        self.counter_currency = self.counter_drop_down_menu.get()
        self.amount = self.base_entry.get()
        self.response = requests.get(url=f"{self.url}/{self.base_currency}")
        self.data = self.response.json()
        self.conversion_rates = self.data["conversion_rates"]
        conversion_result = self.get_conversion_rate(self.amount, self.conversion_rates[self.counter_currency])
        self.exchange_output_label.config(text=f"{self.date_today}:\n{self.amount} {self.base_currency} = "
                                               f"{conversion_result} {self.counter_currency}")
        return self.get_conversion_rate(self.amount, self.conversion_rates[self.counter_currency])

    # conversion rate calculation and correct formatting
    def get_conversion_rate(self, input, rate_exchange):
        self.total = Decimal(input) * Decimal(rate_exchange)
        return Decimal(self.total).quantize(self.TWOPLACES)

    # Display errors to user in a message box
    def show_error(self, *args):
        err = traceback.format_exception(*args)
        messagebox.showerror("Exception", err)


currency_converter = App
currency_converter()






