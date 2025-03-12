# Temperature and Humidity Monitoring with LCD Display

## Overview
This Python script reads temperature and humidity data from a DHT11 sensor and displays the readings on an I2C-connected LCD screen. It is designed for use with a Raspberry Pi and utilizes the `adafruit_dht` and `smbus` libraries for sensor and LCD communication.

## Hardware Requirements
- Raspberry Pi (Rev 2 or later)
- DHT11 Temperature and Humidity Sensor
- I2C-based 16x2 LCD Display (default address `0x3F` or `0x27`)
- Jumper Wires

## Software Requirements
- Python 3
- Required Libraries:
  - `adafruit_dht` for sensor communication
  - `board` for GPIO pin control
  - `smbus` for I2C communication with the LCD
  - `time`, `datetime`, `socket`, and `subprocess` for general utilities

## Setup and Installation
1. **Enable I2C on Raspberry Pi**
   ```bash
   sudo raspi-config
   ```
   Navigate to `Interfacing Options` > `I2C` and enable it.

2. **Install Required Python Libraries**
   ```bash
   pip install adafruit-circuitpython-dht smbus2
   sudo apt-get install libgpiod2
   ```

3. **Connect the Hardware**
   - **DHT11 Sensor:**
     - VCC → 3.3V or 5V
     - Data → GPIO 4 (BCM mode)
     - GND → GND
   - **LCD Display (I2C-based):**
     - VCC → 5V
     - GND → GND
     - SDA → SDA (Pin 3 on Raspberry Pi)
     - SCL → SCL (Pin 5 on Raspberry Pi)

## Code Explanation
### **1. Initialize DHT11 Sensor**
The script defines `DHT_PIN` as `board.D4`, which corresponds to GPIO 4. The `adafruit_dht.DHT11` library handles communication with the sensor.

```python
DHT_PIN = board.D4
dht11 = adafruit_dht.DHT11(DHT_PIN)
```

### **2. LCD Class Implementation**
The `LCD` class provides methods to initialize, send commands, display messages, and clear the LCD screen. It uses the `smbus` library for I2C communication.

```python
lcd = LCD(2, 0x27, True)  # Initialize with Raspberry Pi rev 2, I2C address 0x27, and backlight enabled
```

### **3. Reading Sensor Data**
The function `get_sensor_data()` retrieves temperature and humidity values from the DHT11 sensor with up to 5 retries in case of read failures.

```python
def get_sensor_data():
    retries = 5
    for _ in range(retries):
        try:
            temperature = dht11.temperature
            humidity = dht11.humidity
            if temperature is not None and humidity is not None:
                return temperature, humidity
        except RuntimeError as e:
            print(f"Error reading sensor: {e}")
        time.sleep(1)
    raise RuntimeError("Max retries reached, sensor not returning valid data.")
```

### **4. Display Data on LCD**
Inside the `while True` loop, the script continuously reads sensor data and displays the values on the LCD.

```python
while True:
    temperature, humidity = get_sensor_data()
    lcd.message(f"Temp: {temperature:.1f}°C", 1)
    lcd.message(f"Humidity: {humidity:.1f}%", 2)
    time.sleep(0.5)
```

### **5. Graceful Exit**
If the user interrupts the program (`CTRL+C`), the sensor and LCD are cleaned up before exiting.

```python
except KeyboardInterrupt:
    print("Stopping program...")
finally:
    dht11.exit()
    lcd.clear()
```

## Running the Script
To run the script, execute:
```bash
python3 script_name.py
```
Replace `script_name.py` with the actual filename.

## Troubleshooting
- Ensure the I2C address of the LCD is correct (`0x27` or `0x3F`). Check with:
  ```bash
  i2cdetect -y 1
  ```
- If the DHT11 sensor fails frequently, try reducing read frequency (increase `time.sleep`).
- Ensure proper wiring connections.

## License
This project is open-source and free to use and modify.
