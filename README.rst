===========================
MicroPeri for BBC Microbit
===========================
MicroPeri is quick and easy to use Python 3 library for turning the BBC Microbit into an external peripheral device or sensor.

With it, you can quickly for example read accelerator values, button presses or even write to the LED matrix!

Installation
===============
1. You must first make sure you have a blank MicroPython .hex file loaded onto your Microbit. You can create one `here <https://www.microbit.co.uk/app/#create:xyelfe>`_.
2. If using Windows, you must have the ARM mbed USB serial driver installed. It can be downloaded from `mbed site <https://developer.mbed.org/handbook/Windows-serial-configuration>`_.
3. Install the library with (soon):

    # pip3 install microperi

Notes:
=======
- Some functions and parts of the current micro:bit MicroPython API are not yet implemented - see the TODO.rst file for more information.
- If on Linux, you will need superuser priviledges to open the serial port.

Usage
======
.. code-block:: python

    from microperi import microbit
    microbit.display.scroll("Hello world")
    if microbit.button_a.is_pressed():
        print("Button A is pressed")
    else:
        print("Button A is not pressed")

