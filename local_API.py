from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Mapping of identifiers to device IP/line
IPmap = {
    1: "192.168.8.1/1",
    2: "192.168.8.1/2",
    3: "192.168.8.1/3",
    4: "192.168.8.1/4",
    5: "192.168.8.1/5",
    6: "192.168.8.1/6"
}
DEVICE_PORT = "5005"
DEVICE_API_PATH = "/api/Scarborough"


def fetch_data_from_device(device_ip, line):
    """Fetch data from a single device for a specific line."""
    url = f"http://{device_ip}:{DEVICE_PORT}{DEVICE_API_PATH}/{line}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch data from {device_ip}/{line}: {str(e)}")
        return {"error": str(e)}


@app.route('/api/combined-data', methods=['GET'])
def get_combined_data():
    """Endpoint to get combined data based on the customer number from the IPmap."""
    customer_number = request.args.get('customerNumber', type=int)
    if customer_number not in IPmap:
        return jsonify({"error": "Invalid customer number."}), 400

    device_ip, line = IPmap[customer_number].split('/')
    data = fetch_data_from_device(device_ip, line)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
