import requests
import pandas as pd
from datetime import datetime, timedelta

# Function to fetch facility details
def fetch_facility_details():
    url = "https://secure.rec1.com/FL/pinellas-county-fl/catalog/facilityGridData/14078"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch facility details")
    data = response.json()
    facility_details = {f["id"]: f["name"] for f in data["location"]["facilities"]}
    return facility_details

# Function to get paginated data
def get_paginated_data(url, headers, body_encoded):
    all_data = []
    while url:
        response = requests.post(url, headers=headers, data=body_encoded)
        if response.status_code != 200:
            print("Failed to retrieve data")
            print("Status Code:", response.status_code)
            break
        data = response.json()
        all_data.append(data['availability'])
        link_header = response.headers.get('Link', None)
        next_link = None
        if link_header:
            links = link_header.split(',')
            for link in links:
                if 'rel="next"' in link:
                    next_link = link.split(';')[0].strip('<> ')
                    break
        url = next_link
    return all_data

# Function to transform data
def transform_data(all_data, facility_details):
    rows = []
    for facility_data in all_data:
        for facility_id, years in facility_data.items():
            for year, months in years.items():
                for month, days in months.items():
                    for day, availability in days.items():
                        date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                        facility_name = facility_details.get(facility_id, "Unknown")
                        rows.append({'Facility Name': facility_name, 'facilityId': facility_id, 'date': date, 'availability': availability})
    df = pd.DataFrame(rows)
    pivot_df = df.pivot_table(index=['Facility Name', 'facilityId'], columns='date', values='availability', fill_value="Not Available")
    pivot_df = pivot_df.replace({0: "Not Available", 1: "Partially Available", 2: "Available"})
    pivot_df.reset_index(inplace=True)
    return pivot_df

# Fetch facility details
facility_details = fetch_facility_details()

# Current date and 227 days from today
current_date = datetime.now()
to_date = current_date + timedelta(days=227)

# Format dates in 'YYYY-MM-DD' format
formatted_current_date = current_date.strftime('%Y-%m-%d')
formatted_to_date = to_date.strftime('%Y-%m-%d')

# Initial URL and Headers
url = "https://secure.rec1.com/FL/pinellas-county-fl/permits/getMultiFacilityAvailability/fb55aacf5c0605d2e446daff2601761d"
headers = {
    'Host': 'secure.rec1.com',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-CSRF-KEY': '36e7783389c0873ed13c36c91097f05f',
    'X-CSRF-TOKEN': '61f2e93d494bc0f9c41a940a76604d77',
    'Accept': 'application/json, text/javascript, */*; q=0.01'
}

# Prepare body for POST request
body = {
    'facilityIds[]': list(facility_details.keys()),
    'from': formatted_current_date,
    'to': formatted_to_date
}

body_encoded = '&'.join([f'{key}={value}' for key, values in body.items() for value in (values if isinstance(values, list) else [values])])

# Fetch and transform data
all_data = get_paginated_data(url, headers, body_encoded)
formatted_data = transform_data(all_data, facility_details)

# Save to an Excel file
formatted_data.to_excel("facility_availability.xlsx", index=False, engine='openpyxl')


