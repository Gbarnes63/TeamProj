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


for key in dummy_data:
  print(key)
  point = (
    Point('Temp')
    .tag("Sensor ID", dummy_data[key]['Sensor'])
    .field('Temp',dummy_data[key]['Temp'])


  )
  client.write(database=database,record = point)




print("Complete. Return to the InfluxDB UI.")
