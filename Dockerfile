# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . .

# Step 4: Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the port the app runs on
EXPOSE 5000

# Step 6: Define environment variable
ENV FLASK_APP=main.py

# Step 7: Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]

