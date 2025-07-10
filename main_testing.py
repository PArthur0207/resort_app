from ask_info import DataEntry

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
print(f"{pax} customers will arrive on {date} at {time}. They will stay at {cottage}")
