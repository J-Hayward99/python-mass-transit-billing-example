# LEGAL AND DOCUMENTATION
# Copyright (c) 2023 James Hayward


# DESCRIPTION
"""
    _summary_


"""


# NOTES
"""
    _notes_

"""


# IMPORTS
# Official Modules


# Personal Modules
import libs.included_tools as included


# CONSTANTS
# Included
PROJECT_NAME        = included.get_config_value("Metadata", "project_name")         # What is the title of the program
PROJECT_AUTHOR      = included.get_config_value("Metadata", "project_author")       # Who made the file
PROJECT_YEAR        = included.get_config_value("Metadata", "project_year")         # What is the current year

PROJECT_VERSION     = included.get_config_value("Metadata", "project_version")      # What is the current version

# Paths


# Values


# LOOK-UP TABLES


# HASHMAPS
# Initiation


# Hard-coded Hashmaps


# GLOBAL VARIABLES


# MAIN PIPELINE
def main_pipeline():                                                                # This is the main pipeline of what the code runs
    # INITIATE PROGRAM
    print(f"=== {PROJECT_NAME.upper()} ===")                                        #   # Program name
    print(f"Written by {PROJECT_AUTHOR}, {PROJECT_YEAR}")                           #   # Program details
    print()
    print(f"BOOT: Version -> {PROJECT_VERSION}")                                    #   # Program version

    
    # CHECK PIPELINE
    check_pipeline()                                                                #   # This is used to check, leave as pass if not needed

    
    # PROGRAM PIPELINE
    program_pipeline()
    

    # SCRIPT SHUTDOWN
    print("MAIN: Program Finished")


def check_pipeline():                                                               # This is the pipeline that runs checks if required
    # INITIALISE
    print("CHCK: Running Checks")

    # CHECK FILES
    included.run_file_check(".checks")                                              #   # Ensures all files and folders are present


def program_pipeline():                                                             # Runs the program proper
    # INITIATION
    # Prompt
    print("MAIN: Running Program")


    # PROGRAM PROPER


    # PROGRAM SHUTDOWN



# CLASSES


# FUNCTIONS
# Pipeline Functions


# Utility Functions


# MAIN
if __name__ == '__main__':
   main_pipeline()                                                                  # Runs the main pipeline



# PLAN
"""
    _plan_

"""
