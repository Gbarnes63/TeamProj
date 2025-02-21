import time
import board
import adafruit_dht
import socket
import subprocess
from datetime import datetime
from datetime import date
import smbus
import manageDB

DHT_PIN = board.D4  # Use the board pin name
dht11 = adafruit_dht.DHT11(DHT_PIN)

class LCD:
    def __init__(self, pi_rev = 2, i2c_addr = 0x3F, backlight = True):

        # device constants
        self.I2C_ADDR  = i2c_addr
        self.LCD_WIDTH = 16   # Max. characters per line

        self.LCD_CHR = 1 # Mode - Sending data
        self.LCD_CMD = 0 # Mode - Sending command

        self.LCD_LINE_1 = 0x80 # LCD RAM addr for line one
        self.LCD_LINE_2 = 0xC0 # LCD RAM addr for line two

        if backlight:
            # on
            self.LCD_BACKLIGHT  = 0x08
        else:
            # off
            self.LCD_BACKLIGHT = 0x00

        self.ENABLE = 0b00000100 # Enable bit

        # Timing constants
        self.E_PULSE = 0.0005
        self.E_DELAY = 0.0005

        # Open I2C interface
        if pi_rev == 2:
            # Rev 2 Pi uses 1
            self.bus = smbus.SMBus(1)
        elif pi_rev == 1:
            # Rev 1 Pi uses 0
            self.bus = smbus.SMBus(0)
        else:
            raise ValueError('pi_rev param must be 1 or 2')

        # Initialise display
        self.lcd_byte(0x33, self.LCD_CMD) # 110011 Initialise
        self.lcd_byte(0x32, self.LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06, self.LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C, self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, self.LCD_CMD) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, self.LCD_CMD) # 000001 Clear display

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = data
        # mode = 1 for data, 0 for command

        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits<<4) & 0xF0) | self.LCD_BACKLIGHT

        # High bits
        self.bus.write_byte(self.I2C_ADDR, bits_high)
        self.toggle_enable(bits_high)

        # Low bits
        self.bus.write_byte(self.I2C_ADDR, bits_low)
        self.toggle_enable(bits_low)

    def toggle_enable(self, bits):
        time.sleep(self.E_DELAY)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        time.sleep(self.E_PULSE)
        self.bus.write_byte(self.I2C_ADDR,(bits & ~self.ENABLE))
        time.sleep(self.E_DELAY)

    def message(self, string, line = 1):
        # display message string on LCD line 1 or 2
        if line == 1:
            lcd_line = self.LCD_LINE_1
        elif line == 2:
            lcd_line = self.LCD_LINE_2
        else:
            raise ValueError('line number must be 1 or 2')

        string = string.ljust(self.LCD_WIDTH," ")

        self.lcd_byte(lcd_line, self.LCD_CMD)

        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(string[i]), self.LCD_CHR)

    def clear(self):
        # clear LCD display
        self.lcd_byte(0x01, self.LCD_CMD)

# Initialize the LCD with specific parameters: Raspberry Pi revision, I2C address, and backlight status
lcd = LCD(2, 0x27, True)  # Using Raspberry Pi revision 2 and above, I2C address 0x3f, backlight enabled

def get_sensor_data():
    retries = 5  # Retry limit
    for _ in range(retries):
        try:
            temperature = dht11.temperature
            humidity = dht11.humidity
            if temperature is not None and humidity is not None:
                return temperature, humidity
            else:
                print("Failed to retrieve data from sensor")
        except RuntimeError as e:
            print(f"Error reading sensor: {e}")
        time.sleep(1)  # Wait between retries
    raise RuntimeError("Max retries reached, sensor not returning valid data.")

def parse_sensor_data(datapoint_counter,temp,sensor,unit):
    parsed_dict = {}

    parsed_dict[f'datapoint {datapoint_counter}'] = {
    "Sensor": sensor,
    "Unit": unit,
    "Temp": temp,
  }
    return parsed_dict
    


try:
    counter = 0
    while True:
        temperature, humidity = get_sensor_data()
        parsed_sensor_data = parse_sensor_data(counter,temperature,"DHT11","C")

        data_point = manageDB.parse_to_point("Temp",parsed_sensor_data)
        manageDB.write_to_db(data_point,parsed_sensor_data)
        counter+=1


        print(f"Temp: {temperature:.1f}°C  Humidity: {humidity:.1f}%")
        lcd.message(f"Temp: {temperature:.1f}°C", 1)
        lcd.message(f"Humidity: {humidity:.1f}%", 2)  
        time.sleep(0.5)  # Continue normal interval between readings

except KeyboardInterrupt:
    print("Stopping program...")

finally:
    dht11.exit()  # Clean up GPIO
    print("GPIO released.")
    lcd.clear()
