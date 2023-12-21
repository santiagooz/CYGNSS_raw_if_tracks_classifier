import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import json
from global_land_mask import globe

def is_in_region(lat, lon, region_bounds):
    # Check if the point is inside the specified rectangular region
    cntr = 0
    for ii in range(len(lat)):
        if (
                region_bounds['min_lon'] <= lon[ii] <= region_bounds['max_lon'] and
                region_bounds['min_lat'] <= lat[ii] <= region_bounds['max_lat']
                ):
            cntr += 1
    return cntr/len(lat) >= .5

def is_in_ocean(lat, lon):
    # Check if the point is over the ocean
    lon = [(x + 180) % 360 - 180 for x in lon]
    in_ocean = globe.is_ocean(lat, lon)
    return all(in_ocean)

# Load case data from JSON file
file_path = '.\Raw IF cases parameters.json'
with open(file_path, 'r') as json_file:
    tracks_info = json.load(json_file)

# Define the rectangular region boundaries (Amazon basin)
region_bounds = {'min_lon': 280.934248, 'max_lon': 315.944166, 'min_lat': -11.689748, 'max_lat': 4.341730}

# Create a GeoAxes with the PlateCarree projection
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

# Initialize surface information for each track
tracks_info['surface'] = [None] * len(tracks_info['caseID']) 
ocean_idx = []
region_idx = []

# Plot tracks based on location and region
for cID in range(len(tracks_info['caseID'])):
    if tracks_info['sc_lat'][cID] is not None:
        aux_lat = tracks_info['sc_lat'][cID]
        aux_lon = tracks_info['sc_lon'][cID]

        if is_in_ocean(aux_lat, aux_lon):
            ax.scatter(aux_lon, aux_lat, s=1, color='red', marker='o', label=f'Track {cID}')
            tracks_info['surface'][cID] = 'ocean'
            ocean_idx.append(cID)

        if is_in_region(aux_lat, aux_lon, region_bounds):
            ax.scatter(aux_lon, aux_lat, s=1, color='green', marker='o', label=f'Track {cID}')
            tracks_info['surface'][cID] = 'Amazon basin'
            region_idx.append(cID)

# Add map features
ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.LAKES)
ax.add_feature(cfeature.RIVERS)

# Set plot title and legend
ax.set_title('Tracks Plot')
ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())

# Show the plot
plt.show()


# Save output dictionary as JSON file
with open('Raw_if_tracks_classified.json', 'w') as json_file:
    json.dump(tracks_info, json_file, indent=2)