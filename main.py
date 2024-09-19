from flask import Flask, render_template, request
import xarray as xr
import folium
import numpy as np
import pandas as pd
from folium.plugins import HeatMap

app = Flask(__name__)

# Load the dataset
dataset = xr.open_dataset('data/BERYL_test_data.nc 2')
print(dataset)
steps = dataset.step.values
latitudes = dataset.latitude.values
longitudes = dataset.longitude.values
ws_data = dataset.ws.values


def format_time_steps(steps):
    formatted_steps = []
    for ts in steps:
        td = pd.to_timedelta(ts)
        formatted_steps.append(str(td).split()[2])
    return formatted_steps


step_labels = format_time_steps(steps)


def create_map(step_index, lat=None, lng=None, wind_speed_value=None):
    m = folium.Map(location=[0, 0], zoom_start=2)
    wind_speed = ws_data[step_index]
    heat_data = [
        [latitudes[i], longitudes[j], float(wind_speed[i, j])]
        for i in range(len(latitudes))
        for j in range(len(longitudes))
        if not np.isnan(wind_speed[i, j]) and wind_speed[i, j] > 0
    ]
    HeatMap(heat_data, min_opacity=0.5, max_opacity=1.0, radius=5).add_to(m)

    if lat and lng:
        folium.Marker([lat, lng],
                      popup=f'Wind Speed: {wind_speed_value} m/s' if wind_speed_value is not None else 'No data available').add_to(
            m)

    folium.LatLngPopup().add_to(m)
    max_ws = np.nanmax(wind_speed)
    return m, max_ws


#

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get step index from query parameters or default to 0
    step = request.args.get('step', '0')  # GET method
    if request.method == 'POST':
        step = request.form.get('step', step)  # POST method

    step_index = int(step)
    lat = request.form.get('lat', None)
    lng = request.form.get('lng', None)
    wind_speed_value = None

    # Initialize indices
    lat_idx = None
    lon_idx = None

    if lat and lng:
        try:
            lat = float(lat)
            lng = float(lng)
            lat_idx = np.abs(latitudes - lat).argmin()
            lon_idx = np.abs(longitudes - lng).argmin()
            wind_speed_value = ws_data[step_index, lat_idx, lon_idx]
            if np.isnan(wind_speed_value):
                wind_speed_value = None
        except Exception as e:
            print(f"Error processing latitude and longitude: {e}")

    # Create map and calculate max wind speed
    m, max_ws = create_map(step_index, lat if lat else None, lng if lng else None, wind_speed_value)

    # Prepare wind speeds for different time steps
    wind_speeds = {}
    if lat_idx is not None and lon_idx is not None:
        for i in range(ws_data.shape[0]):
            wind_speeds[step_labels[i]] = ws_data[i, lat_idx, lon_idx] if not np.isnan(
                ws_data[i, lat_idx, lon_idx]) else 'No data'
    else:
        wind_speeds = {label: 'No data available' for label in step_labels}

    return render_template(
        'index.html',
        map=m._repr_html_(),
        max_ws=float(max_ws),
        steps=step_labels,
        current_step=step,
        wind_speed=wind_speed_value,
        lat=lat if lat else '',
        lng=lng if lng else '',
        wind_speeds=wind_speeds
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
