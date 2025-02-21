import os, time






import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = 'T00lUif3KjaNgQOOVpOpIi8d2vIZupRNbDlPh-IlymKNbr9fQQ0hRw3bcDacACQxKlV1WaY2pVcOUg5KS4LMFA=='

url = "http://localhost:8086"

org = "teampi"








dummy_data = {}

dummy_data['datapoint 4'] = {
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
        
    print('Dictionary parsed to  point successfuly')
    return point

def write_to_db(reading,point,parsed_data):

    point = parse_to_point(reading,parsed_data)
    write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    
    write_api = write_client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket='Temp/humidity', org="UoD", record=point)


    print("Success")



