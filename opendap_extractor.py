import requests
from requests.auth import HTTPBasicAuth
import time
import json

def opendap_request(input_dict, cID, var_list):
    """
    Make an OpenDAP request and return the response.

    Parameters:
    - input_dict (dict): Dictionary containing input data.
    - cID (int): Case ID.
    - var_list (list): List of variables to retrieve.

    Returns:
    - requests.Response: Response object from the OpenDAP request.
    """
    time_res = 1
    if (int(input_dict['start_date'][cID][0:4]) >= 2019 and int(input_dict['start_date'][cID][5:7]) >= 7) or int(input_dict['start_date'][cID][0:4]) >= 2020:
        time_res = 0.5
    
    ds = input_dict['start_date'][cID][0:4] + input_dict['start_date'][cID][5:7] + input_dict['start_date'][cID][8:10]
    de = input_dict['end_date'][cID][0:4] + input_dict['end_date'][cID][5:7] + input_dict['end_date'][cID][8:10]

    start_idx = int((int(input_dict['start_date'][cID][11:13]) * 3600 + int(input_dict['start_date'][cID][14:16]) * 60 + int(input_dict['start_date'][cID][17:19])) / time_res)
    end_idx = int((int(input_dict['end_date'][cID][11:13]) * 3600 + int(input_dict['end_date'][cID][14:16]) * 60 + int(input_dict['end_date'][cID][17:19])) / time_res)
    
    interv = str(start_idx) + ":1:" + str(end_idx)

    url = f"https://opendap.earthdata.nasa.gov/collections/C2146321631-POCLOUD/granules/cyg{input_dict['cygID'][cID]}.ddmi.s{ds}-000000-e{de}-235959.l1.power-brcs.a31.d32.dap.csv?dap4.ce="
    
    for var in var_list:
        url += f"/{var}%5B{interv}%5D;"
    url = url[:-1]

    return requests.get(url, auth=HTTPBasicAuth('username', 'password'))

def add_to_dict(input_dict, response, cID, var_list):
    """
    Extract data from OpenDAP response and add it to the input dictionary.

    Parameters:
    - input_dict (dict): Dictionary to update with extracted data.
    - response (requests.Response): Response object from OpenDAP request.
    - cID (int): Case ID.
    - var_list (list): List of variables to extract.

    Returns:
    - int: Status indicating success (0) or failure (1).
    """
    atd_status = 0
    csv_init = str(response.content)
    for var in var_list:
        init_idx = csv_init.find(var) + len(var + ', ')
        end_idx = csv_init[init_idx:].find('\\n') + init_idx
        if init_idx == len(var + ', '):
            atd_status = 1
            break
        input_dict[var][cID] = [float(i) for i in csv_init[init_idx:end_idx].split(', ')] 
    return atd_status

# Load case data from JSON file
file_path = '.\cases.json'
with open(file_path, 'r') as json_file:
    case_dict = json.load(json_file)

num_cases = len(case_dict['caseID'])

cntr = 0
err_cntr = 0
start_time = time.time()

# List of variables to retrieve
var_list = ['ddm_timestamp_utc', 'ddm_timestamp_gps_week', 'ddm_timestamp_gps_sec', 'sc_pos_x', 'sc_pos_y', 'sc_pos_z', 'sc_vel_x', 'sc_vel_y', 'sc_vel_z', 'sc_roll', 'sc_pitch', 'sc_yaw', 'sc_lat', 'sc_lon', 'sc_alt']

# Initialize dictionary entries for variables
for var in var_list:
    case_dict[var] = [None] * num_cases 

# Iterate through cases
for cID in range(87, num_cases):
    response = opendap_request(case_dict, cID, var_list)
    
    if response.status_code == 200:
        atd_status = add_to_dict(case_dict, response, cID, var_list)
        
        # Retry if extraction fails
        num_try = 2
        while atd_status == 1:
            response = opendap_request(case_dict, cID, var_list)
            atd_status = add_to_dict(case_dict, response, cID, var_list)
            print(num_try)
            num_try += 1
    else:
        err_cntr += 1
    
    cntr += 1
    elapsed_time = time.time() - start_time
    remaining_time = ((elapsed_time / (cntr)) * (num_cases - cntr ))
    hours = int(remaining_time // 3600)
    minutes = int((remaining_time % 3600) // 60)
    seconds = int(remaining_time % 60)
    print(f'Time remaining: {hours} hours, {minutes} minutes, {seconds} seconds')

# Save output dictionary as JSON file
with open('Raw IF cases parameters.json', 'w') as json_file:
    json.dump(case_dict, json_file, indent=2)