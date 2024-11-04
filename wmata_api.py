import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "347c3ebca3ad4ae48143dfd83348994d"
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# Get incidents by machine type (elevators/escalators)
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    # Create an empty list to store incidents
    incidents = []

    # Send a GET request to the WMATA Incidents API
    response = requests.get(INCIDENTS_URL, headers=headers)

    if response.status_code != 200:
        return json.dumps({"error": "Failed to fetch data from WMATA API"}), response.status_code

    # Get the JSON data from the response
    data = response.json()

    # Find incidents matching the specified unit type
    matching_incidents = []
    for incident in data.get("ElevatorIncidents", []):
        if incident.get("UnitType"):
            matching_incidents.append(incident)

    # Create a dictionary for each matching incident with specific fields
    for incident in matching_incidents:
        if (unit_type == "elevators" and incident["UnitType"].upper() == "ELEVATOR") or \
                (unit_type == "escalators" and incident["UnitType"].upper() == "ESCALATOR"):
            incident_data = {
                "StationCode": incident.get("StationCode"),
                "StationName": incident.get("StationName"),
                "UnitType": incident.get("UnitType"),
                "UnitName": incident.get("UnitName")
            }
            # Add each incident dictionary to the list
            incidents.append(incident_data)

    # Return the list of incidents as a JSON string
    return json.dumps(incidents)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

# http://127.0.0.1:5000/incidents/elevators
# http://127.0.0.1:5000/incidents/escalators
