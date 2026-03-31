import requests
import matplotlib.pyplot as plt

# Phoenix Sky Harbor Airport coordinates
lat, lon = 33.4342, -112.0116

# Fetch weather data (no API key needed)
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
data = requests.get(url).json()

temps = data["hourly"]["temperature_2m"][:24]
times = [t[11:16] for t in data["hourly"]["time"][:24]]  # HH:MM format

# Plot temperature
plt.figure(figsize=(10, 4))
plt.plot(times, temps)
plt.xticks(rotation=45)
plt.title("Phoenix Airport Temperature (Next 24h)")
plt.tight_layout()
plt.savefig("weather.png")
plt.close()

# Funny Arizona logic
max_temp = max(temps)

if max_temp > 45:
    vibe = "🔥 You are inside an oven."
elif max_temp > 40:
    vibe = "☀️ Desert mode activated."
elif max_temp > 35:
    vibe = "😅 Still normal for Arizona."
else:
    vibe = "🙂 Surprisingly survivable."

summary = f"""
🌵 Arizona Heat Reality

🔥 Max temp: {max_temp}°C — {vibe}

"In Arizona, we don’t check the weather.
We check if it's survivable."

Built because Phoenix heat is built different.
"""

# Save text for metrics injection
with open("weather.md", "w") as f:
    f.write(summary)
