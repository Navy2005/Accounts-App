import os
import openpyxl
from Literals.literals import MONTH_MAP

def generate_excel_report(client_name, month_number, year, fetched_records):
    """
    fetched_records expected format:
    [(order_id, date, quantity, category), (order_id, date, quantity, category)]
    """

    # ==========================================
    # 1. ORGANIZE THE DATA
    # ==========================================
    # We will build a dictionary that looks like this:
    # {'2026-07-15': {'Photoshoot': 5, 'Printout': ''}, ...}
    consolidated_data = {}

    for record in fetched_records:
        order_id, iso_date, quantity, category = record
        year, month, day = iso_date.split("-")
        date = f"{day}-{month}-{year}"
        # If this is the first time we see this date, create a blank template
        if date not in consolidated_data:
            consolidated_data[date] = {"Photoshoot": "", "Printout": ""}

        # Add the quantity to the correct category slot
        # If multiple entries exist for the same day/category, this adds them together.
        if consolidated_data[date][category] == "":
            consolidated_data[date][category] = quantity
        else:
            consolidated_data[date][category] += quantity

    # ==========================================
    # 2. BUILD THE EXCEL FILE
    # ==========================================
    wb = openpyxl.Workbook()
    ws = wb.worksheets[0]
    ws.title = "Monthly Orders"
    # Append the Header Row
    ws.append(["Date", "Photoshoot", "Printout"])

    # Append the Data Rows (Sorted alphabetically/chronologically by ISO date)
    for date in sorted(consolidated_data.keys()):
        # Extract the values (they will be empty strings if no order existed that day)
        photo_qty = consolidated_data[date]["Photoshoot"]
        print_qty = consolidated_data[date]["Printout"]

        # Write the row to Excel
        ws.append([date, photo_qty, print_qty])

    # ==========================================
    # 3. SAVE THE FILE
    # ==========================================
    # Format the file name as requested: Client-Month-Year-Account.xlsx
    month_name = next((k for k, v in MONTH_MAP.items() if v == month_number), None)
    filename = f"{client_name}-{month_name}-{year}-Account.xlsx"
    # Save it to the user's Documents folder so they can easily find it
    client_dir = os.path.join("path to folder")
    # network_dir = os.path.join(client_dir)

    if not os.path.isdir(client_dir):
        return False, f"Network path unreachable or not found:\n{client_dir}"

    save_path = os.path.join(client_dir, filename)

    # 2. Attempt to save with exception handling
    try:
        wb.save(save_path)
    except PermissionError:
        return False, "Permission denied. The file may be open by another user, or write access is restricted."
    except OSError as e:
        return False, f"Network connection error occurred while writing:\n{e}"
    except Exception as e:
        return False, f"An unexpected error occurred:\n{e}"

    # 3. Verify the file exists and has written data (> 0 bytes)
    if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
        return True, save_path
    else:
        return False, "Save command executed, but file could not be verified on the destination."

