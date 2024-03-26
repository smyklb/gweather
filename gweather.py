import datetime
from datetime import datetime

import requests
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    api_key = "03813016975d1bf4e5573449445caef7"
    city = "adelaide"
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

    date_time = datetime.fromtimestamp(dt)

    dt_form2 = (date_time.strftime('%A'))
    dt_3 = dt_form2[0:3]

    # current time
    time_now1 = datetime.now().hour, datetime.now().minute
    time_now = (str(datetime.now().hour) + ":" + str(datetime.now().minute))
    print(time_now)
    cdtn_list = [dt_form2, time_now, weather_dc]

    # get 5 day highs and lows
    def get_daily_low_high_forecast(api_key, city_name):
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city_name,
            "APPID": api_key,
        }

        # Make the API request
        response = requests.get(url, params=params)

        # Check if the request was successful (status code 200)
        if response.ok:
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

    dates, min_temps, max_temps = get_daily_low_high_forecast(api_key, city)
    if dates and min_temps and max_temps:
        print(max_temps, min_temps)
    else:
        print("Failed to fetch forecast data.")

    # get the icons for each day
    icons = []  # List to store the icon URLs
    previous_date = None  # Variable to store the previous date

    # Check if the 'list' key exists in the response data
    if 'list' in response:
        # Parse JSON response
        data = response

        # Extract daily forecasts
        for forecast in data['list']:
            # Get the date for the forecast
            date = forecast['dt_txt'].split()[0]  # Extracting date from dt_txt field

            # Check if it's a new day
            if date != previous_date:
                # Get the icon code for the forecast
                icon_code = forecast['weather'][0]['icon']

                # Construct the URL for the weather icon
                icon_url = f'{icon_code}'

                # Append the icon URL to the list
                icons.append(icon_url)

                # Update previous date
                previous_date = date

    else:
        print("Error fetching data. Response:", response)

    # day 1 (current day) weather
    day1_min = round(min_temps[0] - 273.15)
    day1_max = round(max_temps[0] - 273.15)

    # day 1 (current day ) icon
    icon1 = icons[0]
    icon_1 = icon1 + "@2x.png"
    day_1 = [dt_3, icon_1, day1_min, day1_max]

    # day 2 name DONT FORGET HOW TO DO THIS YOU IDIOT!!!
    date_time2 = (dates[1])
    dt_form2 = datetime.strptime(date_time2, '%Y-%m-%d')
    dt_2 = dt_form2.strftime('%A')
    dt_d2 = dt_2[0:3]
    print(dt_d2)

    # day 2 weather
    day2_min = round(min_temps[1] - 273.15)
    day2_max = round(max_temps[1] - 273.15)

    # day 2 icon
    icon2 = icons[0]
    icon_2 = icon1 + "@2x.png"

    day_2 = [dt_d2, icon_2, day2_min, day2_max]

    return render_template('home.html', current_list=cdtn_list, weather_list=c_list, day_1=day_1, day_2=day_2)


if __name__ == '__main__':
    app.run(debug=True)

    # current weather
    #   temp in f and c, precipitation, humidity, wind speed, date time, description

    # graphs
    #   3 graphs: temp time series, precipitation time series and wind speed
