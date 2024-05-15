import BFM136_1
import BFM136_2
import BFM136_3
import BFM136_4
import BFM136_5
import BFM136_6
import BFM136_7
import BFM136_8
import BFM136_9
import BFM136_10
import BFM136_11
import BFM136_12
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
modules = [
    BFM136_1, BFM136_2, BFM136_3, BFM136_4, BFM136_5, BFM136_6,
    BFM136_7, BFM136_8, BFM136_9, BFM136_10, BFM136_11, BFM136_12
]


def get_data_for_line(line_number, real_time_data):
    """ Helper function to extract specific line data based on line_number. """
    line_data = {}

    # Determine the set of keys based on the line_number
    if line_number in ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34']:
        keys = ["V1Eu", "I1Eu", "kW1Eu", "kvar1Eu", "kVA1Eu",
                "PF1Eu", "V1AngEu", "I1AngEu", "V1THDEu", "I1THDEu", "I1TDDEu"]
    elif line_number in ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32']:
        keys = ["V2Eu", "I2Eu", "kW2Eu", "kvar2Eu", "kVA2Eu",
                "PF2Eu", "V2AngEu", "I2AngEu", "V2THDEu", "I2THDEu", "I2TDDEu"]
    elif line_number in ['3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33']:
        keys = ["V3Eu", "I3Eu", "kW3Eu", "kvar3Eu", "kVA3Eu",
                "PF3Eu", "V3AngEu", "I3AngEu", "V3THDEu", "I3THDEu", "I3TDDEu"]
    else:
        return None

    for key in keys:
        line_data[key] = real_time_data.get(key, None)

    return {'line_number': line_number, 'line_data': line_data}


@app.route("/api/Scarborough/<line>", methods=["GET"])
def get_single_phase_data(line):
    # Convert the line number to an integer for calculations
    try:
        line_number = int(line)
    except ValueError:
        return jsonify({"error": f"Invalid line number {line}."}), 404

    if 1 <= line_number <= 36:
        module_index = (line_number - 1) // 3
        module = modules[module_index]

        real_time_data = module.RealTimeMeasurement().DataArray()
        data = get_data_for_line(str(line_number), real_time_data)
    else:
        return jsonify({"error": f"Line number {line} out of range."}), 404

    if data is not None:
        return jsonify(data)
    else:
        return jsonify({"error": f"Data not found for line number {line}."}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
