# LEGAL AND DOCUMENTATION
# Copyright (c) 2023 James Hayward


# IMPORTS
# Official Modules
import argparse                                                                     # Used for command-line arguments
import csv                                                                          # Used for writing and reading the CSV files
import os                                                                           # Used for checking output existence
import re                                                                           # Used for Regular Expressions
import sys                                                                          # Used for system exit

# Personal Modules
import libs.included_tools as inc


# CONSTANTS
# Included
PROJECT_NAME        = inc.get_config_value("Metadata", "project_name")              # What is the title of the program
PROJECT_AUTHOR      = inc.get_config_value("Metadata", "project_author")            # Who made the file
PROJECT_YEAR        = inc.get_config_value("Metadata", "project_year")              # What is the current year

PROJECT_VERSION     = inc.get_config_value("Metadata", "project_version")           # What is the current version

# Paths
ZONE_MAP            = ""
JOURNEY_DATA        = ""
OUTPUT              = ""

# Clarity Cosntants
TOTAL_BILLING               = 0                                                     # These are used for clarity with user generation
INCOMPLETE_JOURNEY_STATUS   = False
DAY_TAB                     = 0
MONTH_TAB                   = 0
JOURNEY_TAB                 = 0

# Initiation
BASE_FEE                    = 0                                                     # Base fee for engaging with transit
INCOMPLETE_FEE              = 0                                                     # Fee for having an incomplete journey by midnight
DAILY_CAP                   = 0                                                     # The cap for how much you can pay for a day
MONTHLY_CAP                 = 0                                                     # The cap for how much you can pay for a month


# HASHMAPS
# Initiation
hashmap_zone_price      = {}                                                        # This is used to hold the zone pricing
hashmap_station_zone    = {}                                                        # This is used to hold the "Station : Fee" Hashmap
hashmap_user_data       = {}                                                        # Stores user data


# MAIN PIPELINE
def main_pipeline():                                                                # This is the main pipeline of what the code runs
    # INITIATE PROGRAM
    print(f"=== {PROJECT_NAME.upper()} ===")                                        #   # Program name
    print(f"Written by {PROJECT_AUTHOR}, {PROJECT_YEAR}")                           #   # Program details
    print()
    print(f"BOOT: Version -> {PROJECT_VERSION}")                                    #   # Program version

    
    # CHECK PIPELINE
    check_pipeline()                                                                #   # This is used to check, leave as pass if not needed
    get_paths()
    load_config_data()
    check_paths()
    
    # PROGRAM PIPELINE
    program_pipeline()
    

    # SCRIPT SHUTDOWN
    print("MAIN: Program Finished")


def check_pipeline():                                                               # This is the pipeline that runs checks if required
    # INITIALISE
    print("CHCK: Running Checks")

    # CHECK FILES
    inc.run_file_check(".checks")                                                   #   # Ensures all files and folders are present


