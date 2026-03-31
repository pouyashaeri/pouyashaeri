import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Phoenix Airport coords
lat, lon = 33.4342, -112.0116

url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"

data = requests.get(url).json()

temps = data["hourly"]["temperature_2m"][:24]
times = data["hourly"]["time"][:24]

# Plot
plt.figure(figsize=(10,4))
plt.plot(times, temps)
plt.xticks(rotation=45)
plt.title("Phoenix Airport Temperature (Next 24h)")
plt.tight_layout()
plt.savefig("weather.png")
plt.close()

# Funny summary
max_temp = max(temps)

summary = f"""
## 🌵 Arizona Heat Check

Today’s max temp: **{max_temp}°C**

> In Arizona, we don’t check the weather.
> We check if it’s *survivable*.

Yes, I built this because Phoenix heat is built different.
"""

with open("weather.md", "w") as f:
    f.write(summary)
