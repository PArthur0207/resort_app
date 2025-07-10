from datetime import datetime

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
        
    def get_time(self, prompt):
        user_input = input(prompt).strip()
        try:
            parsed_time = datetime.strptime(user_input, self.TIME_FORMAT)
            return parsed_time.strftime(self.TIME_FORMAT)
        except ValueError:
            print("Invalid time format. Please enter the time as HH:MM (24-hour).")
            return self.get_time(prompt)
