import json
import re

# Example message payload:
# b'{"pm2.5_cf_1":12.3,"temperature":75.0,"humidity":40.0,"signal":-67}'

def parse_data(json_data: dict) -> dict:
    """
    Extracts key live values from PurpleAir Flex JSON format.
    """
    sensor = json_data.get("sensor", {})
    pm = json_data.get("pm", {})
    stats = json_data.get("stats", {})

    values = {
        "PM1.0": pm.get("pm1.0"),
        "PM2.5": pm.get("pm2.5"),
        "PM10.0": pm.get("pm10.0"),
        "AQI": pm.get("aqi"),
        "Temp (F)": sensor.get("temperature"),
        "Humidity (%)": sensor.get("humidity"),
        "Pressure (hPa)": sensor.get("pressure"),
        "VOC": sensor.get("voc"),
        "Signal RSSI (dBm)": sensor.get("rssi"),
        "Uptime (s)": sensor.get("uptime"),
        "Last Updated": stats.get("last_updated")
    }

    # Remove None values
    return {k: v for k, v in values.items() if v is not None}


def extract_fallback_values(msg: str) -> dict:
    """
    Fallback parser for simple 'key:value' patterns in plain text.
    """
    results = {}
    patterns = {
        "pm2.5_cf_1": r"pm2\.5[_ ]?cf[_ ]?1[:= ](\d+(\.\d+)?)",
        "temperature": r"temperature[:= ](\d+(\.\d+)?)",
        "humidity": r"humidity[:= ](\d+(\.\d+)?)",
        "pressure": r"pressure[:= ](\d+(\.\d+)?)",
        "signal": r"signal[:= ](-?\d+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, msg, re.IGNORECASE)
        if match:
            results[key] = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))

    return results

if __name__ == "__main__":
    sample = '{"pm2.5_cf_1":12.3,"temperature":75.0,"humidity":40.0,"signal":-67}'
    print(parse_data(sample))

    fallback = "pm2.5_cf_1: 14.7 humidity=42 temperature: 73"
    print(parse_data(fallback))