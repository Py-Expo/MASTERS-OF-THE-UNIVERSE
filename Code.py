import time
import smbus
import RPi.GPIO as GPIO

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)
bulb_pin = 11  # Example GPIO pin to control the bulb
GPIO.setup(bulb_pin, GPIO.OUT)

# Initialize BMP180
bus = smbus.SMBus(1)
address = 0x77  # BMP180 address
oversampling = 3  # Oversampling setting

# BMP180 Calibration data
AC1 = 408
AC2 = -72
AC3 = -14383
AC4 = 32741
AC5 = 32757
AC6 = 23153
B1 = 6190
B2 = 4
MB = -32768
MC = -8711
MD = 2868

# Function to read BMP180 pressure
def read_pressure():
    # Read uncompensated pressure
    bus.write_byte_data(address, 0xf4, 0x34 + (oversampling << 6))
    time.sleep(0.05)
    msb = bus.read_byte_data(address, 0xf6)
    lsb = bus.read_byte_data(address, 0xf7)
    xlsb = bus.read_byte_data(address, 0xf8)
    raw_pressure = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - oversampling)

    # Calculate true pressure
    X1 = ((raw_pressure - AC6) * AC5) >> 15
    X2 = (MC << 11) // (X1 + MD)
    B5 = X1 + X2
    pressure = ((B5 + 8) >> 4) / 10.0

    return pressure

try:
    while True:
        pressure = read_pressure()

        # Example condition: If pressure is greater than 1000, light up the bulb
        if pressure > 1000:
            GPIO.output(bulb_pin, GPIO.HIGH)
        else:
            GPIO.output(bulb_pin, GPIO.LOW)

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
