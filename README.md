
# Wind Speed Map

This project is a web application that visualizes wind speed data using interactive maps. The application reads wind speed data from a NetCDF file, processes it, and displays it on a web map using Flask and Docker.
Clicking on the windspeed layer on the map displays the windspeed with the corresponding latitude and longitude.

## Project Structure

- `main.py`: The main Flask application script.
- `templates/index.html`: The HTML template for the web application.
- `data/BERYL_test_data.nc 2`: Dataset file
- `Dockerfile`: Dockerfile for building the Docker image.
- `requirements.txt`: Python dependencies for the project.

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/wind-speed-visualization.git
cd wind-speed-map
```

### Set Up Python Environment

Create a virtual environment and install the required packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Running the Application Locally

To run the Flask application locally, use:

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000/`.

## Docker Setup

### Build the Docker Image

```bash
docker build -t wind-speed-visualization .
```

### Run the Docker Container

```bash
docker run -p 5000:5000 wind-speed-visualization
```

The application will be available at `http://127.0.0.1:5000/`.

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000/`.
2. The interactive map will display wind speeds for different time steps.
3. Use the dropdown menu to select between 6 AM and 9 AM data.

## Pushing Docker Image to Docker Hub

1. **Log in to Docker Hub:**

   ```bash
   docker login
   ```

2. **Tag the Docker Image:**

   ```bash
   docker tag wind-speed-map your-username/wind-speed-visualization:latest
   ```

3. **Push the Docker Image:**

   ```bash
   docker push your-username/wind-speed-visualization:latest
   ```

