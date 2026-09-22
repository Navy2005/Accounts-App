from tkinter import *
from tkinter import ttk, messagebox

from Database.entry_correction_update_command import correct_order
from Database.get_client_list import GetClientList
from Database.get_order_details import get_Client_orders, get_order_id_list
from Literals.literals import MONTH_MAP, add_separator


def execute_order_correction(order_id, quantity):
    message = "Change order id {0} to {1} pieces ? ".format(order_id,quantity)
    response = messagebox.askquestion(title="SUBMIT", message=message)
    if response == 'yes':
        correct_order(quantity, order_id)
        message = "Successfully changed entry"
        messagebox.showinfo(title="SUBMIT", message=message)
        selected_client.set("Select a Client")
        selected_month.set("Select a Month")
        selected_ID.set("Select an ID")
        QuantityEntry.delete(0, END)
    else:
        messagebox.showwarning(title="Error", message="Change Cancelled")
        selected_client.set("Select a Client")
        selected_month.set("Select a Month")
        selected_ID.set("Select an ID")
        QuantityEntry.delete(0, END)

def CreateCorrectPrintoutPage(parent, show_page):
    ParentFrame = Frame(parent)
    MainTitle = Label(ParentFrame, text="Correction In Printouts",pady=18, font=("Arial", 25, "bold"), bg="White")
    MainTitle.pack(side="top", fill="x")

    EnterDataFrame = Frame(ParentFrame)
    EnterDataFrame.pack(anchor="center", fill="both", expand=True)
    EnterDataFrame.grid_columnconfigure(index=0, weight=1)
    EnterDataFrame.grid_columnconfigure(index=1, weight=8)

    # Empty Label Which Acts as blank space to add division wherever needed
    add_separator(EnterDataFrame, 0, 1)

    ClientLabel = Label(EnterDataFrame, text="Select Client :", font="Arial 25 bold")
    ClientLabel.grid(row=1, column=0, sticky="nsew")

    MonthLabel = Label(EnterDataFrame, text="Select Month :", font="Arial 25 bold")
    MonthLabel.grid(row=1, column=1, sticky="nsew")

    # Create a Tkinter String Variable to hold the selected value
    global selected_client
    selected_client = StringVar()
    # Set the default text that shows before a user clicks it
    selected_client.set("Select a Client")

    # Create a Tkinter String Variable to hold the selected value
    global selected_month
    selected_month = StringVar()
    # Set the default text that shows before a user clicks it
    selected_month.set("Select a Month")

    ClientSelection = ttk.Combobox(EnterDataFrame, textvariable=selected_client, width=45, height=5,
                                   font="Arial 20 bold")
    # ClientSelection.config(
    #     width=20,      # Width in character units
    #     height=2,      # Height in text lines
    #     padx=10,       # Horizontal internal padding
    #     pady=5        # Vertical internal padding
    # )
    ClientSelection.option_add("*TCombobox*Listbox.font", ("Arial", 20, "bold"))
    ClientSelection['values'] = ('Apple', 'Banana', 'Cherry', 'Date')
    ClientSelection['state'] = 'readonly'

    MonthSelection = ttk.Combobox(EnterDataFrame, textvariable=selected_month, width=25, height=5, font="Arial 20 bold")
    MonthSelection.option_add("*TCombobox*Listbox.font", ("Arial", 20, "bold"))
    MonthSelection['values'] = list(MONTH_MAP.keys())
    MonthSelection['state'] = 'readonly'


    #This functions gets the list of clients from database and
    # updates the combobox dropdown everytime the page is called forward(tkraise())
    def update_dropdown():
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

    # this statement registers an attribute named - "update dropdown" to this python frame
    # so that main.py can call it when this frame will be raised
    ParentFrame.update_dropdown = update_dropdown
    #calling the function once manually in order to load the list at first(initial) call
    update_dropdown()

    # 5. Place it on the screen
    ClientSelection.grid(row=2, column=0, sticky="nsew", padx=25)
    MonthSelection.grid(row=2, column=1, sticky="nsew", padx=20)


