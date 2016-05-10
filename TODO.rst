What's currently not implemented (i.e: the TODO list):
 - exceptions and errors from the micro:bit - any exceptions or other errors
   that originate from the micro:bit are not yet detected by microrepl
 - most of the microbit.Image class
 - microbit.Image.ALL_CLOCKS
 - microbit.Image.ALL_ARROWS
 - microbit.display.show() functions
 - all functions in microbit.uart (see the _microbit_uart class below for more
   information).
 - microbit.spi.write_readinto()
 - re-importing the microbit module after a hard reset
 - checking whether arguments are the right type or not
 - error and type checking pretty much everywhere
 - functions in microbit modules which return True/False will return None upon
   any error (this should either not happen or an exception be thrown)
