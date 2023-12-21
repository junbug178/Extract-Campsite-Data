import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # Add this import
from selenium.webdriver.support import expected_conditions as EC  # Add this import
from datetime import datetime, timedelta
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

# Wait for the datepicker element to be visible
wait = WebDriverWait(driver, 10)
datepicker_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='ui-voffset-lg']//input[@class='datepicker text-center form-control interactive-grid-date hasDatepicker']")))

# Define the start date and end date
start_date = datetime.today()
end_date = start_date + timedelta(days=14)

# Loop through the date range
current_date = start_date
while current_date <= end_date:
    # Format the new date in 'm/d/y' format
    formatted_date = current_date.strftime("%m/%d/%Y")

    # Send the new date to the datepicker input
    datepicker_element.send_keys(Keys.CONTROL, 'a')
    datepicker_element.send_keys(Keys.DELETE)
    datepicker_element.send_keys(formatted_date)
    datepicker_element.send_keys(Keys.ENTER)
    datepicker_element.send_keys(Keys.ENTER)

    # Wait for the page to load (you may adjust the wait time as needed)
    time.sleep(5)

    # Continue with the rest of your code related to table extraction and Excel saving
    
    # Update the current date for the next iteration by adding 7 days
    current_date += timedelta(days=7)

# Close the Chrome WebDriver
driver.quit()

