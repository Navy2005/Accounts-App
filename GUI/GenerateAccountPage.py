from tkinter import *
from tkinter import ttk, messagebox

from datetime import date as d
import pandas as pd

from Database.get_client_list import GetClientList
from Database.get_order_details import get_client_orders_with_category
from Excel_logic.generate_excel_file import generate_excel_report
from Literals.literals import add_separator

def generate_excel(client_name):
    message = "Make file for {0}".format(client_name)
    response = messagebox.askquestion(title="SUBMIT", message=message)
    if response == 'yes':
       month_number = d.today().strftime("%m")
       year_number = d.today().strftime("%Y")
       records = get_client_orders_with_category(client_name, month_number)
       resp = generate_excel_report(client_name, month_number, year_number, records)
       if not resp[0]:
          message = "Error : {0}".format(resp)
          messagebox.showwarning(title="Error", message=message)

       else:
           message = "File Saved Successfully"
           messagebox.showinfo(title="SUCCESS", message=message)
           selected_client.set("Select a Client")
    else:
        messagebox.showwarning(title="Error", message="Cancelled")
        selected_client.set("Select a Client")

def CreateMonthlyAccountPage(parent, page_change):
    ParentFrame = Frame(parent)

    MainTitle = Label(ParentFrame, text="Generate Monthly Account", pady=20, font=("Arial", 25, "bold"), bg="White")
    MainTitle.pack(side="top", fill="x")

    EnterDataFrame = Frame(ParentFrame)
    EnterDataFrame.pack(anchor="center", fill="both", expand=True)

    EnterDataFrame.grid_columnconfigure(index=0, weight=1)
    EnterDataFrame.grid_columnconfigure(index=1, weight=8)

    add_separator(EnterDataFrame, 0,5)

    # Add New Customer Label With Data Entry
    ClientLabel = Label(EnterDataFrame, text="Select Client :", font="Arial 25 bold")
    ClientLabel.grid(row=1, column=0, sticky="nsew")

    # 2. Create a Tkinter String Variable to hold the selected value
    global selected_client
    selected_client = StringVar()
    # 3. Set the default text that shows before a user clicks it
    selected_client.set("Select a Client")

    ClientSelection = ttk.Combobox(EnterDataFrame, textvariable=selected_client, width=50, height=5,
                                   font="Arial 20 bold")
    # ClientSelection.config(
    #     width=20,      # Width in character units
    #     height=2,      # Height in text lines
    #     padx=10,       # Horizontal internal padding
    #     pady=5        # Vertical internal padding
    # )
    ClientSelection.option_add("*TCombobox*Listbox.font", ("Arial", 20, "bold"))
    ClientSelection['values'] = [name[1] for name in GetClientList()]
    ClientSelection['state'] = 'readonly'

    #This functions gets the list of clients from database and
    # updates the combobox dropdown everytime the page is called forward(tkraise())
    def update_dropdown():
        global ClientList
        ClientList = [name[1] for name in GetClientList()]
        if not ClientList:
            # Use .config() instead of dictionary assignment
            ClientSelection.config(values=["No clients found"])
            selected_client.set("No clients found")
        else:
            ClientSelection.config(values=ClientList)
            # CRITICAL: Force the visible text to reset.
            # This proves to you visually that the function ran and the UI refreshed.
            selected_client.set("Select a Client")

    #this statement registers an attribute named - "update dropwdown" to this python frame
    # so that main.py can call it when this frame will be raised
    ParentFrame.update_dropdown = update_dropdown
    #calling the function once manually in order to load the list at first(initial) call
    update_dropdown()

    # 5. Place it on the screen
    ClientSelection.grid(row=1, column=1, sticky="nsew", padx=30)

    add_separator(EnterDataFrame, 2,5)

    SubmitButton = Button(EnterDataFrame, text="Generate Excel", font="Arial 20 bold", bg="white", command= lambda : generate_excel(selected_client.get()))
    SubmitButton.grid(row=3, columnspan=2)

    BackToHomeButton = Button(ParentFrame, text="Back To Home", font="Arial 20 bold", bg="white", command=lambda:page_change("Main"))
    BackToHomeButton.pack(side="bottom", fill="x")

    return ParentFrame