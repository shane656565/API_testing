import BFM136_1
import BFM136_2
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_data_for_line(line_number, real_time_data):
    """ Helper function to extract specific line data based on line_number. """
    line_data = {}
    print(line_number)
    if line_number == '1' or '4':
        keys = ["V1Eu", "I1Eu", "kW1Eu", "kvar1Eu", "kVA1Eu",
                "PF1Eu", "V1AngEu", "I1AngEu", "V1THDEu", "I1THDEu", "I1TDDEu"]
    elif line_number == '2' or '5':
        keys = ["V2Eu", "I2Eu", "kW2Eu", "kvar2Eu", "kVA2Eu",
                "PF2Eu", "V2AngEu", "I2AngEu", "V2THDEu", "I2THDEu", "I2TDDEu"]
    elif line_number == '3' or '6':
        keys = ["V3Eu", "I3Eu", "kW3Eu", "kvar3Eu", "kVA3Eu",
                "PF3Eu", "V3AngEu", "I3AngEu", "V3THDEu", "I3THDEu", "I3TDDEu"]
    else:
        return None

    for key in keys:
        line_data[key] = real_time_data[key]

    return line_data


@app.route("/api/Scarborough/<line>", methods=["GET"])
def get_single_phase_data(line):
    real_time1 = BFM136_1.RealTimeMeasurement()
    real_time2 = BFM136_2.RealTimeMeasurement()
    real_time_data1 = real_time1.DataArray()
    real_time_data2 = real_time2.DataArray()
    if line == "1" or "2" or "3":
        data = get_data_for_line(line, real_time_data1)
    elif line == "4" or "5" or "6":
        data = get_data_for_line(line, real_time_data2)
    else:
        return

    if data is not None:
        return jsonify(data)
    else:
        return jsonify({"error": f"Invalid line number {line}."}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
