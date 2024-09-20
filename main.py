from flask import Flask, render_template, request
import xarray as xr
import folium
import numpy as np
import pandas as pd
from folium.plugins import HeatMap

app = Flask(__name__)

# Load the dataset
dataset = xr.open_dataset('data/BERYL_test_data.nc_2')
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


def create_map(step_index):
    m = folium.Map(location=[0, 0], zoom_start=2)
    wind_speed = ws_data[step_index]

    heat_data = []

    for lat_idx in range(len(latitudes)):
        for lng_idx in range(len(longitudes)):
            if not np.isnan(wind_speed[lat_idx, lng_idx]):
                lat = latitudes[lat_idx]
                lon = longitudes[lng_idx]
                speed = float(wind_speed[lat_idx, lng_idx])
                heat_data.append([lat, lon, speed])
                folium.CircleMarker(
                    location=(lat, lon),
                    radius=5,
                    color='yellow' if speed >= 0 else 'red',
                    fill=True,
                    fill_color='yellow' if speed >= 0 else 'red',
                    fill_opacity=0.6,
                    popup=f'<p>Latitude: {lat}, Longitude: {lon}, Wind Speed: {speed:.2f} m/s</p>'
                ).add_to(m)

    HeatMap(heat_data, min_opacity=0.5, max_opacity=1.0, radius=5).add_to(m)

    folium.LatLngPopup().add_to(m)
    return m


@app.route('/')
def index():
    step = request.args.get('step', '0')  # Default to first step
    step_index = int(step)
    m = create_map(step_index)
    max_ws = np.nanmax(ws_data[step_index])

    return render_template(
        'index.html',
        map=m._repr_html_(),
        max_ws=float(max_ws),
        steps=step_labels,
        current_step=step
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
