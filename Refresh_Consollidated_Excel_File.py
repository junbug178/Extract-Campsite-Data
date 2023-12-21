import os
import win32com.client as win32
import time

def refresh_excel_data(file_path):
    # Path to the Excel file
    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return

    # Start an instance of Excel
    excel = win32.gencache.EnsureDispatch('Excel.Application')

    # Disable alerts (like confirmation dialogs)
    excel.DisplayAlerts = False

    # Excel visible to the user (optional)
    excel.Visible = True

    # Open the Excel file
    workbook = excel.Workbooks.Open(file_path)

    # Refresh all data connections
    workbook.RefreshAll()

    # Wait for each query to complete
    for sheet in workbook.Sheets:
        for query in sheet.QueryTables:
            while query.Refreshing:
                time.sleep(1)

    # Save and close
    workbook.Save()
    workbook.Close()

    # Re-enable alerts
    excel.DisplayAlerts = True

    # Quit Excel
    excel.Application.Quit()

# Path to your Excel file
excel_file_path = r'C:\Users\junbu\OneDrive\Documents\GitHub\Extract Campsite Data\Consolidatd View Site Availability.xlsx'
refresh_excel_data(excel_file_path)
