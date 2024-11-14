FastAPI Warehouse Distance API
This project is a FastAPI-based API to calculate the closest warehouse to a given destination using the Google Maps API.

Features
Calculates driving distances between a destination address (to_address) and multiple warehouse addresses (from_address).
Returns the closest warehouse based on the shortest driving distance.
Handles validation for empty or invalid addresses.
Prerequisites
Docker: Ensure you have Docker Desktop installed and running.
Google Maps API Key: You'll need a Google Maps API key to make distance calculations.
Setup Instructions
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
Create a .env File:

In the root directory, create a .env file with your Google Maps API key:

plaintext
Copy code
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
Replace your_google_maps_api_key with your actual API key.

Run the App Using Docker Compose:

Build and start the Docker container:

bash
Copy code
docker-compose up --build
The API will be accessible at http://localhost:8000.

API Endpoints
POST /closest-warehouse/
Request Body
to_address: The destination address (string).
from_address: A list of warehouse addresses, each with a warehouse_name and address.
Example request body:

json

{
   "to_address": "1600 Amphitheatre Parkway, Mountain View, CA",
   "from_address": [
     {
        "warehouse_name": "WH1",
        "address": "1 Infinite Loop, Cupertino, CA"
     },
     {
        "warehouse_name": "WH2",
        "address": "345 Spear St, San Francisco, CA"
     }
   ]
}

Response
Success: Returns the closest warehouse if all addresses are valid.
Error: Returns closest_warehouse as null with details on any invalid or missing addresses.
Example success response:

{
  "closest_warehouse": {
    "warehouse_name": "WH1",
    "address": "1 Infinite Loop, Cupertino, CA"
  }
}

Running Tests
Use tools like Postman or curl to test the endpoint at http://localhost:8000/closest-warehouse/.

Stopping the App
To stop the app, use Ctrl+C in the terminal where Docker is running or run:

bash
Copy code
docker-compose down
Notes
.gitignore: Add a .gitignore file to prevent .env and other sensitive or unnecessary files from being committed to Git.
Docker: The app runs on port 8000 locally, mapped to port 80 in the container.
