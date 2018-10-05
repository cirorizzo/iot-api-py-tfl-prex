
import urllib2
import json

from flask import Flask, url_for
app = Flask(__name__)

@app.route("/")
def first_function():
    return "<html><body><h1 style='color:red'>I am hosted on Raspberry Pi !!!</h1></body></html>"

@app.route('/tfl')
def tflprex():
    return "<html><body><h1 style='color:red'>" + 'TfL API IoT ' + url_for('tflprex') + "</h1></body></html>"

@app.route('/tfl/busprex')
def tflbusprex():
    return "<html><body><h1 style='color:red'>" + 'Bus Predictions ' + url_for('tflbusprex') + "</h1></body></html>"

@app.route('/tfl/busprex/stop/<stopid>')
def tflbusstopprex(stopid):
    return gimmeinfo(stopid)

@app.route('/tfl/busprex/stopx')
def busprexparam():
   if 'ixd' in request.args:
       return gimmeinfo(request.args['ixd'])
   else:
       return "<html><body><h1 style='color:red'>" + 'Direct StopId no Param ' + request.args['ixd'] + "</h1></body></html>"


def gimmeinfo(bus_stop_id):
    try:
        tfl_url_stub = "https://api.tfl.gov.uk/StopPoint/%s/Arrivals" % bus_stop_id
        response = urllib2.urlopen(tfl_url_stub)

        jstring = response.read()
    except ValueError:
        error_result = "TfL API Error %s", ValueError
        print error_result
        return error_result


    try:
        parsed_json = json.loads(jstring)
        bus_list = list()

        for item in parsed_json:
            time_minute = "%s\'%s\"" % ((item['timeToStation'] / 60), (item['timeToStation'] % 60));
            bus_list.append((item['lineName'], item['timeToStation'], time_minute))

        def custom_sort(t):
            return t[1]

        bus_list.sort(key=custom_sort)

        result_list = list()
        for item_line in bus_list:
            x, y, z = item_line
            line = "Bus %s in %s" % (x, z)
            result_list.append(line)

        result_tfl = '\n'.join(result_list)
        return result_tfl

    except ValueError:
        error_result = "Error loading JSON"
        print error_result
        return error_result

if __name__ == '__main__':
    app.run(host='0.0.0.0')
