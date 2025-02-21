import time
import math

import badger2040
import breakout_scd41
from pimoroni_i2c import PimoroniI2C

BREAKOUT_GARDEN_I2C_PINS = {"sda": 4, "scl": 5}
start = time.time()

# CO2
co2_readings = []
co2_upper = 2000
co2_lower = 500

# Temp
temp_readings = []
temp_upper = 50
temp_lower = 10

# Humidity
hu_readings = []
hu_upper = 100
hu_lower = 0

def drawRectangle(x, y, w, h):
  badger.line(x, y, x+w, y)
  badger.line(x, y, x, y+h)
  badger.line(x, y+h, x+w, y+h)
  badger.line(x+w, y, x+w, y+h)


def centreText(text, x, y, w, scale):
  text_width = badger.measure_text(text, scale)
  badger.text(text, int((w - text_width) / 2) + x, y, False, scale)


def drawMetric(val):
  badger.set_pen(0)
  badger.set_thickness(3)
  val_text = str(math.floor(val))
  centreText(val_text, 0, 52, 148, 1.6)


def drawLowerMetric(temperature, humidity):
  badger.set_pen(0)
  badger.set_thickness(2)
  lower_metric_text = str(math.floor(temperature)) + 'C  ' + \
      str(math.floor(humidity)) + '%'
  centreText(lower_metric_text, 0, 98, 148, 0.7)


def drawGraph(readings, upper, lower, pen):
  # Upper and lower limits for the screen
  graph_y_high = 15
  graph_y_low = 103

  reading_diff = upper - lower
  graph_diff = graph_y_low - graph_y_high
  steps = reading_diff / graph_diff

  x1 = y1 = x2 = y2 = 0
  for index, str_reading in enumerate(readings):

    reading = float(str_reading)
    limited_reading = reading - lower

    if index == 0:
      x1 = 158
      y1 = graph_y_low - round(limited_reading / steps)
    if index != 0:
      x2 = x1 + 8
      y2 = graph_y_low - round(limited_reading / steps)

      if y2 > graph_y_low:
        y2 = graph_y_low
      if y2 < graph_y_high:
        y2 = graph_y_high

      badger.set_pen(pen)
      badger.line(x1, y1, x2, y2, 2)

      x1 = x2
      y1 = y2

def drawScreen(co2, temperature, humidity):
  badger.set_thickness(1)
  badger.set_pen(15)
  badger.clear()
  badger.set_pen(0)

  drawRectangle(148, 10, 138, 108)
  
  drawGraph(co2_readings, co2_upper, co2_lower, 1)
  drawGraph(temp_readings, temp_upper, temp_lower, 5)
  drawGraph(hu_readings, hu_upper, hu_lower, 10)
  
  drawMetric(co2)
  drawLowerMetric(temperature, humidity)
   
  badger.update()


def addReading(reading, store):
  store.append(str(reading))
  if len(store) == 17:
      store.pop(0)
  return store

badger = badger2040.Badger2040()
badger.set_font('sans')

badger.led(255)

try:
  f = open('/readings.txt')
  co2_readings = f.readline().strip().split(",")
  temp_readings = f.readline().strip().split(",")
  hu_readings = f.readline().strip().split(",")
except OSError:
  pass

print("Connecting to sensor")
i2c = PimoroniI2C(**BREAKOUT_GARDEN_I2C_PINS)
breakout_scd41.init(i2c)
breakout_scd41.start()


while True:
  if breakout_scd41.ready():
    co2, temperature, humidity = breakout_scd41.measure()
    print(co2, temperature, humidity)

    co2_readings = addReading(co2, co2_readings)
    temp_readings = addReading(temperature, temp_readings)
    hu_readings = addReading(humidity, hu_readings)

    print("Refreshing screen")
    drawScreen(co2, temperature, humidity)

    try:
      f = open('/readings.txt', 'w')
      f.write(",".join(co2_readings))
      f.write("\n")
      f.write(",".join(temp_readings))
      f.write("\n")
      f.write(",".join(hu_readings))
      f.close()
    except OSError:
      pass

    badger.led(0)

    print("Going to sleep")
    badger2040.sleep_for(5)
  else:
    print("SCD41 Not ready")

  time.sleep(0.1)