def program_pipeline():                                                             # Runs the program proper
    # INITIATION
    # Prompt
    print("MAIN: Running Program")


    # PROGRAM PROPER
    # INITIATE
    # Arrays
    array_zone_map      = []                                                        #   # Initation for zone_map.csv array
    array_journey_data  = []                                                        #   # Initation for journey_data.csv array
    array_output_data   = []                                                        #   # Used to hold and sort the output data before output.csv

    # Variables
    current_row_day     = ""                                                        #   # These are for the journey_data handling
    current_row_month   = ""
    previous_row_day    = ""
    previous_row_month  = ""

    print("MAIN: - Initiated Variables")
    # Load the Zone Map into Memory
    print("MAIN: - Loading Zone Map to Hashmap")
    with open(ZONE_MAP, "r") as csvfile_zone_map:
        # Reader
        csv_reader = csv.reader(csvfile_zone_map)

        # Skip Header
        next(csv_reader, None)                                                      #   # The reader is an iterable

        # Append Rows to Array
        for row in csv_reader:
            array_zone_map.append(row)
    print("MAIN: - Loaded Zone Map to Hashmap")

    # Convert Stations into "Station : Fee" Hashmap
    print("MAIN: - Converting Stations to Station : Fee Hashmap")
    for row in array_zone_map:
        # Initate Variables
        station_name    = row[0]
        station_zone    = row[1]
        station_fee     = 0
        
        # CHECKS
        # Zone Out of Bounds
        if hashmap_zone_price.get(station_zone) == None:
            station_zone = "6"                                                      #   # if zone is not in the zone-price hashmap, default to zone 6

        # Compile Hashmap
        station_fee = hashmap_zone_price.get(station_zone)                          #   # Gets the fee from the hashmap
        hashmap_station_zone[station_name] = station_fee                            #   # Adds item to hashmap with key=station_name & value=zone_fee
    
    # Load the Journey Data into Memory
    print("MAIN: - Loading Journey Data into Memory")
    with open(JOURNEY_DATA, "r") as csvfile_zone_map:
        # Reader
        csv_reader = csv.reader(csvfile_zone_map)

        # Skip Header
        next(csv_reader, None)                                                      #   # The reader is an iterable

        # Append Rows to Array
        for row in csv_reader:
            array_journey_data.append(row)
    
        # Acquire First Day
        current_row_day     = array_journey_data[0][3][8:10]                        #   # Gets the first day mentioned
        current_row_month   = array_journey_data[0][3][5:7]                         #   # Gets the first month mentioned


    # JOURNEY_DATA HANDLING
    print("MAIN: - Handling Journey Data")
    for row in array_journey_data:
        # INITIATION
        # Retain Previous Day
        previous_row_day    = current_row_day                                       #   # Placed here to avoid first iteration bugs
        previous_row_month  = current_row_month

        # Dates
        current_row_day     = row[3][8:10]                                          #   # Gets yyyy-mm-DD
        current_row_month   = row[3][5:7]                                           #   # Gets yyyy-MM-dd

        # Clarity Variables
        row_user        = regexify(row[0])                                          #   # Clarity variable
        row_direction   = row[2]                                                    #   # Clarity direction
        zone_fee        = hashmap_station_zone.get(row[1])                          #   # Gets the zone fee
        
        new_day     = (current_row_day != previous_row_day)                         #   # Clarity Variable for new day
        new_month   = (current_row_month != previous_row_month)                     #   # Clarity Variable for new month
        
        
        # CHECKS
        # Missing name
        if row_user == "":                                                          #   # If there is no name
            row_user = "_MISSING_"                                                  #   # Default missing name

        # Missing Station
        if zone_fee == None:
            zone_fee = 0                                                            #   # If the station is missing, set the fee to 0
        
        # Missing Time
        if (regexify_number(current_row_day) == "" 
            or regexify_number(current_row_month) == ""):
            new_day             = False
            new_month           = False
            current_row_day     = previous_row_day
            current_row_month   = previous_row_month
        
        # User Existence
        if hashmap_user_data.get(row_user) == None:                                 #   # Checks if user is already in system, if not generate
            hashmap_user_data[row_user] = [
                TOTAL_BILLING,                                                      #   # Default 0
                INCOMPLETE_JOURNEY_STATUS,                                          #   # Default True, as generation infers first journey started
                JOURNEY_TAB,                                                        #   # Tracks the total price for the jounrey, Default 0
                DAY_TAB,                                                            #   # Tracks the total price for the day, Default 0
                MONTH_TAB                                                           #   # Tracks the total price for the month, Default 0
            ]

        # Incomplete Journeys
        if new_day or new_month:                                                    #   # Gets checked the next day
            if hashmap_user_data[row_user][1]:                                      #   # If the journey is incomplete
                hashmap_user_data[row_user][3] += hashmap_user_data[row_user][2]    #   # Adds the incomplete fee as the journey
                hashmap_user_data[row_user][2]  = 0                                 #   # Resets the journey tab

        # Daily Cap Overflow Check
        if hashmap_user_data[row_user][3] >= DAILY_CAP:                             #   # If the daily cap is reached
            hashmap_user_data[row_user][3] = DAILY_CAP                              #   # Set daily amount to the cap (avoid going over cap)

        # Monthly Cap Overflow Check
        if hashmap_user_data[row_user][4] >= MONTHLY_CAP:                           #   # If the daily cap is reached
            hashmap_user_data[row_user][4] = MONTHLY_CAP                            #   # Set daily amount to the cap (avoid going over cap)
                    

        # New Day Transfer
        if new_day:
            for user in hashmap_user_data:
                hashmap_user_data[user][4] += hashmap_user_data[user][3]            #   # Adds the daily to the monthly
                hashmap_user_data[user][3]  = 0                                     #   # Resets the daily_amount

        # New Month Transfer
        if new_month:
            for user in hashmap_user_data:
                hashmap_user_data[user][0] += hashmap_user_data[user][4]            #   # Adds the monthly_amount to the bill
                hashmap_user_data[user][4]  = 0                                     #   # Resets the monthly_amount
        

        # JOURNEY PROPER
        # Direction Handling
        if row_direction == "IN":
            hashmap_user_data[row_user][1]  = True                                  #   # Enables the incomplete journey boolean
            hashmap_user_data[row_user][2] += BASE_FEE + zone_fee                   #   # Add base fee + entry fee
    
        else:                                                                       #   # Direction=OUT, but also default case in case of corruption
            hashmap_user_data[row_user][1]  = False                                 #   # Reset the boolean
            hashmap_user_data[row_user][2] += zone_fee                              #   # Add the exit fee
            hashmap_user_data[row_user][3] += hashmap_user_data[row_user][2]        #   # Add entire journey to the daily tab
            hashmap_user_data[row_user][2]  = 0                                     #   # Reset Journey


    # FINAL ACTIONS
    # Push All Daily and Monthly Tabs to Total Billing
    print("MAIN: - Finalising Billing")
    for user in hashmap_user_data:
        # Assume All Incomplete Journeys are Incomplete
        if hashmap_user_data[user][1] == True:                                      #   # If the journey is incomplete
            hashmap_user_data[user][2] = INCOMPLETE_FEE                             #   # Adds an incomplete fee

        # Push Remaining Journey Tabs to Daily
        hashmap_user_data[user][3] += hashmap_user_data[user][2]

        # Daily Cap Overflow Check
        if hashmap_user_data[row_user][3] >= DAILY_CAP:                             #   # If the daily cap is reached
            hashmap_user_data[row_user][3] = DAILY_CAP                              #   # Set daily amount to the cap (avoid going over cap)

        # Monthly Cap Overflow Check
        if hashmap_user_data[row_user][4] >= MONTHLY_CAP:                           #   # If the daily cap is reached
            hashmap_user_data[row_user][4] = MONTHLY_CAP                            #   # Set daily amount to the cap (avoid going over cap)
                    
        # Daily Tab Clear
        hashmap_user_data[user][4] += hashmap_user_data[user][3]                    #   # Adds the daily to the monthly
        hashmap_user_data[user][3]  = 0                                             #   # Resets the daily_amount

        # Monthly Tab Clear
        hashmap_user_data[user][0] += hashmap_user_data[user][4]                    #   # Adds the monthly_amount to the bill
        hashmap_user_data[user][4]  = 0                                             #   # Resets the monthly_amount

    # Append and Sort Output Array in Ascending Order
    print("MAIN: - Sorting Data")
    for user in hashmap_user_data:                                                  #   # I could do this after Python 3.7 but safer to do this way
        user_fee = hashmap_user_data[user][0]                                       #   # Clarity
        array_output_data.append([user, round(user_fee, 2)])                        #   # Appends new row to array
    
    array_output_data.sort(key=lambda row:row[0])                                   #   # Sorts the array by the order of the first column of the rows


    # WRITE TO OUTPUT.CSV
    # Check for Existence
    print("MAIN: - Writing Output")
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)

    # Write Output
    with open(OUTPUT, "w") as csvfile_output:
        # Reader
        csv_writer = csv.writer(csvfile_output)

        # Write Rows to CSV
        for row in array_output_data:
            csv_writer.writerow(row)
    print("MAIN: - Wrote Output")

    # SHUTDOWN
    if inc.get_config_value("Program", "print_output") == "True":
        with open(OUTPUT, "r") as file:
            # Reader
            output_reader = csv.reader(file)

            print("MAIN: Output Printout")
            print("MAIN: User\t| Billing")
            for row in output_reader:
                if row == []:                                                       #   # Empty row check
                    continue
                
                print(f"MAIN: {row[0]}\t| {row[1]}")





