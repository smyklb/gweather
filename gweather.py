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
    cdtn_list = [dt_form2, time_now, weather_dc]

    # get 5 day highs and lows
    def get_daily_low_high_forecast(api_key, city_name):
        # Make the API request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            dates = []
            min_temps = []
            max_temps = []

            # Initialize a dictionary to store temperatures for each date
            temp_dict = {}

            for forecast in data["list"]:
                # Extract date and temperature data
                date = forecast["dt_txt"].split(" ")[0]
                temperature = forecast["main"]["temp"]

                # Add temperature to temp_dict for the corresponding date
                if date not in temp_dict:
                    temp_dict[date] = [temperature]
                else:
                    temp_dict[date].append(temperature)

            # Calculate min and max temperatures for each date
            for date, temps in temp_dict.items():
                dates.append(date)
                min_temps.append(min(temps))
                max_temps.append(max(temps))

            return dates, min_temps, max_temps
        else:
            print("Error:", response.status_code)
            return None, None, None

    # Example usage
    api_key = 'YOUR_API_KEY'
    city = 'YOUR_CITY_NAME'

    dates, min_temps, max_temps = get_daily_low_high_forecast(api_key, city)
    if dates and min_temps and max_temps:
        for date, min_temp, max_temp in zip(dates, min_temps, max_temps):
            print(f"Date: {date}, Min Temp: {min_temp}, Max Temp: {max_temp}")
    else:
        print("Failed to fetch forecast data.")

    # get the icons for each day
    icons = []  # List to store the icon URLs
    previous_date = None  # Variable to store the previous date

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

    # day 2 weather
    day2_min = round(min_temps[1] - 273.15)
    day2_max = round(max_temps[1] - 273.15)

    # day 2 icon
    icon2 = icons[1]
    icon_2 = icon2 + "@2x.png"

    day_2 = [dt_d2, icon_2, day2_min, day2_max]

    # day 3 name
    date_time3 = (dates[2])
    dt_form3 = datetime.strptime(date_time3, '%Y-%m-%d')
    dt_3 = dt_form3.strftime('%A')
    dt_d3 = dt_3[0:3]

    # day 3 weather
    day3_min = round(min_temps[2] - 273.15)
    day3_max = round(max_temps[2] - 273.15)

    # day 3 icon
    icon3 = icons[2]
    icon_3 = icon3 + "@2x.png"

    day_3 = [dt_d3, icon_3, day3_min, day3_max]

    # day 4 name
    date_time4 = (dates[3])
    dt_form4 = datetime.strptime(date_time4, '%Y-%m-%d')
    dt_4 = dt_form4.strftime('%A')
    dt_d4 = dt_4[0:3]

    # day 4 weather
    day4_min = round(min_temps[3] - 273.15)
    day4_max = round(max_temps[3] - 273.15)

    # day 4 icon
    icon4 = icons[3]
    icon_4 = icon4 + "@2x.png"

    day_4 = [dt_d4, icon_4, day4_min, day4_max]

    # day 5 name
    date_time5 = (dates[4])
    dt_form5 = datetime.strptime(date_time5, '%Y-%m-%d')
    dt_5 = dt_form5.strftime('%A')
    dt_d5 = dt_5[0:3]

    # day 5 weather
    day5_min = round(min_temps[4] - 273.15)
    day5_max = round(max_temps[4] - 273.15)

    # day 5 icon
    icon5 = icons[4]
    icon_5 = icon5 + "@2x.png"

    day_5 = [dt_d5, icon_5, day5_min, day5_max]

    # day 6 name
    print(dates)
    date_time6 = dates[4]
    dt_form6 = datetime.strptime(date_time6, '%Y-%m-%d')
    dt_6 = dt_form6.strftime('%A')
    dt_d6 = dt_6[0:3]

    # day 6 weather
    day6_min = round(min_temps[4] - 273.15)
    day6_max = round(max_temps[4] - 273.15)

    # day 6 icon
    icon6 = icons[4]
    icon_6 = icon6 + "@2x.png"

    day_6 = [dt_d6, icon_6, day6_min, day6_max]
    return render_template('home.html', current_list=cdtn_list, weather_list=c_list, day_1=day_1, day_2=day_2, day_3=day_3, day_4=day_4, day_5=day_5, day_6=day_6)


if __name__ == '__main__':
    app.run(debug=True)

    # current weather
    #   temp in f and c, precipitation, humidity, wind speed, date time, description

    # graphs
    #   3 graphs: temp time series, precipitation time series and wind speed
