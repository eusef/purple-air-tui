import json
import re
# Example message payload:
# b'{"pm2.5_cf_1":12.3,"temperature":75.0,"humidity":40.0,"signal":-67}'

def parse_data(json_data: dict) -> dict:
    """
    Extracts ALL available values from PurpleAir Flex JSON format.
    """

    values = {
        # Basic sensor information
        "SensorId": json_data.get("SensorId"),
        "DateTime": json_data.get("DateTime"),
        "Geo": json_data.get("Geo"),
        "Id": json_data.get("Id"),
        "place": json_data.get("place"),
        "version": json_data.get("version"),
        "hardwareversion": json_data.get("hardwareversion"),
        "hardwarediscovered": json_data.get("hardwarediscovered"),
        
        # Location data
        "lat": json_data.get("lat"),
        "lon": json_data.get("lon"),
        
        # System information
        "Mem": json_data.get("Mem"),
        "memfrag": json_data.get("memfrag"),
        "memfb": json_data.get("memfb"),
        "memcs": json_data.get("memcs"),
        "uptime": json_data.get("uptime"),
        "loggingrate": json_data.get("loggingrate"),
        "period": json_data.get("period"),
        
        # Network and connectivity
        "rssi": json_data.get("rssi"),
        "httpsuccess": json_data.get("httpsuccess"),
        "httpsends": json_data.get("httpsends"),
        "wlstate": json_data.get("wlstate"),
        "ssid": json_data.get("ssid"),
        "pa_latency": json_data.get("pa_latency"),
        "response": json_data.get("response"),
        "response_date": json_data.get("response_date"),
        "latency": json_data.get("latency"),
        
        # Analog and sensor readings
        "Adc": json_data.get("Adc"),
        
        # Environmental data - Primary sensor
        "current_temp_f": json_data.get("current_temp_f"),
        "current_humidity": json_data.get("current_humidity"),
        "current_dewpoint_f": json_data.get("current_dewpoint_f"),
        "pressure": json_data.get("pressure"),
        
        # Environmental data - BME680 sensor
        "current_temp_f_680": json_data.get("current_temp_f_680"),
        "current_humidity_680": json_data.get("current_humidity_680"),
        "current_dewpoint_f_680": json_data.get("current_dewpoint_f_680"),
        "pressure_680": json_data.get("pressure_680"),
        "gas_680": json_data.get("gas_680"),
        
        # PM2.5 AQI and color codes - Channel A
        "p25aqic": json_data.get("p25aqic"),
        "pm2.5_aqi": json_data.get("pm2.5_aqi"),
        
        # PM2.5 AQI and color codes - Channel B
        "p25aqic_b": json_data.get("p25aqic_b"),
        "pm2.5_aqi_b": json_data.get("pm2.5_aqi_b"),
        
        # PM measurements - Channel A (CF=1)
        "pm1_0_cf_1": json_data.get("pm1_0_cf_1"),
        "pm2_5_cf_1": json_data.get("pm2_5_cf_1"),
        "pm10_0_cf_1": json_data.get("pm10_0_cf_1"),
        
        # PM measurements - Channel A (ATM)
        "pm1_0_atm": json_data.get("pm1_0_atm"),
        "pm2_5_atm": json_data.get("pm2_5_atm"),
        "pm10_0_atm": json_data.get("pm10_0_atm"),
        
        # PM measurements - Channel B (CF=1)
        "pm1_0_cf_1_b": json_data.get("pm1_0_cf_1_b"),
        "pm2_5_cf_1_b": json_data.get("pm2_5_cf_1_b"),
        "pm10_0_cf_1_b": json_data.get("pm10_0_cf_1_b"),
        
        # PM measurements - Channel B (ATM)
        "pm1_0_atm_b": json_data.get("pm1_0_atm_b"),
        "pm2_5_atm_b": json_data.get("pm2_5_atm_b"),
        "pm10_0_atm_b": json_data.get("pm10_0_atm_b"),
        
        # Particle counts - Channel A
        "p_0_3_um": json_data.get("p_0_3_um"),
        "p_0_5_um": json_data.get("p_0_5_um"),
        "p_1_0_um": json_data.get("p_1_0_um"),
        "p_2_5_um": json_data.get("p_2_5_um"),
        "p_5_0_um": json_data.get("p_5_0_um"),
        "p_10_0_um": json_data.get("p_10_0_um"),
        
        # Particle counts - Channel B
        "p_0_3_um_b": json_data.get("p_0_3_um_b"),
        "p_0_5_um_b": json_data.get("p_0_5_um_b"),
        "p_1_0_um_b": json_data.get("p_1_0_um_b"),
        "p_2_5_um_b": json_data.get("p_2_5_um_b"),
        "p_5_0_um_b": json_data.get("p_5_0_um_b"),
        "p_10_0_um_b": json_data.get("p_10_0_um_b"),
        
        # Status indicators
        "status_0": json_data.get("status_0"),
        "status_1": json_data.get("status_1"),
        "status_2": json_data.get("status_2"),
        "status_3": json_data.get("status_3"),
        "status_4": json_data.get("status_4"),
        "status_6": json_data.get("status_6")
    }

    # Remove None values
    return {k: v for k, v in values.items() if v is not None}

