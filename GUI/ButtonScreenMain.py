from tkinter import *

def CreateMainButtons(master,page_change):
    MainFrame = Frame(master)

    MainFrame.grid(row=0, column=0, sticky="nsew")
    # Sangam Title
    MainTitle = Label(MainFrame, text="SANGAM ACCOUNTS APP", pady=20, font=("Arial", 25, "bold"), bg="White")
    MainTitle.pack(side="top", fill='x')

    # Buttons (Photoshoot, Printout, Generate Monthly Account, New Client)
    ButtonFrame = Frame(MainFrame, bg="lightblue")
    PhotoshootButton = Button(ButtonFrame, text="PhotoShoot", command=lambda: page_change("PhotoShoot"), font="Arial 50 bold")
    PrintoutButton = Button(ButtonFrame, text="Printout", command=lambda: page_change("Printout"), font="Arial 50 bold")
    GenerateExcelButton = Button(ButtonFrame, text="Generate Monthly \nAccount", command=lambda: page_change("MonthlyAccount"),font="Arial 40 bold")
    NewClientButton = Button(ButtonFrame, text="Add New \nClient", command=lambda: page_change("NewCust"), font="Arial 40 bold")

    PhotoshootButton.grid(row=0, column=0, sticky=NSEW)
    PrintoutButton.grid(row=0, column=1, sticky=NSEW)
    GenerateExcelButton.grid(row=1, column=0, sticky=NSEW)
    NewClientButton.grid(row=1, column=1, sticky=NSEW)

    ButtonFrame.pack(fill="both", expand=True)
    ButtonFrame.grid_columnconfigure(index=0, weight=1)
    ButtonFrame.grid_rowconfigure(index=0, weight=5)
    ButtonFrame.grid_columnconfigure(index=1, weight=1)
    ButtonFrame.grid_rowconfigure(index=1, weight=1)

    return MainFrame