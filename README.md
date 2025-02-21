# Badgerwatch

Scripts for the CO2 sensor project in Raspberry Pi Magazine. This project
uses a Pimoroni Badger 2040 W with a Circuitgarden CO2 sensor to provide
reading on CO2, temperature and humidity. It can also transmit those
readings as MQTT payloads. Deep sleep means it can run off a 1200mAh LiPo
battery for weeks based on a reading every 5 minutes.

Intended to only be run on a Pimoroni Badger 2024 W

Please see the magazine for full information on usage.

## You'll need

- Badger 2040 W: https://shop.pimoroni.com/products/badger-2040-w
- SCD41 CO2 Sensor: https://shop.pimoroni.com/products/scd41-co2-sensor-breakout
- Lipo Amigo: https://shop.pimoroni.com/products/lipo-amigo
- 1200mAh 3.7V LiPo Battery: https://thepihut.com/products/1200mah-3-7v-lipo-battery
- 4 Pin JST-SH Cable (50mm): https://shop.pimoroni.com/products/jst-sh-cable-qwiic-stemma-qt-compatible

## tl;cr (Too late, couldn't read)

- Connect a CO2 sensor to the QT/SW connector on the Badger
- Ensure the Badger is running Pimoroni-flavoured Badger OS (MicroPython)
- Copy all these files to the Badger's root filesystem over USB
- Edit WIFI_CONFIG.py and MQTT_CONFIG.py (if using) to suit
- Edit your main.py:

If using MQTT/Wifi:

`import co2_mqtt`

If not:

`import co2`

You should now have a CO2 sensor! Add the LiPo batter and charger for true portability.