import requests
import datetime as dt

#Create an openweather account, store the api key in a document and add it in the same directory as the main program and add the path to the "API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = open("Enter the path to your api key", "r").read().strip()  
city = input("enter city name:").strip()


url = f"{BASE_URL}appid={API_KEY}&q={city}"


response = requests.get(url)
if response.status_code == 200:
    response = response.json() 
    def conversion(kelvin):
        celsius = kelvin - 273.15
        fahreneit = celsius *9/5 +32
        return celsius,fahreneit
    
    def activity_recommendation(temp_celsius, wind_speed, humidity, description):
        if description in ["rain", "thunderstorm", "snow","fog","haze"]:
            return "❌ It's not a good day for outdoor activities due to bad weather/low visibility."
        elif wind_speed > 15:
            return "❌ High winds! It might not be safe for outdoor activities."
        elif temp_celsius < 10:
            return "❌ It's too cold for most outdoor activities."
        elif temp_celsius > 30:
            return "❌ It's too hot for outdoor activities. Stay hydrated!"
        elif humidity > 80:
            return "❌ High humidity might make outdoor activities uncomfortable."
        else:
            return "✅ It's a good day for outdoor activities!"
        
    kelvin = response['main']['temp']
    temp_celsius,temp_fahrenheit = conversion(kelvin)

    feels_like=response['main']['feels_like']
    temp_celsius_feel,temp_fahrenheit_feel = conversion(feels_like)

    humidity = response['main']['humidity']
    wind_speed = response['wind']['speed']
    description = response['weather'][0]['description']
    sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

else:
    print(f"Error {response.status_code}: {response.json().get('message', 'Unknown error')}")


html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .container {{
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            width: 300px;
            text-align: center;
        }}
        h1 {{
            font-size: 24px;
            color: #333;
        }}
        #weather-info {{
            margin-top: 20px;
            font-size: 16px;
            color: #555;
        }}
        strong {{
            color: #333;
        }}
        p {{
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Weather Report</h1>
        <div id="weather-info">
            <p><strong>City:</strong> {city}</p>
            <p><strong>Temperature:</strong> {temp_celsius:.2f} °C or {temp_fahrenheit:.2f} °F</p>
            <p><strong>Feels Like:</strong> {temp_celsius_feel:.2f} °C or {temp_fahrenheit_feel:.2f} °F</p>
            <p><strong>Humidity:</strong> {humidity}%</p>
            <p><strong>Wind Speed:</strong> {wind_speed} m/s</p>
            <p><strong>Description:</strong> {description.capitalize()}</p>
            <p><strong>Sunrise:</strong> {sunrise_time}</p>
            <p><strong>Sunset:</strong> {sunset_time}</p>
            <p><strong>Activity Recommendation:</strong>{activity_recommendation(temp_celsius, wind_speed, humidity, description)}</p>
        </div>
    </div>
</body>
</html>
"""

# Write the HTML content to a file
with open(f"weather_report_{city}.html", "w",encoding="utf-8") as file:
    file.write(html_content)

print(" Weather report generated! Open 'weather_report.html' to view it.")
