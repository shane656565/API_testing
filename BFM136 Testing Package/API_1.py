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


def get_data_for_line(line_number, real_time_data):
    """ Helper function to extract specific line data based on line_number. """
    line_data = {}

    # Correct the logic to check line_number correctly
    if line_number in ['1', '4', '7', '10', '13', '16']:
        keys = ["V1Eu", "I1Eu", "kW1Eu", "kvar1Eu", "kVA1Eu",
                "PF1Eu", "V1AngEu", "I1AngEu", "V1THDEu", "I1THDEu", "I1TDDEu"]
    elif line_number in ['2', '5', '8', '11', '14', '17']:
        keys = ["V2Eu", "I2Eu", "kW2Eu", "kvar2Eu", "kVA2Eu",
                "PF2Eu", "V2AngEu", "I2AngEu", "V2THDEu", "I2THDEu", "I2TDDEu"]
    elif line_number in ['3', '6', '9', '12', '15', '18']:
        keys = ["V3Eu", "I3Eu", "kW3Eu", "kvar3Eu", "kVA3Eu",
                "PF3Eu", "V3AngEu", "I3AngEu", "V3THDEu", "I3THDEu", "I3TDDEu"]
    else:
        return None

    for key in keys:
        line_data[key] = real_time_data.get(key, None)

    return {'line_number': line_number, 'line_data': line_data}


@app.route("/api/Scarborough/<line>", methods=["GET"])
def get_single_phase_data(line):
    real_time1 = BFM136_1.RealTimeMeasurement()
    real_time2 = BFM136_2.RealTimeMeasurement()
    real_time3 = BFM136_3.RealTimeMeasurement()
    real_time4 = BFM136_4.RealTimeMeasurement()
    real_time5 = BFM136_5.RealTimeMeasurement()
    real_time6 = BFM136_6.RealTimeMeasurement()
    real_time7 = BFM136_7.RealTimeMeasurement()
    real_time8 = BFM136_8.RealTimeMeasurement()
    real_time9 = BFM136_9.RealTimeMeasurement()
    real_time10 = BFM136_10.RealTimeMeasurement()
    real_time11 = BFM136_11.RealTimeMeasurement()
    real_time12 = BFM136_12.RealTimeMeasurement()
    real_time_data1 = real_time1.DataArray()
    real_time_data2 = real_time2.DataArray()
    real_time_data3 = real_time3.DataArray()
    real_time_data4 = real_time4.DataArray()
    real_time_data5 = real_time5.DataArray()
    real_time_data6 = real_time6.DataArray()
    real_time_data7 = real_time7.DataArray()
    real_time_data8 = real_time8.DataArray()
    real_time_data9 = real_time9.DataArray()
    real_time_data10 = real_time10.DataArray()
    real_time_data11 = real_time11.DataArray()
    real_time_data12 = real_time12.DataArray()

    if line == "1" or line == "2" or line == "3":
        data = get_data_for_line(line, real_time_data1)
    elif line == "4" or line == "5" or line == "6":
        data = get_data_for_line(line, real_time_data2)
    elif line == "7" or line == "8" or line == "9":
        data = get_data_for_line(line, real_time_data3)
    elif line == "10" or line == "11" or line == "12":
        data = get_data_for_line(line, real_time_data4)
    elif line == "13" or line == "14" or line == "15":
        data = get_data_for_line(line, real_time_data5)
    elif line == "16" or line == "17" or line == "18":
        data = get_data_for_line(line, real_time_data6)
# Make it easier
    else:
        return

    if data is not None:
        return jsonify(data)
    else:
        return jsonify({"error": f"Invalid line number {line}."}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
