import badger2040
import breakout_scd41
from pimoroni_i2c import PimoroniI2C
import time

BREAKOUT_GARDEN_I2C_PINS = {"sda": 4, "scl": 5}
i2c = PimoroniI2C(**BREAKOUT_GARDEN_I2C_PINS)

breakout_scd41.init(i2c)
breakout_scd41.start()

while True:
    if breakout_scd41.ready():
        co2, temperature, humidity = breakout_scd41.measure()
        print(co2, temperature, humidity)
        badger2040.sleep_for(1)
    time.sleep(1)