# this Section displays last month all entries
    LastMonthEntriesLabel = Label(EnterDataFrame, text="Last Month Entries :", font="Arial 25 bold")
    LastMonthEntriesLabel.grid(row=3, columnspan=2)

    LastMonthEntriesContainer = Frame(EnterDataFrame)
    LastMonthEntriesContainer.grid(row=4, columnspan=2, padx=30, sticky="nsew")

    OrdersListScrollbar = Scrollbar(LastMonthEntriesContainer)
    OrdersListScrollbar.pack(side="right", fill="y")

    OrdersList = Listbox(LastMonthEntriesContainer, width=50, height=5, font="Arial 20 bold", bg="WHITE",
                         yscrollcommand=OrdersListScrollbar.set)
    OrdersList.pack(side="top", fill="both")

    OrdersListScrollbar.config(command=OrdersList.yview)

    add_separator(EnterDataFrame, row=5, height=2)

    IDLabel = Label(EnterDataFrame, text="Enter Order ID :", font="Arial 25 bold")
    IDLabel.grid(row=6, column=0)

    global selected_ID
    selected_ID = StringVar()
    selected_ID.set("Select a Date")
    IDSelection = ttk.Combobox(EnterDataFrame, textvariable=selected_ID, width=50, height=5, font="Arial 20 bold")
    IDSelection.option_add("*TCombobox*Listbox.font", ("Arial", 20, "bold"))
    IDSelection['values'] = ()
    IDSelection['state'] = 'readonly'
    IDSelection.grid(row=6, column=1, sticky="nsew", padx=30)

    def validate_fetch_Populate_OrdersList(event=None):
        """
            Validates selections, then updates both the Listbox and
            the Date Combobox using a single database call.
            """
        client = selected_client.get()
        month_name = selected_month.get()

        invalid_clients = ["", "Select a Client", "No clients found"]
        invalid_months = ["", "Select a Month"]

        # 1. Reset widgets
        OrdersList.delete(0, END)

        # 2. Guard clause: Ensure both dropdowns have valid choices
        if (client in invalid_clients) or (month_name in invalid_months):
            IDSelection['values'] = []
            IDSelection.set("Select Client and Month...")
            IDSelection['state'] = DISABLED
            return

        # 3. Fetch monthly records (returns [(date, qty), ...])
        month_number = MONTH_MAP[month_name]
        records = get_Client_orders(client, month_number, "Printout")

        if not records:
            OrdersList.insert(END, "No records found for this month.")
            IDSelection['values'] = []
            IDSelection.set(f"No orders in {month_name}")
            IDSelection['state'] = DISABLED

        # 4. Populate the Listbox (Sorted ascending by date)
        for order_id, order_date, qty in records:
            year, month, day = order_date.split("-")
            display_date = f"{day}-{month}-{year}"
            OrdersList.insert(END, f" Order ID : {order_id}  |  {display_date}  |  Quantity : {qty}")

        # 5. Extract unique ISO dates directly from the records for the Combobox
        if records:
            unique_order_id = get_order_id_list(client, month_number, "Printout")
            IDSelection['state'] = "readonly"
            IDSelection['values'] = unique_order_id
            IDSelection.set("Select an Order ID")

    ClientSelection.bind("<<ComboboxSelected>>", validate_fetch_Populate_OrdersList)
    MonthSelection.bind("<<ComboboxSelected>>", validate_fetch_Populate_OrdersList)

    add_separator(EnterDataFrame,row=7,height=2)

    QuantityLabel = Label(EnterDataFrame, text="Enter Correct Quantity :", font="Arial 25 bold")
    QuantityLabel.grid(row=8, column=0, ipadx=30)

    # Create the Entry widget and link the validation(It Allows only Numbers to be entered)
    def only_numbers(char):
        return char.isdigit() or char == ""

    validate_command = EnterDataFrame.register(only_numbers), '%S'
    global QuantityEntry
    QuantityEntry = Entry(
        EnterDataFrame,
        validate="key",  # 'key' means validate on every keystroke
        validatecommand=validate_command,  # Link our function here
        font="Arial 25 bold", width=50)
    QuantityEntry.grid(row=8, column=1, padx=30)

    add_separator(EnterDataFrame, row=9, height=2)

    SubmitButton = Button(EnterDataFrame, text="Submit", font="Arial 20 bold", bg="white", command= lambda : execute_order_correction(selected_ID.get(),QuantityEntry.get()))
    SubmitButton.grid(row=10, columnspan=2)

    BackToHomeButton = Button(ParentFrame, text="Back To Home", font="Arial 20 bold", bg="white", command=lambda : show_page("Main"))
    BackToHomeButton.pack(side="bottom", fill="x")

    return ParentFrame