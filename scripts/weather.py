import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Phoenix Sky Harbor Airport coordinates
lat, lon = 33.4342, -112.0116

# Fetch BOTH current conditions AND the past 6 hours of actual data
url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={lat}&longitude={lon}"
    f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
    f"precipitation,weathercode,windspeed_10m,winddirection_10m,uv_index"
    f"&hourly=temperature_2m"
    f"&past_hours=6"       # last 6 hours of real recorded data
    f"&forecast_hours=18"  # next 18 hours of forecast
    f"&timezone=America%2FPhoenix"
)

data = requests.get(url).json()

# ── Current conditions ──────────────────────────────────────────────────────
current    = data["current"]
now_temp   = current["temperature_2m"]
feels_like = current["apparent_temperature"]
humidity   = current["relative_humidity_2m"]
wind_speed = current["windspeed_10m"]
wind_dir   = current["winddirection_10m"]
uv_index   = current["uv_index"]
precip     = current["precipitation"]
updated_at = current["time"]  # local Phoenix time string e.g. "2025-07-01T14:00"

# ── Hourly series (past 6h + next 18h = 24 points) ─────────────────────────
raw_times     = data["hourly"]["time"]
temps         = data["hourly"]["temperature_2m"]
parsed_times  = [datetime.strptime(t, "%Y-%m-%dT%H:%M") for t in raw_times]

# Split into actual (past) vs forecast (future)
now_str      = updated_at[:13]  # "YYYY-MM-DDTHH"
past_mask    = [t[:13] <= now_str for t in raw_times]
past_times   = [t for t, p in zip(parsed_times, past_mask) if p]
past_temps   = [v for v, p in zip(temps, past_mask) if p]
future_times = [t for t, p in zip(parsed_times, past_mask) if not p]
future_temps = [v for v, p in zip(temps, past_mask) if not p]

# ── Plot ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 4))

ax.plot(past_times, past_temps, color="#FF6B35", linewidth=2.5, label="Actual")
ax.fill_between(past_times, past_temps, alpha=0.18, color="#FF6B35")
ax.plot(future_times, future_temps, color="#FF6B35", linewidth=2.0,
        linestyle="--", alpha=0.7, label="Forecast")
ax.axvline(x=past_times[-1], color="gray", linestyle=":", linewidth=1.2, label="Now")

ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
plt.xticks(rotation=45)
ax.set_title("🌵 Phoenix Airport — Past 6h Actual + 18h Forecast", fontsize=13, pad=10)
ax.set_ylabel("Temperature (°C)")
ax.legend(loc="upper right", fontsize=9)
ax.grid(axis="y", linestyle="--", alpha=0.35)
plt.tight_layout()
plt.savefig("weather.png", dpi=150)
plt.close()

# ── Vibe logic ───────────────────────────────────────────────────────────────
max_temp = max(t for t in temps if t is not None)
min_temp = min(t for t in temps if t is not None)

def wind_direction_label(deg):
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return dirs[round(deg / 45) % 8]

if now_temp > 45:
    vibe = "🔥 You are inside an oven."
elif now_temp > 40:
    vibe = "☀️ Desert mode activated."
elif now_temp > 35:
    vibe = "😅 Still normal for Arizona."
elif now_temp > 25:
    vibe = "🙂 Surprisingly survivable."
else:
    vibe = "🧊 Wait, is this still Phoenix?"

updated_fmt = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M").strftime("%b %d, %Y at %H:%M")

summary = f"""🌵 Arizona Heat Reality — Updated {updated_fmt} (Phoenix time)

| Condition        | Value                                    |
|------------------|------------------------------------------|
| 🌡️ Temperature   | {now_temp}°C (feels like {feels_like}°C) |
| 💧 Humidity      | {humidity}%                              |
| 💨 Wind          | {wind_speed} km/h {wind_direction_label(wind_dir)} |
| ☀️ UV Index      | {uv_index}                               |
| 🌧️ Precipitation | {precip} mm                              |
| 📈 24h Range     | {min_temp}°C – {max_temp}°C              |

{vibe}

> "In Arizona, we don't check the weather.
> We check if it's survivable."

_Auto-updated every 2 hours via GitHub Actions._
"""

with open("weather.md", "w") as f:
    f.write(summary)

print(summary)
