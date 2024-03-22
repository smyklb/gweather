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
    url_c = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&APPID=" + api_key
    print(url_c)
    response = requests.get(url).json()
    response_2 = requests.get(url_c).json()

    # current weather
    cw = response_2.get("main").get("temp")
    cw_c = round(cw - 273.15)
    print(cw_c)
    c_list = [cw_c]

    # current weather description
    weather_d = (response.get("list")[2].get("weather")[0].get("description"))
    weather_dc = weather_d.capitalize()

    # current date time as day name
    dt = int(response.get("list")[0].get("dt"))

    date_time = datetime.datetime.fromtimestamp(dt)

    dt_form = (date_time.strftime('%A'))
    dt_3 = dt_form[0:3]

    # current hour
    now = date.now()

    current_time = now.strftime("%H:%M")
    cdtn_list = [dt_form, current_time, weather_dc]

    # get 5 day highs and lows
    def get_daily_low_high_forecast(city_name, api_key):
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city_name,
            "APPID": api_key,
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            dates = []
            min_temps = []
            max_temps = []

            for forecast in data["list"]:
                # Extract date and temperature data
                date = forecast["dt_txt"].split(" ")[0]
                temperature = forecast["main"]["temp"]

                # Check if the date exists in the lists
                if date not in dates:
                    dates.append(date)
                    min_temps.append(temperature)
                    max_temps.append(temperature)
                else:
                    # Update min and max temperature if necessary
                    index = dates.index(date)
                    if temperature < min_temps[index]:
                        min_temps[index] = temperature
                    elif temperature > max_temps[index]:
                        max_temps[index] = temperature

            return dates, min_temps, max_temps
        else:
            print("Error:", response.status_code)
            return None, None, None

    # Replace "adelaide" and "your_api_key" with your desired city and actual API key

    dates, min_temps, max_temps = get_daily_low_high_forecast(city, api_key)
    if dates and min_temps and max_temps:
        print(max_temps, min_temps)

    else:
        print("Failed to fetch forecast data.")

    # day 1 (current day) weather
    day1_min = round(min_temps[0] - 273.15)
    day1_max = round(max_temps[0] - 273.15)

    # day 1 (current day ) icon
    icon = response.get("list")[2].get("weather")[0].get("icon")
    icon_f = icon + "@2x.png"
    day_1 = [dt_3, icon_f, day1_min, day1_max]

    # day 2 name
    dt2 = int(response.get("list")[8].get("dt"))

    date_time2 = datetime.datetime.fromtimestamp(dt2)

    dt_form2 = (date_time.strftime('%A'))
    dt_d2 = dt_form2[0:3]

    # day 2 weather
    day2_min = round(min_temps[1] - 273.15)
    day2_max = round(max_temps[1] - 273.15)

    # day 2 icon
    icon = response.get("list")[10].get("weather")[0].get("icon")
    print(icon)
    icon2_f = icon + "@2x.png"

    day_2 = [dt_d2, icon2_f, day2_min, day2_max]

    return render_template('home.html', current_list=cdtn_list, weather_list=c_list, day_1=day_1, day_2=day_2)


if __name__ == '__main__':
    app.run(debug=True)

    # current weather
    #   temp in f and c, precipitation, humidity, wind speed, date time, description

    # graphs
    #   3 graphs: temp time series, precipitation time series and wind speed
