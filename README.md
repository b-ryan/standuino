standuino
=========

Code to monitor an arduino for sitting / standing

Prerequisites
=============

```
apt-get install arduino-core
apt-get install picocom
pip install ino
```

Setup Arduino
=============

Check out the sketch
[here](http://arduinobasics.blogspot.com/2012/11/arduinobasics-hc-sr04-ultrasonic-sensor.html).

To give a brief rundown, the ultrasonic sensor needs four connections. You will
see labels for each pin on the front of the sensor. These are named

* `VCC` for voltage
* `Trig` for trigger
* `Echo`
* `GND` for ground

Connect `VCC` pin to 5V power. Connect ground to ground. Connect 7 to `Echo`
and connect 8 to `Trig`.


Build and load
==============

```
cd arduino
ino build
ino upload
```

Serial
======

```
ino serial
```

To quit: `<C-a><C-q>`
