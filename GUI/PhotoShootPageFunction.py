from tkinter import *
from tkinter import ttk, messagebox
from Database.insert_order import  insert_order
from Database.get_client_list import GetClientList
from Literals.literals import add_separator


def SubmitOrder(name:str, quantity:int):
    message = "Add {0} Photoshoot for {1}".format(str(quantity), name)
    response = messagebox.askquestion(title="SUBMIT",message=message)
    if response =='yes':
        insert_order(name,quantity,"Photoshoot")
        message= "Successfully Added {0} Photoshoot for {1}".format(str(quantity), name)
        messagebox.showinfo(title="SUBMIT",message=message)
        selected_client.set("Select a Client")
        QuantityEntry.delete(0,END)
    else:
        messagebox.showwarning(title="Error", message="Insert Cancelled")
        selected_client.set("Select a Client")
        QuantityEntry.delete(0,END)



def CreatePhotoShootFrame(parent, page_change):

    ParentFrame = Frame(parent)
    MainTitle = Label(ParentFrame, text="Add Photo Shoots", pady=20, font=("Arial", 25, "bold"), bg="White")
    MainTitle.pack(side="top", fill="x")

    # Data Entry Frame

    EnterDataFrame = Frame(ParentFrame)
    EnterDataFrame.pack(anchor="center", fill="both", expand=True)

    add_separator(EnterDataFrame, 0,5)

    ClientLabel = Label(EnterDataFrame, text="Select Client :", font="Arial 25 bold")
    ClientLabel.grid(row=1, column=0, sticky="nsew")

    EnterDataFrame.grid_columnconfigure(index=0, weight=1)
    EnterDataFrame.grid_columnconfigure(index=1, weight=8)

    # 2. Create a Tkinter String Variable to hold the selected value
    global selected_client
    selected_client= StringVar()
    # 3. Set the default text that shows before a user clicks it
    selected_client.set("Select a Client")


    global ClientSelection
    ClientSelection = ttk.Combobox(EnterDataFrame, textvariable=selected_client, width=50, height=5, font="Arial 25 bold")
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



    # Quantity Selection
    QuantityLabel = Label(EnterDataFrame, text="Enter Quantity :", font="Arial 25 bold")
    QuantityLabel.grid(row=3, column=0, ipadx=30)

    # 2. Create the Entry widget and link the validation
    def only_numbers(char):
        return char.isdigit() or char == ""

    validate_command = EnterDataFrame.register(only_numbers), '%S'
    global QuantityEntry
    QuantityEntry = Entry(
        EnterDataFrame,
        validate="key",  # 'key' means validate on every keystroke
        validatecommand=validate_command,  # Link our function here
        font="Arial 30 bold", width=50)
    QuantityEntry.grid(row=3, column=1, padx=30)

    add_separator(EnterDataFrame, 4,5)

    SubmitButton = Button(EnterDataFrame, text="Submit", font="Arial 20 bold", bg="white", command= lambda: SubmitOrder(name = str(ClientSelection.get()),quantity=int(QuantityEntry.get())))
    SubmitButton.grid(row=5, columnspan=2)

    add_separator(EnterDataFrame, row=6, height=5)

    CorrectionButton = Button(EnterDataFrame, text="Make\nCorrection", font="Arial 20 bold", bg="white",command= lambda : page_change("CorrectPhotoshoot"))
    CorrectionButton.grid(row=7)

    BackToHomeButton = Button(ParentFrame, text="Back To Home", font="Arial 20 bold", bg="white", command= lambda : page_change("Main"))
    BackToHomeButton.pack(side="bottom", fill="x")
    return ParentFrame