from tkinter import *
from tkinter import messagebox
from Literals.literals import add_separator
from Database.insert_client import InsertClient

def SubmitNewClient():
    name = str(ClientNameEntry.get())
    message = "Add Client : " + name
    response = messagebox.askquestion(title="SUBMIT",message=message)
    if response =='yes':
        InsertClient(name)
        message="Successfully Added Client : " + name
        messagebox.showinfo(title="SUBMIT",message=message)
        ClientNameEntry.delete(0,END)
    else:
        messagebox.showwarning(title="Error", message="Insert Cancelled")
        ClientNameEntry.delete(0, END)


def Create_NewCustomerPage(parent, page_change):
    ParentFrame = Frame(parent)
    MainTitle = Label(ParentFrame, text="Add New Client", pady=20, font=("Arial", 25, "bold"), bg="White")
    MainTitle.pack(side="top", fill="x")

    EnterDataFrame = Frame(ParentFrame)
    EnterDataFrame.pack(anchor="center", fill="both", expand=True)
    EnterDataFrame.grid_columnconfigure(index=0,weight=1)
    EnterDataFrame.grid_columnconfigure(index=1,weight=8)

    add_separator(EnterDataFrame, 0,5)

    # Add New Customer Label With Data Entry
    ClientNameLabel = Label(EnterDataFrame, text="Client Name :", font="Arial 20 bold")
    ClientNameLabel.grid(row=1, column=0,sticky="nsew",padx=10)


    def only_alphabets(char):
        return char.isalpha() or char == "" or char == " "

    validate_command = EnterDataFrame.register(only_alphabets), '%S'
    global ClientNameEntry
    ClientNameEntry = Entry(
        EnterDataFrame,
        validate="key",
        validatecommand=validate_command,
        font="Arial 30 bold",
        width=50)
    ClientNameEntry.grid(row=1,column=1,padx=30,sticky="nsew")

    add_separator(EnterDataFrame,2,5)

    SubmitButton = Button(EnterDataFrame, text="Submit", font="Arial 20 bold", bg="white", command= lambda : SubmitNewClient())
    SubmitButton.grid(row=3, columnspan=2)

    BackToHomeButton = Button(ParentFrame, text="Back To Home", font="Arial 20 bold", bg="white", command= lambda : page_change("Main"))
    BackToHomeButton.pack(side="bottom", fill="x")
    return ParentFrame