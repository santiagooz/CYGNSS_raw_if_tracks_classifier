# NASA CMR Data Scraper, OpenDAP Data Extractor and Tracks Classifier
This set of Python scripts looks for all the available CYGNSS Level 1 Raw Intermediate Frequency Data Records, then extracts relevant parameters from their respective CYGNSS Level 1 Science Data Records metadata. Using those parameters it classifies the tracks by location of the CYGNSS satellites.


## CMR Data Scraper (`cmr_scraper.py`)

This script scrapes the NASA Common Metadata Repository (CMR) to extract information about available files in the CYGNSS Level 1 Raw Intermediate Frequency Data Records. It focuses on that specific collection with temporal data.

### Usage

1. Make sure you have the required libraries installed: `requests`, `beautifulsoup4`.
2. Execute the script (`cmr_scraper.py`).
3. The script will output information about each case, including `caseID`, `cygID`, `start_date`, and `end_date`.
4. The results are saved in a JSON file named `cases.json`.

## OpenDAP Data Extractor (`opendap_extractor.py`)

This script retrieves data from NASA's OpenDAP server for a specific set of cases. It utilizes the OpenDAP protocol to request and extract data.

### Usage

1. Ensure you have the required libraries installed: `requests`.
2. Execute the script (`opendap_extractor.py`).
3. The script reads case information from a JSON file (`cases.json`).
4. It performs OpenDAP requests for each case and extracts specified variables.
5. The extracted data is saved in a JSON file named `Raw IF cases parameters.json`.

## Track Classifier (`classify_tracks.py`)
This script visualizes the tracks from the extracted data on a map using Cartopy. It classifies tracks based on their location, distinguishing between tracks over the ocean and those within a specified rectangular region (Amazon basin). The classified information is saved in a JSON file named Raw_if_tracks_classified.json.

### Usage
1. Ensure you have the required libraries installed: cartopy, matplotlib, json, global_land_mask.
2. Execute the script (classify_tracks.py).
3. The script reads track information from a JSON file (Raw IF cases parameters.json).
4. It visualizes and classifies tracks based on their location, saving the results in Raw_if_tracks_classified.json.

### Additional Notes
- The OpenDAP requests include authentication with a specific username and password.
- The scripts assume a specific structure and format of the data available on the CMR and OpenDAP services.

Feel free to modify the scripts according to your specific use case or adapt them for other data sources.
