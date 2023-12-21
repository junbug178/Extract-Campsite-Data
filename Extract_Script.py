import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import openpyxl

# Set the path to the Chrome WebDriver executable
chrome_driver_path = "C:/Users/junbu/OneDrive/Documents/GitHub/Extract Campsite Data/chromedriver.exe"

# Set Chrome options
chrome_options = Options()
chrome_options.binary_location = "C:\\Users\\junbu\\OneDrive\\Documents\\GitHub\\Extract Campsite Data\\chrome-win64\\chrome.exe"

# Initialize the WebDriver with the provided options and path
driver_service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=driver_service, options=chrome_options)

# Open the webpage
url = "https://secure.rec1.com/FL/pinellas-county-fl/catalog"
driver.get(url)

# Wait for the page to load (you may adjust the wait time as needed)
time.sleep(5)

# Locate the table using the class name
table = driver.find_element(By.CLASS_NAME, "interactive-grid-table.ui-table.ui-table-fixed")

# Locate the thead element within the table
try:
    thead = table.find_element(By.TAG_NAME, "thead")
except NoSuchElementException:
    print("The <thead> element was not found.")
    driver.quit()

# Extract table headers and replace "<th>&nbsp;</th>" with "Site Number"
headers = []
for th in thead.find_elements(By.TAG_NAME, "th"):
    header_text = th.text
    if header_text == "\u00A0":
        header_text = "Site Number"
    if header_text.strip() != "":  # Check if the header is not blank
        headers.append(header_text)

# Add "Site Number" to the beginning of the headers list
headers.insert(0, "Site Number")

# Initialize a dictionary to store the availability statuses for each site
availability_statuses = {}

# Loop through rows in the table starting from the second row (index 1)
for row_index, row in enumerate(table.find_elements(By.TAG_NAME, "tr")):
    # Skip the first row (index 0)
    if row_index == 0:
        continue
    
    # Extract data from each cell in the row
    row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
    
    # The first cell contains the site number
    site_number = row_data[0]
    
    # The remaining cells contain availability statuses
    availability_status_elements = row.find_elements(By.CLASS_NAME, "interactive-grid-cell")
    
    # Extract and translate availability statuses using the lookup
    availability_status_texts = []
    for status_element in availability_status_elements:
        status_class = status_element.find_element(By.TAG_NAME, "div").get_attribute("class")
        if "bg-danger" in status_class:
            availability_status_texts.append("Not Available")
        elif "bg-success" in status_class:
            availability_status_texts.append("Available")
        elif "bg-warning" in status_class:
            availability_status_texts.append("Partially Available")
    
    # Store the availability statuses in the dictionary
    availability_statuses[site_number] = availability_status_texts

# Create a new Excel workbook and add a worksheet
workbook = openpyxl.Workbook()
worksheet = workbook.active

# Write the table headers to the Excel worksheet
worksheet.append(headers)

# Write the availability statuses to the Excel worksheet
for site_number, status_list in availability_statuses.items():
    row_values = [site_number] + status_list
    worksheet.append(row_values)

# Save the Excel workbook
excel_filename = "campsite_data_with_availability.xlsx"
workbook.save(excel_filename)

# Close the Chrome WebDriver
driver.quit()

print(f"Data has been extracted with availability statuses and saved to {excel_filename}.")
