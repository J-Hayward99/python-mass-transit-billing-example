# Mass Transit Billing

## Table of Contents

- [Mass Transit Billing](#mass-transit-billing)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Versions](#versions)
  - [Main Features](#main-features)
  - [Build/Run Process](#buildrun-process)
    - [For Arguments Mode](#for-arguments-mode)
    - [For Config Mode](#for-config-mode)
  - [Notes](#notes)
  - [Assumptions](#assumptions)
  - [Fail-safes](#fail-safes)
  - [License](#license)

## Introduction

This is a journey calculator to determine the fees amount per "user",
the zone costs are hard coded however the program allow for stations to be
mapped via the zone_map.csv file.

## Requirements

- N/A

## Versions

- Python 3.10.6
- Windows 64-bit

## Main Features

- Uses CMD or bash arguments to run.
- Basic fee entry-exit system.
- Hard coded zone:price map.
- Can allocate stations to the zone map via CSV.
- Can calculate incomplete journeys with an incomplete fee.
- Can assign a base fee for starting a journey.

## Build/Run Process

- The program does not require to be built
- There are two modes of the program: Arguments and Config

### For Arguments Mode

- This is used via "[Program][use_arguments] = False" line in the config
- To run, open the terminal or command prompt in the root folder directory
  then type (without quotation marks):

```
python my_solution.py <zones_file_path> <journey_data_path> <output_file_path>
```

Where the angled brackets represent the paths.

- Note that in some Linux systems, "python" may have to be replaced with
  "python3"

### For Config Mode

- This is used via "[Program][use_arguments] = True" line in the config
- Run the code as:

```
python main.py
```

- Edit the values via the config

## Notes

- WARNING: listing the output.csv path to an already existing file will remove
           the original file.

## Assumptions

- A new day will inherently start with the direction being IN.
- In the case that you reached the daily cap or are near the cap, incomplete
  journeys will take you to the cap instead of over.
- Dates are in YYYY-MM-DD(timeinfo) standard.
- Zone maps and Journey data files have headers.
- The base fee included on entry

## Fail-safes

- If time is missing, it will default to the previous row's time.
- If station name is corrupt, zone_fee defaults to 0.
- Missing names (either due to no name or corruption) default to _MISSING_.
- Names with non-regular characters will be filtered by RegEx.
- Default case for corrupted directions (IN/OUT) to be be OUT.

## License

Distributed under the MIT License. See LICENSE.txt for more information.
