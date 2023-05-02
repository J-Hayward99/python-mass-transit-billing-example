# This folder is used to hold the code that's inherent to the project

# IMPORTS
import configparser                                                                 # For the config function
import os                                                                           # Checking existence of files
import sys                                                                          # For exiting the program if the checks fail

# CODE
def run_file_check(check_file_name:str) -> None:                                    # Checks the list of files to ensure all are there
    # INITIALISE
    flag_missing_files = False                                                      #   # Flag that triggers if there's a missing file
    list_missing_files = []                                                         #   # Archives a list of missing files

    # OPEN FILE
    with open(check_file_name, "r") as file:
        # LINES TO LIST
        file_lines = file.readlines()

        # CHECK LINES
        for line in file_lines:
            # REMOVE NEWLINE SPECIAL CHARACTER
            line = line.strip("\n")
            
            # CONDITIONS
            # If the Line is Empty
            if line == "":
                continue

            # If the Line is a Comment
            if line.strip().startswith("#"):                                        #   # Removes whitespace then checks if the first is #
                continue
            
            # GET EXISTENCE
            existence = os.path.exists(line)                                        #   # Checks the existence of the file

            # FLAG TRIGGER OF MISSING FILES
            if not existence:                                                       #   # If the files are missing
                flag_missing_files = True
                list_missing_files.append(line)

            
            # PRINT THE EXISTANCE OF FILE
            if get_config_value("Included", "show_checks") == "True":
                print(f"CHCK: Existence of \"{line}\" -> {existence}")
        
        # MISSING TRIGGER
        if flag_missing_files:
            # STATE ISSUE
            print("CHCK: Failed Check -> Missing Files")
            
            # LIST FILE
            for file in list_missing_files:
                print(f"CHCK: Missing File -> \"{file}\"")
            
            # SHUTS DOWN PROGRAM
            sys.exit("CHCK: Stopping Program")
        
        print("CHCK: Checks Passed")




def get_config_value(section:str, value:str) -> str:                                # Streamlines the config value acquisition
    # CONFIG INITIATION
    config = configparser.ConfigParser()                                            #   # Initiates Parser
    config.read("config.ini")                                                       #   # Hardcoded config.ini file

    # RETURN
    return config[section][value].strip("\"")                                       #   # Removes un-needed ""