if __name__ == "__main__":
    # Example PurpleAir Flex JSON format expected by parse_data
    sample_json = {
        "SensorId": "f0:24:f9:c3:1a:9c",
        "DateTime": "2025/07/26T15:26:44z",
        "Geo": "PurpleAir-1a9c",
        "Mem": 7096,
        "memfrag": 47,
        "memfb": 3424,
        "memcs": 352,
        "Id": 7468,
        "lat": 45.412498,
        "lon": -122.757500,
        "Adc": 4.93,
        "loggingrate": 15,
        "place": "outside",
        "version": "7.04",
        "uptime": 389380,
        "rssi": -60,
        "period": 120,
        "httpsuccess": 4685,
        "httpsends": 6597,
        "hardwareversion": "3.0",
        "hardwarediscovered": "3.0+OPENLOG+NO-DISK+RV3028+BME68X+PMSX003-A+PMSX003-B",
        "current_temp_f": 63,
        "current_humidity": 64,
        "current_dewpoint_f": 50,
        "pressure": 1010.52,
        "current_temp_f_680": 63,
        "current_humidity_680": 64,
        "current_dewpoint_f_680": 50,
        "pressure_680": 1010.52,
        "gas_680": 82.94,
        "p25aqic_b": "rgb(7,229,0)",
        "pm2.5_aqi_b": 15,
        "pm1_0_cf_1_b": 2.90,
        "p_0_3_um_b": 568.47,
        "pm2_5_cf_1_b": 3.68,
        "p_0_5_um_b": 168.63,
        "pm10_0_cf_1_b": 3.92,
        "p_1_0_um_b": 24.66,
        "pm1_0_atm_b": 2.90,
        "p_2_5_um_b": 1.00,
        "pm2_5_atm_b": 3.68,
        "p_5_0_um_b": 0.17,
        "pm10_0_atm_b": 3.92,
        "p_10_0_um_b": 0.17,
        "p25aqic": "rgb(7,229,0)",
        "pm2.5_aqi": 15,
        "pm1_0_cf_1": 2.60,
        "p_0_3_um": 578.17,
        "pm2_5_cf_1": 3.64,
        "p_0_5_um": 164.88,
        "pm10_0_cf_1": 3.97,
        "p_1_0_um": 26.47,
        "pm1_0_atm": 2.60,
        "p_2_5_um": 1.64,
        "pm2_5_atm": 3.64,
        "p_5_0_um": 0.33,
        "pm10_0_atm": 3.97,
        "p_10_0_um": 0.33,
        "pa_latency": 227,
        "response": -11,
        "response_date": 1753543593,
        "latency": 207,
        "wlstate": "Connected",
        "status_0": 2,
        "status_1": 0,
        "status_2": 2,
        "status_3": 2,
        "status_4": 2,
        "status_6": 3,
        "ssid": "MONKEY-Domain"
    }

    print(parse_data(sample_json))