# FUNCTIONS
# Pipeline Functions
def get_paths():
    print("LOAD: Loading Paths")

    # GLOBALS
    global ZONE_MAP
    global JOURNEY_DATA
    global OUTPUT

    if inc.get_config_value("Program", "use_arguments") == "True":
        # PROMPT
        print("LOAD: - Loading Paths via Arguments")
        
        # ARGUMENT HANDLING
        # Initiate Parser
        parser = argparse.ArgumentParser(
        usage=("%(prog)s "
               + "<zones_file_path> <journey_data_path> <output_file_path>"),
        exit_on_error=False
        )

        # Add Arguments
        parser.add_argument("zones_file_path")
        parser.add_argument("journey_data_path")
        parser.add_argument("output_file_path")

        arguments = parser.parse_args()

        # Update Paths
        ZONE_MAP        = arguments.zones_file_path
        JOURNEY_DATA    = arguments.journey_data_path
        OUTPUT          = arguments.output_file_path
        print("LOAD: - Loaded Paths")

    else:
        print("LOAD: - Loading Paths via Config")
        ZONE_MAP        = inc.get_config_value("Paths", "zone_map")
        JOURNEY_DATA    = inc.get_config_value("Paths", "journey_data")
        OUTPUT          = inc.get_config_value("Paths", "output")
        print("LOAD: - Loaded Paths")
    

