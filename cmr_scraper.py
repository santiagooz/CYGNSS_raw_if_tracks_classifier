import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# Define the URL for the CMR (Common Metadata Repository)
url = "https://cmr.earthdata.nasa.gov/virtual-directory/collections/C2036882037-POCLOUD/temporal"

# Get the HTML response from the CMR URL
response = requests.get(url)

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links to files in the HTML
file_links = soup.find_all('a', href=True)
file_links0 = file_links[4:-6]

# Initialize caseID counter and a dictionary to store case information
caseID = 0
cases = {
    'caseID': [],
    'cygID': [],
    'start_date': [],
    'end_date': [],
}

# Iterate through file links
for file_link0 in file_links0:
    file_url = urljoin(url, file_link0['href'])
    response = requests.get(file_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    file_links = soup.find_all('a', href=True)
    file_links1 = file_links[5:-6]
    
    for file_link1 in file_links1:
        file_url = urljoin(url, file_link1['href'])
        response = requests.get(file_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        file_links = soup.find_all('a', href=True)
        file_links2 = file_links[6:-6]
    
        for file_link2 in file_links2:
            file_url = urljoin(url, file_link2['href'])
            response = requests.get(file_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            file_links = soup.find_all('a', href=True)
            file_links3 = file_links[7:-6]
        
            for file_link3 in file_links3:
                file_url = urljoin(url, file_link3['href'])

                # Check if the file URL ends with 'data.bin'
                if file_url[-8:] == 'data.bin':
                    # Extract information and append to the cases dictionary
                    cases['caseID'].append(caseID)
                    cases['cygID'].append(file_url[91:93])
                    cases['start_date'].append(file_url[102:106]+'-'+file_url[106:108]+'-'+file_url[108:110]+'T'+file_url[111:113]+':'+file_url[113:115]+':'+file_url[115:117]+'Z')
                    cases['end_date'].append(file_url[119:123]+'-'+file_url[123:125]+'-'+file_url[125:127]+'T'+file_url[128:130]+':'+file_url[130:132]+':'+file_url[132:134]+'Z')
                    caseID += 1
            print(cases['start_date'][-1])

# Save the cases dictionary to a JSON file
with open('cases.json', 'w') as json_file:
    json.dump(cases, json_file, indent=2)

# Uncomment the following lines if you want to save the data to a CSV file using pandas
# import pandas as pd
# cases_df = pd.DataFrame(cases)
# cases_df.to_csv('./Raw IF Cases.csv')
