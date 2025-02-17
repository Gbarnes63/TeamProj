import os, time
from influxdb_client_3 import InfluxDBClient3, Point

token = os.environ.get("INFLUXDB_TOKEN")
token = "lN30ygiY4Q7XAXnUnDxhoVACxUyRuFfGCgAmYtM6PJe2bhI9I09eqKco1977dLqh-UhBKc8N0FaNhmmozs33xg=="
org = "Uod"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"

client = InfluxDBClient3(host=host, token=token, org=org)


database="Temp"



dummy_data = {}
dummy_data['point 1'] = {
    "Sensor": "1",
    "Unit": "C",
    "Temp": 40,
  }

dummy_data['point 2'] = {
    "Sensor": "1",
    "Unit": "C",
    "Temp": 41,
  }


dummy_data['point 3'] = {
    "Sensor": "1",
    "Unit": "C",
    "Temp": 50,
  }
print(dummy_data)


def parse_to_point(reading, reading_dict):
    """
    Parses sensor temperateure/humidity readings and writes them to InfluxDB.

    Args:
        reading (str): The key for the reading to be written to InfluxDB. String can only be 'Temp' or 'Humidity'
        reading_dict (dict): A dictionary containing sensor data. Must be in the format below in dummy_data.

        dummy_data['point 3'] = {
                                    "Sensor": "1",
                                    "Unit": "C",
                                    "Temp": 50,
                                }

    Returns:
        Point: Returns record as point
    """
    for key in reading_dict:
        print(key)
        point = (
            Point(reading)
            .tag("Sensor ID", reading_dict[key]['Sensor'])
            .field(reading, reading_dict[key][reading])
        )
        

    return point

point = parse_to_point('Temp',dummy_data)
client.write(database=database, record=point)


print("Complete. Return to the InfluxDB UI.")
