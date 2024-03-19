import requests
from flask import Flask, render_template, request
from datetime import datetime as date
import datetime as datetime
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
    c_list = [temp_c]

    # weather description
    weather_d = (response.get("list")[2].get("weather")[0].get("description"))
    weather_dc = weather_d.capitalize()
    print(weather_dc)

    # date time as day name
    dt = int(response.get("list")[0].get("dt"))

    date_time = datetime.datetime.fromtimestamp(dt)

    dt_form = (date_time.strftime('%A'))
    print(dt_form)

    # current hour
    now = date.now()

    current_time = now.strftime("%H:%M")
    dtn_list = [dt_form, current_time, weather_dc]

    return render_template('home.html', current_list=dtn_list, weather_list=c_list)


if __name__ == '__main__':
    app.run(debug=True)

    # current weather
    #   temp in f and c, precipitation, humidity, wind speed, date time, description

    # graphs
    #   3 graphs: temp time series, precipitation time series and wind speed
