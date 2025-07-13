from flask import Flask, render_template, request
from calculations import Process
from datetime import datetime
import csv
import os
import logging

app = Flask(__name__)
FILENAME = "reservations.csv"

def parse_date_time(date_str, time_str):
    for fmt in ("%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(f"{date_str} {time_str}", f"{fmt} %H:%M")
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date/time: {date_str} {time_str}")

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["GET", "POST"])
def reserve():
    form_data = {}  # Initialize form_data as an empty dictionary
    if request.method == "POST":
        try:
            date = request.form["date"]
            time = request.form["time"]
            pax = int(request.form["pax"])
            cottage = request.form["cottage"].strip().upper()
            name = request.form["name"]
            contact = request.form["contact"]
            email = request.form["email"]

            # Log the received form data
            logging.debug("Received form data: %s", request.form)

            # Validate inputs
            reservation_datetime = parse_date_time(date, time)  # Get full datetime object
            current_datetime = datetime.now()
            
            # Compare datetime objects properly
            if reservation_datetime < current_datetime:
                raise ValueError("Reservation date/time cannot be in the past.")
                
            if cottage not in ["A", "B", "C", "D"]:
                raise ValueError("Invalid cottage option.")
            if not contact.isdigit() or len(contact) != 11:
                raise ValueError("Contact number must be 11 digits.")

            # Now that all is valid, proceed
            do = Process()
            total_payment = do.payment_calculator(pax, cottage)

            reservation_data = {
                "Date": date,
                "Time": time,
                "Pax": pax,
                "Cottage": cottage,
                "Name": name,
                "Contact": contact,
                "Email": email or "",
                "Total Payment": total_payment
            }

            # Only write to CSV after validation
            file_exists = os.path.isfile(FILENAME)
            with open(FILENAME, mode="a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=reservation_data.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(reservation_data)

            # Sort CSV
            with open(FILENAME, newline="") as file:
                reader = csv.DictReader(file)
                rows = list(reader)
            rows.sort(key=lambda row: parse_date_time(row["Date"], row["Time"]))
            with open(FILENAME, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=reservation_data.keys())
                writer.writeheader()
                writer.writerows(rows)

            # Log success and return success message
            logging.debug("Reservation successful: %s", reservation_data)
            return render_template("form.html", success="Reservation successful!", total=total_payment, form_data=form_data)

        except ValueError as ve:
            form_data = request.form  # Retain user input on error
            logging.error("ValueError: %s", str(ve))
            return render_template("form.html", error=str(ve), form_data=form_data)
        except Exception as e:
            logging.error("An unexpected error occurred: %s", e)  # Log the error
            form_data = request.form  # Retain user input on unexpected error
            return render_template("form.html", error="An unexpected error occurred. Please try again.", form_data=form_data)

    # Ensure form_data is passed on GET request
    return render_template("form.html", form_data=form_data)


if __name__ == "__main__":
    app.run(debug=True)
