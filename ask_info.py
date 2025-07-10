from datetime import datetime
import re

class DataEntry:
    DATE_FORMAT = "%d-%m-%Y"
    TIME_FORMAT = "%H:%M"   

    def get_date(self, prompt, allow_default=False):
        user_input = input(prompt).strip()

        if allow_default and not user_input:
            return datetime.today().strftime(self.DATE_FORMAT)

        try:
            parsed_date = datetime.strptime(user_input, self.DATE_FORMAT)
            today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

            if parsed_date < today:
                print("Date cannot be earlier than today.")
                return self.get_date(prompt, allow_default)
            return parsed_date.strftime(self.DATE_FORMAT)
        except ValueError:
            print("Invalid date format. Please enter the date as dd-mm-yyyy.")
            return self.get_date(prompt, allow_default)
        
    def get_time(self, prompt="Enter time (HH:MM, 24-hour format between 08:00 and 16:00): "):
        user_input = input(prompt).strip()

        # Quick check: must contain ":" and look like HH:MM
        if ":" not in user_input or len(user_input) < 4:
            print("Invalid input. Please use HH:MM format (24-hour).")
            return self.get_time(prompt)

        try:
            parsed_time = datetime.strptime(user_input, self.TIME_FORMAT)
            hour = parsed_time.hour
            if 8 <= hour <= 16:
                return parsed_time.strftime(self.TIME_FORMAT)
            else:
                print("Time must be between 08:00 and 16:00.")
                return self.get_time(prompt)
        except ValueError:
            print("Invalid time format. Please enter the time as HH:MM (e.g. 14:30).")
            return self.get_time(prompt)

    def get_pax(self, prompt):
        try:
            user_input = int(input(prompt))
            return user_input
        except:
            print("Invalid Input please put a proper number.")
            return self.get_pax(prompt)
    
    def get_cottage(self, prompt):
        user_input = input(prompt).upper().strip()

        if user_input == 'A':
            return "Big Cottage"
        elif user_input == 'B':
            return "Small Cottage"
        elif user_input == 'C':
            return "Umbrella"
        elif user_input == 'D':
            return "None"
        else:
            print("Please enter a valid choice (A-D)")
            return self.get_cottage(prompt)
        
    def get_contact_info(self):
        name = input("Enter your full name: ").strip()

        # Accept only exactly 11 digits
        while True:
            contact = input("Enter your contact number (11 digits): ").strip()
            if contact.isdigit() and len(contact) == 11:
                break
            print("Invalid contact number. Please enter exactly 11 digits.")

        # Email is optional
        while True:
            email = input("Enter your email address (optional): ").strip()
            if email == "" or re.match(r"[^@]+@[^@]+\.[^@]+", email):
                break
            print("Invalid email format. Please try again.")

        return {
            "name": name,
            "contact": contact,
            "email": email if email else None
        }
