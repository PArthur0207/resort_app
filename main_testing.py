from ask_info import DataEntry
from datetime import datetime
import csv
import os

FILENAME = "reservations.csv"

def parse_date_time(date_str, time_str):
    for fmt in ("%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(f"{date_str} {time_str}", f"{fmt} %H:%M")
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {date_str}")

# Ask user info
ask = DataEntry()
date = ask.get_date("Please enter when you want to reserve your spot, or enter for today's date: ", allow_default=True)
time = ask.get_time("Please enter the time you will arrive on. 24 hour format(HH:MM): ")
pax = ask.get_pax("How many people would be in your party: ")
cottage = ask.get_cottage("Please pick your cottage \n" \
"   A. Big Cottage(500Php) \n" \
"   B. Small Cottage(300Php) \n" \
"   C. Umbrella(150Php) \n" \
"   D. None  \n" \
"Pick from A to C, or press enter if you will not avail a cottage:" )
contact = ask.get_contact_info()

# Format date for consistency
date = datetime.strptime(date, "%d-%m-%Y").strftime("%d-%m-%Y")

# Prepare data to write
reservation_data = {
    "Date": date,
    "Time": time,
    "Pax": pax,
    "Cottage": cottage,
    "Name": contact["name"],
    "Contact": contact["contact"],
    "Email": contact["email"] or ""
}

# Write to CSV
file_exists = os.path.isfile(FILENAME)
with open(FILENAME, mode="a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=reservation_data.keys())
    if not file_exists:
        writer.writeheader()
    writer.writerow(reservation_data)

print("✅ Reservation saved.")

# Read and sort
with open(FILENAME, newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

rows.sort(key=lambda row: parse_date_time(row["Date"], row["Time"]))

# Overwrite CSV with sorted data
with open(FILENAME, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=reservation_data.keys())
    writer.writeheader()
    writer.writerows(rows)

print("📅 Reservations sorted by date and time.")
