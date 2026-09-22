from tkinter import Label

MONTH_MAP = {
    "January": "01", "February": "02", "March": "03", "April": "04",
    "May": "05", "June": "06", "July": "07", "August": "08",
    "September": "09", "October": "10", "November": "11", "December": "12"
}

def add_separator(parent, row, height):
    """Creates and grids a fresh horizontal separator."""
    s = Label(parent,height=height)
    s.grid(row=row, columnspan=2, sticky="nsew")
    return s