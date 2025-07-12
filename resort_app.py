from flask import Flask, render_template, request
from calculations import Process
from datetime import datetime
import csv
import os

app = Flask(__name__)
FILENAME = "reservations.csv"

def parse_date_time(date_str, time_str):
    for fmt in ("%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(f"{date_str} {time_str}", f"{fmt} %H:%M")
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date/time: {date_str} {time_str}")

@app.route("/", methods=["GET", "POST"])
def reserve():
    form_data = {
        "date": "",
        "time": "",
        "pax": "",
        "cottage": "",
        "name": "",
        "contact": "",
        "email": ""
    }
    error = None

    if request.method == "POST":
        form_data = request.form.to_dict()
        try:
            date = form_data["date"]
            time = form_data["time"]
            pax = int(form_data["pax"])
            cottage = form_data["cottage"].strip().upper()
            name = form_data["name"]
            contact = form_data["contact"]
            email = form_data["email"]

            datetime.strptime(date, "%d-%m-%Y")
            datetime.strptime(time, "%H:%M")
            if cottage not in ["A", "B", "C", "D"]:
                raise ValueError("Please select a valid cottage.")
            if not contact.isdigit() or len(contact) != 11:
                raise ValueError("Contact number must be 11 digits.")

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

            file_exists = os.path.isfile(FILENAME)
            with open(FILENAME, mode="a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=reservation_data.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(reservation_data)

            with open(FILENAME, newline="") as file:
                reader = csv.DictReader(file)
                rows = list(reader)
            rows.sort(key=lambda row: parse_date_time(row["Date"], row["Time"]))
            with open(FILENAME, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=reservation_data.keys())
                writer.writeheader()
                writer.writerows(rows)

            return f"<h2>✅ Reservation submitted! Total payment: {total_payment} PHP</h2>"

        except Exception as e:
            error = f"⚠️ {str(e)}"

    return render_template("form.html", error=error, form_data=form_data)

if __name__ == "__main__":
    app.run(debug=True)
