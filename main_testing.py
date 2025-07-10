from ask_info import DataEntry

ask = DataEntry()

date = ask.get_date("Please enter when you want to reserve your spot, or enter for today's date: ", allow_default=True)
time = ask.get_time("Please enter the time you will arrive on. 24 hour format(HH:MM): ")
print(f"The customer will arrive on {date} at {time}.")