def load_config_data():
    print("LOAD: Loading Config Data")
    # GLOBALS
    global hashmap_zone_price
    
    global DAILY_CAP
    global MONTHLY_CAP
    
    global BASE_FEE
    global INCOMPLETE_FEE

    # ZONE PRICE
    hashmap_zone_price = {
        "1" : get_zone_price("zone_one"),
        "2" : get_zone_price("zone_two"),
        "3" : get_zone_price("zone_three"),
        "4" : get_zone_price("zone_four"),
        "5" : get_zone_price("zone_five"),
        "6" : get_zone_price("zone_six_plus")
    }
    print("LOAD: - Loaded Zone Price Data")

    # CAPS
    print("LOAD: - Loading Cap Data")
    DAILY_CAP           = get_cap_prices("daily_cap")
    MONTHLY_CAP         = get_cap_prices("monthly_cap")
    print("LOAD: - Loaded Caps Data")

    # FEES
    print("LOAD: - Loading Fees Data")
    BASE_FEE            = get_fee_prices("fee_base")
    INCOMPLETE_FEE      = get_fee_prices("fee_incomplete")
    print("LOAD: - Loaded Fees Data")

    # FINISHED
    print("LOAD: Finished Loading Config Data")

def check_paths():
    check_path_existance(ZONE_MAP)                                                  #   # Ensures the zone map exists
    check_path_existance(JOURNEY_DATA)                                              #   # Ensures the journey data exists


# Utility Functions
def get_zone_price(zone_name:str) -> float:
    return inc.convert_config_type("Zone Prices", zone_name, "float")

def get_cap_prices(price_name:str) -> float:
    return inc.convert_config_type("Cap Prices", price_name, "float")

def get_fee_prices(price_name:str) -> float:
    return inc.convert_config_type("Fee Prices", price_name, "float")

def regexify(text: str) -> str:                                                     # This is used to ensure that inputted data is safe
    return re.sub(r"[^\w]", "", text.encode("ascii", "ignore").decode())            #   # Removes any char that's not a-z, A-Z, 0-9, or _

def regexify_number(text: str) -> str:                                              # This is used to ensure that inputted data is safe
    return re.sub(r"[^0-9]+$", "", text)                                            #   # Removes any char that's not 0-9

def check_path_existance(path:str):
    if not os.path.exists(path):
        sys.exit(f"ERROR: Missing Path -> \"{path}\"")


# MAIN
if __name__ == '__main__':
   main_pipeline()                                                                  # Runs the main pipeline

