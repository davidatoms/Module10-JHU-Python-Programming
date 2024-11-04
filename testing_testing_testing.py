import json
import requests
from flask import Flask, jsonify

# API endpoint URL's and access keys
WMATA_API_KEY = "347c3ebca3ad4ae48143dfd83348994d"
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

app = Flask(__name__)

@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    # create an empty list called 'incidents'
    incidents = []

    try:
        # Make the API request
        response = requests.get(INCIDENTS_URL, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        # iterate through the JSON response and retrieve all incidents matching 'unit_type'
        for incident in data['ElevatorIncidents']:
            if incident['UnitType'].lower() == unit_type.lower():
                incident_dict = {
                    'StationCode': incident['StationCode'],
                    'StationName': incident['StationName'],
                    'UnitType': incident['UnitType'],
                    'UnitName': incident['UnitName']
                }
                incidents.append(incident_dict)

        return jsonify(incidents)  # Use Flask's jsonify for proper JSON response

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except KeyError as e:
        return jsonify({'error': f'Invalid response format: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

# Add a root route to show basic instructions
@app.route("/", methods=["GET"])
def index():
    return '''
    <h1>WMATA Elevator/Escalator Incidents API</h1>
    <p>Available endpoints:</p>
    <ul>
        <li>/incidents/elevator - Get all elevator incidents</li>
        <li>/incidents/escalator - Get all escalator incidents</li>
    </ul>
    '''

if __name__ == '__main__':
    app.run(debug=True)
