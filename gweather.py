import datetime
import requests
from flask import Flask, render_template, request
from datetime import datetime
from datetime import datetime as date
from matplotlib import pyplot as plt

app = Flask(__name__)


@app.route('/')
def index():
    api_key = "03813016975d1bf4e5573449445caef7"
    city = "adelaide"
    # print(request.form)
    url = "https://api.openweathermap.org/data/2.5/forecast?q=" + city + "&APPID=" + api_key
    # print(url)
    response = requests.get(url).json()

    # current weather
    cw = response.get("list")[1].get("main")
    main_w = cw.get("temp")
    temp_c = round(main_w - 273.15)
    print(temp_c)

    # date time as name
    dt = response.get("list")[0]

    g_list = [temp_c]
    return render_template('home.html', weather_list=g_list)


@app.route('/results', methods=("GET", "POST"))
def results():
    api_key = "03813016975d1bf4e5573449445caef7"
    city = request.form.get('city')
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&APPID=" + api_key
    print(url)
    response = requests.get(url).json()
    print(response)
    location = response.get("name")
    timezone = response.get("timezone")
    timestamp = response.get("dt")
    dt = datetime.fromtimestamp(timestamp)
    print(dt)
    timestamp_local = ""
    description = response.get("weather[0].description")
    temp_k = response.get("main").get("temp")
    temp_c = temp_k - 273.15
    wind_speed = response.get("wind").get("speed")
    icon = response.get("weather")[0].get("icon")
    my_list = [location, timezone, timestamp, timestamp_local, description, temp_k, temp_c, wind_speed, icon]
    my_dict = {
        "location": {"lat": 0, "long": 0},
        "timestamp": timestamp,
        "timezone": timezone,
        "dt": dt,
        "description": description,
        "temp_c": temp_c,
        "wind_speed": wind_speed,
        "icon": icon
    }
    print(my_dict)
    print(my_dict["timestamp"])
    print(my_dict["location"]["lat"])

    return render_template('results.html', weather_list=my_list, weather_dict=my_dict)


if __name__ == '__main__':
    app.run(debug=True)

# current weather
#   temp in f and c, precipitation, humidity, wind speed, date time, description

# graphs
#   3 graphs: temp time series, precipitation time series and wind speed
