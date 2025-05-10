# Copyright (c) 2025 James Hayward

# IMPORTS
import argparse
import csv
import os
import re
import sys


# MAIN PIPELINE
if __name__ == "__main__":
    # Get Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("zone_prices")
    parser.add_argument("station_zones")
    parser.add_argument("user_data")
