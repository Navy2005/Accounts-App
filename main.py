from tkinter import *
from Database.init_db import init_db
from GUI.ButtonScreenMain import CreateMainButtons
from GUI.CorrectPhotoshootPageFunction import CreateCorrectPhotoshootPage
from GUI.CorrectPrintoutPageFunction import CreateCorrectPrintoutPage
from GUI.PrintOutPageFunction import CreatePrintoutFrame
from GUI.PhotoShootPageFunction import CreatePhotoShootFrame
from GUI.AddNewCustomerPage import Create_NewCustomerPage
from GUI.GenerateAccountPage import CreateMonthlyAccountPage

init_db()

root = Tk()
# noinspection SpellCheckingInspection
root.title("Sangam Accounts App")
# Size Definition
root.geometry("1280x720")
root.resizable(False,False)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frames = {}
def show_page(name, **kwargs):
    frame = frames[name]
    frame.tkraise()
    if hasattr(frame, 'update_dropdown'):
        frame.update_dropdown(**kwargs)


# New Customer Frame Created and added to frames{} dict
NewCustomerFrame = Create_NewCustomerPage(root, show_page)
NewCustomerFrame.grid(row=0,column=0,sticky="nsew")
frames["NewCust"] = NewCustomerFrame

# Generate Monthly Account Page
MonthlyAccountFrame = CreateMonthlyAccountPage(root, show_page)
MonthlyAccountFrame.grid(row=0,column=0,sticky="nsew")
frames["MonthlyAccount"] = MonthlyAccountFrame

# Photoshoot Frame Created and added to frames{} dict
PhotoFrame = CreatePhotoShootFrame(root,show_page)
PhotoFrame.grid(row=0,column=0,sticky="nsew")
frames["PhotoShoot"] = PhotoFrame

# Printout Frame Created and added to frames{} dict
PrintFrame = CreatePrintoutFrame(root,show_page)
PrintFrame.grid(row=0,column=0,sticky="nsew")
frames["Printout"] = PrintFrame

CorrectPhotoshootFrame = CreateCorrectPhotoshootPage(root,show_page)
CorrectPhotoshootFrame.grid(row=0,column=0,sticky="nsew")
frames["CorrectPhotoshoot"] = CorrectPhotoshootFrame

CorrectPrintoutFrame = CreateCorrectPrintoutPage(root,show_page)
CorrectPrintoutFrame.grid(row=0,column=0,sticky="nsew")
frames["CorrectPrintout"] = CorrectPrintoutFrame

# Main Frame (Main Menu/Navigation Buttons) Created and added to frames{} dict
MainFrame = CreateMainButtons(root,show_page)
MainFrame.grid(row=0,column=0,sticky="nsew")
frames["Main"] = MainFrame



#Exit Button
ExitButton = Button(MainFrame, text="EXIT",font="Arial 20 bold",bg="white", command=lambda : root.destroy())
ExitButton.pack(fill="x")



root.mainloop()
