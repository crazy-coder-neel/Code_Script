import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from staticmap import StaticMap, CircleMarker

def get_weather() -> None:
    """
    Fetch weather data for the specified city and update the UI with weather info and map.
    Arguments:
        None
    Returns:
        None
    """
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    api_key = "OPENWEATHER_API_KEY" # Replace with your OpenWeatherMap API key
    weather_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(weather_url, params=params) # Fetch weather data
        data = response.json()
        if data["cod"] != 200:
            messagebox.showerror("Error", f"City not found: {city}")
            return

        city_name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        weather_info = (
            f"City: {city_name}, {country}\n"
            f"Temperature: {temp}°C\n"
            f"Weather: {weather_desc.title()}\n"
            f"Humidity: {humidity}%"
        )
        weather_label.config(text=weather_info)

        # Generate static map locally using OSM tiles
        m = StaticMap(450, 300, url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png')
        marker = CircleMarker((lon, lat), 'red', 12)
        m.add_marker(marker)
        image = m.render(zoom=10)

        # Convert to Tkinter image
        img_bytes = BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        map_photo = ImageTk.PhotoImage(Image.open(img_bytes))

        map_label.config(image=map_photo)
        map_label.image = map_photo

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# Tkinter UI setup
root = tk.Tk()
root.title("Weather App with Local Map")
root.geometry("500x600")
root.resizable(False, False)

# UI Components
tk.Label(root, text="Enter City Name:", font=("Arial", 14)).pack(pady=10)
city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=5)

tk.Button(root, text="Get Weather", font=("Arial", 14), command=get_weather).pack(pady=10)
weather_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
weather_label.pack(pady=10)
map_label = tk.Label(root)
map_label.pack(pady=10)

root.mainloop()
