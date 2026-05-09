"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: 20241077
 4. Date: 2025/11/22
****************************************************************************
"""
from graphics import *
import csv

flight_records = []

def read_data_file(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for record in csv_reader:
            flight_records.append(record)

            
#======TASK A - user input and file handling========
            
airport_codes = {"LHR":"London Heathrow","MAD":"Madrid Adolfo Suárez-Barajas",
                 "CDG":"Charles De Gaulle International","IST":"Istanbul Airport International",
                 "AMS":"Amsterdam Schiphol","LIS":"Lisbon Portela","FRA":"Frankfurt Main",
                 "FCO":"Rome Fiumicino","MUC":"Munich International","BCN":"Barcelona International"}

def get_user_input():

#loop keeps asking the user for valid input until everything is correct.
    while True:
        user_code = input("Please enter a three-letter city code : ").upper()
        # see whether the code exists in the dictionary.
        while len(user_code) != 3 or user_code not in airport_codes:
            if len(user_code) != 3:
                user_code = input("Wrong code length - please enter a three-letter city code : ").upper()
            else:
                user_code = input("Unavailable city code - please enter a valid city code : ").upper()

         # If the loop ends we now have a valid airport code.
        selected_airport = airport_codes[user_code]
        
        input_year = input("Please enter a year required in the format YYYY : ")
        while not input_year.isdigit() or len(input_year) != 4:
            input_year = input("Wrong data type - please enter a four-digit year value : ")
        
        numerical_year = int(input_year)

        # Check if the yaar is between 2000 and 2025.If not, ask again.
        if numerical_year < 2000 or numerical_year > 2025:
            input_year = input("Out of range - please enter a value from 2000 to 2025 : ")

        # Construct the expected CSV filename, e.g. "LHR2020.csv".      
        data_filename = user_code + input_year + ".csv"
        airport_label = airport_codes[user_code]
        
        try:
            # Try reading the data file. If this fails, the except block below will run.
            read_data_file(data_filename)
            print('')
            print('*' * 82)
            print("File " + data_filename + " selected - Planes departing " + airport_label + " " + input_year)
            print('*'* 82)
            print('')
            # Append the same information to results.txt for record-keeping.
            with open("results.txt", "a") as output_file:
                output_file.write('*' * 82 + '\n')
                output_file.write("File " + data_filename + " selected - Planes departing " + airport_label + " " + input_year + '\n')
                output_file.write('*' * 82 + '\n\n')
                # Return the validated user inputs so other tasks can use them.
            return user_code, input_year, airport_label
        except FileNotFoundError:
             # If the CSV file doesn't exist, notify the user and stop the program.
             
            print('\n',data_filename,"file not found. Please ensure the file is in the correct directory.\n")
            exit()

#=======TASK B - data processing and stats=======
def process_data():
    # Initialise counters
    total_count = 0
    terminal_2_count = 0
    short_route_count = 0
    af_count = 0
    low_temp_count = 0
    ba_count = 0
    delayed_af = 0

    # A set is used to track unique time slots where rain occurred
    rainy_times = set()

     # Append output to results.txt
    with open("results.txt", "a") as output_file:
        # Total number of flight records loaded from the CSV
        total_count = len(flight_records)
        print("The total number of flights from this airport was: ", total_count)
        output_file.write(f"The total number of flights from this airport was {total_count}\n")

        # Count flights that departed from Terminal 2 
        for entry in flight_records:
            if entry[8] == '2':
                terminal_2_count += 1
        print("The total number of flights departing from Terminal two was: ", terminal_2_count)
        output_file.write(f"The total number of flights departing from Terminal two was {terminal_2_count}\n")

        # Count flights with disstance < 600 miles (column index 5)
        for entry in flight_records:
            distance_value = int(entry[5])
            if distance_value < 600:
                short_route_count += 1
        print("The total number of departures on flights under 600 miles was: ", short_route_count)
        output_file.write(f"The total number of departures on flights under 600 miles was {short_route_count}\n")

        # Count Air France flights (any flight code starting with 'AF')
        for entry in flight_records:
            if entry[1][0:2] == 'AF':
                af_count += 1
        print("There were", af_count , "Air France flights from this airport.")
        output_file.write(f"There were {af_count} Air France flights from this airport.\n")

        # Count flights with temperatures below 15°C (column index 10 contains weather)
        # The weather column seeems to start with temperature (e.g., "12 rain")
        for entry in flight_records:
            if float(entry[10][0:2]) < 15:
                low_temp_count += 1
        print("There were", low_temp_count, "Flights departing in temperatures below 15 degrees")
        output_file.write(f"There were {low_temp_count} Flights departing in temperatures below 15 degrees\n")

        # Count British Airways flights (codes starting with 'BA')
        for entry in flight_records:
            if entry[1][0:2] == 'BA':
                ba_count += 1
        # BA average flights per hour (assuming 12 hours of operation)
        ba_avg = ba_count / 12
        print("There was an average of {:.2f}".format(ba_avg),'British Airways flights per hour from this airport')
        output_file.write(f"There was an average of {ba_avg:.2f} British Airways flights per hour from this airport\n")

        # BA percentage of total flights
        ba_ratio = (ba_count / total_count) * 100
        print("British Airways planes made up {:.2f}%".format(ba_ratio),'of all departures')
        output_file.write(f"British Airways planes made up {ba_ratio:.2f}% of all departures\n")


        # Count delayed Air France flights (terminal value > 0 indicates delay)
        for entry in flight_records:
            if entry[1][0:2] == 'AF' and float(entry[8]) > 0:
                delayed_af += 1
        # Percentage of delayed AF flights (avoid division by zero)
        delayed_af_ratio = (delayed_af / af_count) * 100 if af_count > 0 else 0
        print("{:.2f}%".format(delayed_af_ratio),'of Air France departures were delayed.')
        output_file.write(f"{delayed_af_ratio:.2f}% of Air France departures were delayed.\n")

        # Identify all hours during which rain was reported 
        for entry in flight_records:
            if 'rain' in entry[10].lower():
                time_slot = entry[2][:2]
                rainy_times.add(time_slot)
        print("There were", len(rainy_times),'hours in which rain fell')
        output_file.write(f"There were {len(rainy_times)} hours in which rain fell\n")

        # Determine the least common destination
        destination_stats = {}
        for entry in flight_records:
            dest_code = entry[4]
            dest_name = airport_codes.get(dest_code, dest_code)
            destination_stats[dest_name] = destination_stats.get(dest_name, 0) + 1

        # Find the destination with the lowest frequency
        min_destination = min(destination_stats, key=destination_stats.get)
        print("The least common destination is", min_destination,'\n')
        output_file.write(f"The least common destination is {min_destination}\n\n")

    # Return all stats as a dictionary for possible later use
    return {
        'total': total_count,
        'terminal2': terminal_2_count,
        'short_flights': short_route_count,
        'air_france': af_count,
        'cold_departures': low_temp_count,
        'ba_average': ba_avg,
        'ba_percentage': ba_ratio,
        'af_delayed_percent': delayed_af_ratio,
        'rain_hours': len(rainy_times),
        'least_destination': min_destination
    }

#========TASK D- histrogram ======

# This allows too display readable names instead of just codes.
carrier_list = {'BA': 'British Airways','AF': 'Air France', 'AY': 'Finnair',
                'KL': 'KLM','SK': 'Scandinavian Airlines',
                'TP': 'TAP Air Portugal','TK': 'Turkish Airlines',
                'W6': 'Wizz Air','U2': 'easyJet','FR': 'Ryanair',
                'A3': 'Aegean Airlines','SN': 'Brussels Airlines',
                'EK': 'Emirates','QR': 'Qatar Airways','IB': 'Iberia',
                'LH': 'Lufthansa'}

def get_carrier_input():
    # Loop ensures user keeps trying until a valid airline code is entered
    
    while True:
        print('')
        carrier_input = input("Enter a two-character Airline code to plot a histogram: ").upper()

        # If code exists in the dictionary, return the code and its full name
        if carrier_input in carrier_list:
            return carrier_input, carrier_list[carrier_input]
        else:
            print("Unavailable Airline code please try again.")

def create_chart(carrier_code, carrier_full_name, year_data, location_code, airport_full_name):

    # Creates a dictionary to count how many flights occur in each hour (0 to 11)
    hour_data = {}
    for hour in range(12):
        hour_data[hour] = 0 # Start all hours with a count of 0
        
    # Count flights for the chosen airline by looking at departure times
    for record in flight_records:
        if record[1].startswith(carrier_code):
            hour_value = int(record[2].split(':')[0])

            # Increase count only if hour is between 0–11
            if hour_value in hour_data:
                hour_data[hour_value] += 1
                
    # Set the size of the window used for drawing the graph
    chart_height = 680            
    chart_width = 1000
    chart_window = GraphWin('Airline Histogram', chart_width, chart_height)
    chart_window.setBackground('white')

    # Create and draw the heading text at the top of the window
    chart_heading = 'Departures by hour for ' + carrier_full_name + ' From ' + airport_full_name + ' ' + year_data
    heading_text = Text(Point(chart_width/2,50), chart_heading)
    heading_text.setSize(16)
    heading_text.setStyle('bold')
    heading_text.draw(chart_window)

    
    y_axis_label = Text(Point(50, chart_height/2), "Hours")
    y_axis_label.setSize(14)
    y_axis_label.setStyle("bold")
    y_axis_label.draw(chart_window)


    max_value = max(hour_data.values()) if hour_data.values() else 1
    if max_value == 0:
        max_value = 1 

    bar_gap = 45 
    left_padding = 120 
    
    for hour_index in range(12):
        flights_num = hour_data[hour_index]
        bar_position = 100 + (hour_index * bar_gap)
        
        bar_size = (flights_num / max_value) * 700
        
        hour_text = Text(Point(left_padding - 20, bar_position), str(hour_index))
        hour_text.setSize(11)
        hour_text.setStyle("bold")
        hour_text.draw(chart_window)
        
        if flights_num > 0:
            bar_rect = Rectangle(Point(left_padding, bar_position - 15), Point(left_padding + bar_size, bar_position + 15))
            bar_rect.setFill("pink")
            bar_rect.draw(chart_window)
            
            count_display = Text(Point(left_padding + bar_size + 40, bar_position), str(flights_num))
            count_display.setSize(11)
            count_display.setStyle("bold")
            count_display.draw(chart_window)

# Instruction for the user to close the graph window
    info_text = Text(Point(chart_width/2, 20), "Click anywhere to close the histogram")
    info_text.setSize(10)
    info_text.draw(chart_window)
    
    # Wait for a mouse click before closing
    chart_window.getMouse()
    chart_window.close()

#=======TASK E- main===========
def run_program():
    while True:  # Outer loop to allow the user to restart the program with a new file
        flight_records.clear() # Clear the previous flight records 
        
        location, selected_year, airport = get_user_input()
        
        analysis_results = process_data()

        
        # Get airline input and generate histogram chart
        airline_code, airline_full_name = get_carrier_input()
        create_chart(airline_code, airline_full_name, selected_year, location, airport)
        
        print("\n" + "="*50)

 #ask user if they want to select a new file
        while True:
            user_decision = input("Do you want to select a new data file? Y/N: ").upper()
            if user_decision == 'Y' or user_decision == 'N':
                break   #valid input; exit the loop
            else:
                print("Please enter Y or N")
        
        # Exit program if user selects 'N'
        if user_decision == 'N':
            print("\nThank you. End of run")
            break  
        else:
            print("\n" + "="*50)
            print("Selecting a new file...")
            print("="*50 + "\n")


 
            
# Entry point of the program
if __name__ == "__main__":
    run_program()
