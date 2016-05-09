# microperi.py
# Part of MicroPeri https://github.com/JoeGlancy/microperi
#
# See LICENSE file for copyright and license details

# MicroPeri is a library for using the BBC Microbit with MicroPython as an
# external peripheral device or sensor.

if __name__ == "__main__":
    # this shouldn't be run as a file
    import os, sys
    name = os.path.basename(__file__)
    if name[-3:] == ".py":
        name = name[:-3]
    print("Use me as a module:\n    from %s import microbit" % (name))
    sys.exit(1)

import serial

class _C_microbit_image_class:
    """
    Class representing the microbit.Image class. Currently incomplete.

    >>> str(microbit.Image.SNAKE)
    "Image(\n    '99000:'\n    '99099:'\n    '09090:'\n    '09990:'\n    '00000:'\n)"
    >>> repr(microbit.Image.SNAKE)
    "Image('99000:99099:09090:09990:00000:')"

    """
    _M_image_string = None
    _M_img_width = None
    _M_img_height = None
    _M_img_buffer = None
    _M_is_string = False
    _M_is_readonly = False

    def __init__(self, string=None, width=None, height=None, buffer=None,
                 _V_microrepl_isreadonly=False):
        if string is not None:
            self._M_is_string = True
            if isinstance(string, _C_microbit_image_class):
                string = string._M_image_string
            string.replace("\n", ":")
            self._M_image_string = string
            self._M_img_width = 5
            self._M_img_height = 5
        else:
            self._M_img_width = width
            self._M_img_height = height
            if buffer is not None:
                self._M_image_string = buffer
            else:
                self._M_image_string = "00000:00000:00000:00000:00000"
        _M_is_readonly = _V_microrepl_isreadonly

    def _F_is_out_of_bounds(self, x, y):
        if x + y * (self._M_img_height - 1) > self._M_img_width * self._M_img_height - 1 or \
            y < 0 or y > self._M_img_height - 1 or \
            x < 0 or x > self._M_img_width - 1:
            return True
        return False

    def width(self):
        return self._M_img_width

    def height(self):
        return self._M_img_height

    def set_pixel(self, x, y, value):
        if self._M_is_readonly:
            raise Exception("You cannot modify read-only images!")
        if self._F_is_out_of_bounds(x, y):
            raise Exception("Specified index is out of bounds!")
        index = x + y * (self._M_img_height)
        self._M_image_string = self._M_image_string[:index-1] + str(value) + \
            self._M_image_string[:index+1]
        return None

    def get_pixel(self, x, y):
        if self._F_is_out_of_bounds(x, y):
            raise Exception("Specified index is out of bounds!")
        return int(self._M_image_string[x + y * (self._M_img_height)])

class _C_microbit:
    """
    Main class, which represents the microibt module. Everything goes in here.
    """
    _M_ubit_conn = None

    # buttons
    button_a = None
    button_b = None

    # pins
    pin0  = None
    pin1  = None
    pin2  = None
    pin3  = None
    pin4  = None
    pin5  = None
    pin6  = None
    pin7  = None
    pin8  = None
    pin9  = None
    pin10 = None
    pin11 = None
    pin12 = None
    pin13 = None
    pin14 = None
    pin15 = None
    pin16 = None
    pin19 = None
    pin20 = None

    # display module
    display = None

    # UART module (not implemented as trying to create a serial connection will
    # cut the connection between the micro:bit and the host
    uart = None

    # spi module
    spi = None

    # accelerometer module
    accelerometer = None

    # compass module
    compass = None

    # classes
    class _C_microbit_connection:
        """
        Class which handles the sending and receiving of data to and from the
        micro:bit over the serial connection.
        """
        conn = None

        def __init__(self):
            """
            Constructor. Attempts to find the micro:bit, and raises an Exception
            if one can't be found.
            """
            port = self.guess_port()
            if port is None:
                raise Exception("Could not find micro:bit!")

            self.conn = serial.Serial(port, 115200, timeout=1)
            self.write("")
            self.post_reset()

        def guess_port(self):
            """
            From https://github.com/ntoll/microrepl
            Returns the port for the first micro:bit found connected to the computer
            running this script. If no micro:bit is found, returns None.
            """
            import sys
            from serial.tools.list_ports import comports as list_serial_ports
            ports = list_serial_ports()
            platform = sys.platform
            if platform.startswith("linux"):
                for port in ports:
                    if "VID:PID=0D28:0204" in port[2].upper():
                        return port[0]
            elif platform.startswith("darwin"):
                for port in ports:
                    if "VID:PID=0D28:0204" in port[2].upper():
                        return port[0]
            elif platform.startswith("win"):
                for port in ports:
                    if "VID:PID=0D28:0204" in port[2].upper():
                        return port[0]
            return None

        def write(self, data):
            """
            Writes a string of data plus a carriage return ("\r") to the serial
            connection, after encoding it.
            """
            self.conn.write(str(data + "\r").encode())

        def readlines(self, strip=True, decode=True):
            """
            Continuously reads data from the serial connection until a ">>>" is
            encountered.
            """
            self.conn.readline()
            dataArray = bytes()
            dataDecodedStr = ""
            while True:
                try:
                    data = self.conn.readline()
                    dataDecoded = data.decode()
                except:
                    break
                if dataDecoded.rstrip() == ">>>":
                    break
                dataDecodedStr += dataDecoded
                dataArray += data
            if strip:
                dataDecodedStr = dataDecodedStr.rstrip('\n').rstrip('\r')
            if decode:
                return dataDecodedStr
            return dataArray

        def execute(self, command, strip=True, decode=True):
            """
            Executes the specified command, and returns the result. `strip`
            specifies whether to strip the whole of the output, or just the
            carriage return at the very end.
            """
            self.write(command)
            return self.readlines(strip, decode)

        def post_reset(self):
            """
            Function executed after a device reset is called. It waits for the
            ">>>" prompt to appear, and then imports the microbit module, ready
            for use.
            """
            self.execute("")
            self.execute("import microbit")

    class _C_microbit_display:
        """
        Class which represents the microbit.display module.
        """
        _M_ubit_conn = None

        def __init__(self, conn):
            self._M_ubit_conn = conn

        def _F_unimplemented(self):
            raise Exception("Unimplemented function")

        def get_pixel(self, x, y):
            s = self._M_ubit_conn.execute("microbit.display.get_pixel(%d,%d)" % (x, y))
            try:
                return int(s)
            except:
                return None

        def set_pixel(self, x, y, value):
            self._M_ubit_conn.execute("microbit.display.set_pixel(%d,%d,%d)" % (x, y, value))
            return None

        def clear(self):
            self._M_ubit_conn.execute("microbit.display.clear()")
            return None

        def show(self, image):
            self._F_unimplemented()

        def show(self, iterable, delay, wait=True, loop=False, clear=False):
            self._F_unimplemented()

        def scroll(self, string, delay=400):
            self._M_ubit_conn.execute("microbit.display.scroll(\"%s\",%d)" % (string, delay))
            return None

    class _C_microbit_uart:
        """
        Class representing the microbit.uart module. Everything is unimplemented,
        and attempting to call any of the functions contained will result in an
        Exception being thrown. This is because the serial connection over USB
        (which is what this module uses to send and receive data from the
        micro:bit) will be cut and used instead for the newly created connection,
        as there is only one hardware serial chip which cannot be shared.
        """
        def _F_unimplemented(self):
            raise Exception("The microbit.uart module is not implemented, as it will render this module useless")

        def init(self, baudrate=9600, bits=8, parity=None, stop=1, *, tx=None, rx=None):
            self._F_unimplemented()

        def any(self):
            self._F_unimplemented()

        def read(self, nbytes=None):
            self._F_unimplemented()

        def readall(self, ):
            self._F_unimplemented()

        def readinto(self, buf, nbytes=None):
            self._F_unimplemented()

        def readline(self):
            self._F_unimplemented()

        def write(self, buf):
            self._F_unimplemented()

    class _C_microbit_spi:
        """
        Class representing the microbit.api module. The function
        `write_readinto(outbuf, inbuf)` is currently not implemented.
        """
        _M_ubit_conn = None
        _M_default_sclk = None
        _M_default_mosi = None
        _M_default_miso = None

        def __init__(self, conn, default_sclk, default_mosi, default_miso):
            self._M_ubit_conn = conn
            self._M_default_sclk = default_sclk
            self._M_default_mosi = default_mosi
            self._M_default_miso = default_miso

        def _F_unimplemented(self):
            raise Exception("Unimplemented function")

        def init(self, baudrate=1000000, bits=8, mode=0, sclk=None, mosi=None, miso=None):
            if sclk is None:
                sclk = self._M_default_sclk
            if mosi is None:
                mosi = self._M_default_mosi
            if miso is None:
                miso = self._M_default_miso

            if not isinstance(sclk, self._C_microbit_pin) or not isinstance(mosi, self._C_microbit_pin) or \
                not isinstance(miso, self._C_microbit_pin):
                raise Exception("sclk must be an instance of one of:\n    microbit.MicroBitDigitalPin\n    microbit.MicroBitAnalogDigitalPin\n    microbit.MicroBitTouchPin")

            self._M_ubit_conn.execute("microbit.spi.init(baudrate=%d,bits=%d,mode=%d,sclk=%s,mosi=%s,miso=%s)" % \
                                      (baudrate, bits, mode, \
                                      "microbit.%s" % (sclk._M_pin_name), \
                                      "microbit.%s" % (mosi._M_pin_name), \
                                      "microbit.%s" % (miso._M_pin_name)))
            return None

        def read(self, nbytes):
            data = self._M_ubit_conn.execute("microbit.spi.read(%d)" % (nbytes),
                                             decode=False)
            return data[2:-1] # make sure to remove the

        def write(self, buffer):
            if not isinstance(buffer, bytes):
                #buffer = str(buffer)[2:-1] # TODO check this logic
                raise Exception("Expected bytes, not %s!" % (type(buffer)))
            self._M_ubit_conn.execute("microbit.spi.write(b\"%s\")" % (buffer))
            return None

        def write_readinto(self, outbuf, inbuf):
            if not isinstance(out, str):
                out = str(out)[2:-1]
            self._F_unimplemented()

    class _C_microbit_i2c:
        """
        Class representing the microbit.i2c module.
        """
        _M_ubit_conn = None

        def __init__(self, conn):
            self._M_ubit_conn = conn

        def read(self, addr, n, repeat=False):
            data = self._M_ubit_conn.execute("microbit.i2c.read(%x,%d,repeat=%s)" % \
                                             (addr, n, repeat), decode=False)
            return data[2:-1]

        def write(addr, buf, repeat=False):
            if not isinstance(buffer, bytes):
                #buffer = str(buffer)[2:-1] # TODO check this logic
                raise Exception("Expected bytes, not %s!" % (type(buffer)))
            self._M_ubit_conn.execute("microbit.i2c.write(%x,b\"%s\",repeat=%s)" % \
                                      (addr, buf, repeat))
            return None

    class _C_microbit_accelerometer:
        """
        Class representing the microbit.accelerometer module.
        """
        _M_ubit_conn = None

        def __init__(self, conn):
            self._M_ubit_conn = conn

        def get_x(self):
            s = self._M_ubit_conn.execute("microbit.accelerometer.get_x()")
            try:
                return int(s)
            except:
                return None

        def get_y(self):
            s = self._M_ubit_conn.execute("microbit.accelerometer.get_y()")
            try:
                return int(s)
            except:
                return None

        def get_z(self):
            s = self._M_ubit_conn.execute("microbit.accelerometer.get_z()")
            try:
                return int(s)
            except:
                return None

        def get_values(self):
            return (self.get_x(), self.get_y(), self.get_z())

        def current_gesture(self):
            s = self._M_ubit_conn.execute("microbit.accelerometer.get_z()")
            return s

        def is_gesture(self, name):
            s = self._M_ubit_conn.execute("microbit.accelerometer.is_gesture(%s)" % \
                                          (name))
            if s == "True":
                return True
            elif s == "False":
                return False
            else:
                return None

        def was_gesture(self, name):
            s = self._M_ubit_conn.execute("microbit.accelerometer.was_gesture(%s)" % \
                                          (name))
            if s == "True":
                return True
            elif s == "False":
                return False
            else:
                return None

        def get_gestures(self):
            s = self._M_ubit_conn.execute("microbit.accelerometer.get_gestures()") \
                    .replace(" ", "")[1:-1]
            result = ()
            for i in s.split(","):
                result = result + (i,)
            return result

    class _C_microbit_compass:
        """
        Class representing the microbit.compass module.
        """
        _M_ubit_conn = None

        def __init__(self, conn):
            self._M_ubit_conn = conn

        def calibrate(self):
            self._M_ubit_conn.execute("microbit.compass.calibrate()")
            return None

        def is_calibrated(self):
            s = self._M_ubit_conn.execute("microbit.compass.is_calibrated()")
            if s == "True":
                return True
            elif s == "False":
                return False
            else:
                return None

        def clear_calibration(self):
            self._M_ubit_conn.execute("microbit.compass.clear_calibration()")
            return None

        def get_x(self):
            s = self._M_ubit_conn.execute("microbit.compass.get_x()")
            try:
                return int(s)
            except:
                return None

        def get_y(self):
            s = self._M_ubit_conn.execute("microbit.compass.get_y()")
            try:
                return int(s)
            except:
                return None

        def get_z(self):
            s = self._M_ubit_conn.execute("microbit.compass.get_z()")
            try:
                return int(s)
            except:
                return None

        def heading(self):
            s = self._M_ubit_conn.execute("microbit.compass.heading()")
            try:
                return int(s)
            except:
                return None

        def get_field_strength(self):
            s = self._M_ubit_conn.execute("microbit.compass.get_field_strength()")
            try:
                return int(s)
            except:
                return None

    class _C_microbit_pin:
        """
        This class facilitates isinstance-ing of the other pin classes, and also
        provides the _M_pin_name member. It serves no other real purpose.
        """
        _M_pin_name = None

    # microbit module classes
    class Image(_C_microbit_image_class):
        # constants (these are all readonly images)
        HEART           = _C_microbit_image_class("01010:11111:11111:01110:00100", _V_microrepl_isreadonly=True)
        HEART_SMALL     = _C_microbit_image_class("00000:01010:01110:00100:00000", _V_microrepl_isreadonly=True)
        HAPPY           = _C_microbit_image_class("00000:01010:00000:10001:01110", _V_microrepl_isreadonly=True)
        SMILE           = _C_microbit_image_class("00000:00000:00000:10001:01110", _V_microrepl_isreadonly=True)
        SAD             = _C_microbit_image_class("00000:01010:00000:01110:10001", _V_microrepl_isreadonly=True)
        CONFUSED        = _C_microbit_image_class("00000:01010:00000:01010:10101", _V_microrepl_isreadonly=True)
        ANGRY           = _C_microbit_image_class("10001:01010:00000:11111:10101", _V_microrepl_isreadonly=True)
        ASLEEP          = _C_microbit_image_class("00000:11011:00000:01110:00000", _V_microrepl_isreadonly=True)
        SURPRISED       = _C_microbit_image_class("01010:00000:00100:01010:00100", _V_microrepl_isreadonly=True)
        SILLY           = _C_microbit_image_class("10001:00000:11111:00101:00111", _V_microrepl_isreadonly=True)
        FABULOUS        = _C_microbit_image_class("11111:11011:00000:01010:01110", _V_microrepl_isreadonly=True)
        MEH             = _C_microbit_image_class("01010:00000:00010:00100:01000", _V_microrepl_isreadonly=True)
        YES             = _C_microbit_image_class("00000:00001:00010:10100:01000", _V_microrepl_isreadonly=True)
        NO              = _C_microbit_image_class("10001:01010:00100:01010:10001", _V_microrepl_isreadonly=True)
        CLOCK12         = _C_microbit_image_class("00100:00100:00100:00000:00000", _V_microrepl_isreadonly=True)
        CLOCK1          = _C_microbit_image_class("00010:00010:00100:00000:00000", _V_microrepl_isreadonly=True)
        CLOCK2          = _C_microbit_image_class("00000:00011:00100:00000:00000", _V_microrepl_isreadonly=True)
        CLOCK3          = _C_microbit_image_class("00000:00000:00111:00000:00000", _V_microrepl_isreadonly=True)
        CLOCK4          = _C_microbit_image_class("00000:00000:00100:00011:00000", _V_microrepl_isreadonly=True)
        CLOCK5          = _C_microbit_image_class("00000:00000:00100:00010:00010", _V_microrepl_isreadonly=True)
        CLOCK6          = _C_microbit_image_class("00000:00000:00100:00100:00100", _V_microrepl_isreadonly=True)
        CLOCK7          = _C_microbit_image_class("00000:00000:00100:01000:01000", _V_microrepl_isreadonly=True)
        CLOCK8          = _C_microbit_image_class("00000:00000:00100:11000:00000", _V_microrepl_isreadonly=True)
        CLOCK9          = _C_microbit_image_class("00000:00000:11100:00000:00000", _V_microrepl_isreadonly=True)
        CLOCK10         = _C_microbit_image_class("00000:11000:00100:00000:00000", _V_microrepl_isreadonly=True)
        CLOCK11         = _C_microbit_image_class("01000:01000:00100:00000:00000", _V_microrepl_isreadonly=True)
        ARROW_N         = _C_microbit_image_class("00100:01110:10101:00100:00100", _V_microrepl_isreadonly=True)
        ARROW_NE        = _C_microbit_image_class("00111:00011:00101:01000:10000", _V_microrepl_isreadonly=True)
        ARROW_E         = _C_microbit_image_class("00100:00010:11111:00010:00100", _V_microrepl_isreadonly=True)
        ARROW_SE        = _C_microbit_image_class("10000:01000:00101:00011:00111", _V_microrepl_isreadonly=True)
        ARROW_S         = _C_microbit_image_class("00100:00100:10101:01110:00100", _V_microrepl_isreadonly=True)
        ARROW_SW        = _C_microbit_image_class("00001:00010:10100:11000:11100", _V_microrepl_isreadonly=True)
        ARROW_W         = _C_microbit_image_class("00100:01000:11111:01000:00100", _V_microrepl_isreadonly=True)
        ARROW_NW        = _C_microbit_image_class("11100:11000:10100:00010:00001", _V_microrepl_isreadonly=True)
        TRIANGLE        = _C_microbit_image_class("00000:00100:01010:11111:00000", _V_microrepl_isreadonly=True)
        TRIANGLE_LEFT   = _C_microbit_image_class("10000:11000:10100:10010:11111", _V_microrepl_isreadonly=True)
        CHESSBOARD      = _C_microbit_image_class("01010:10101:01010:10101:01010", _V_microrepl_isreadonly=True)
        DIAMOND         = _C_microbit_image_class("00100:01010:10001:01010:00100", _V_microrepl_isreadonly=True)
        DIAMOND_SMALL   = _C_microbit_image_class("00000:00100:01010:00100:00000", _V_microrepl_isreadonly=True)
        SQUARE          = _C_microbit_image_class("11111:10001:10001:10001:11111", _V_microrepl_isreadonly=True)
        SQUARE_SMALL    = _C_microbit_image_class("00000:01110:01010:01110:00000", _V_microrepl_isreadonly=True)
        RABBIT          = _C_microbit_image_class("10100:10100:11110:11010:11110", _V_microrepl_isreadonly=True)
        COW             = _C_microbit_image_class("10001:10001:11111:01110:00100", _V_microrepl_isreadonly=True)
        MUSIC_CROTCHET  = _C_microbit_image_class("00100:00100:00100:11100:11100", _V_microrepl_isreadonly=True)
        MUSIC_QUAVER    = _C_microbit_image_class("00100:00110:00101:11100:11100", _V_microrepl_isreadonly=True)
        MUSIC_QUAVERS   = _C_microbit_image_class("01111:01001:01001:11011:11011", _V_microrepl_isreadonly=True)
        PITCHFORK       = _C_microbit_image_class("10101:10101:11111:00100:00100", _V_microrepl_isreadonly=True)
        XMAS            = _C_microbit_image_class("00100:01110:00100:01110:11111", _V_microrepl_isreadonly=True)
        PACMAN          = _C_microbit_image_class("01111:11010:11100:11110:01111", _V_microrepl_isreadonly=True)
        TARGET          = _C_microbit_image_class("00100:01110:11011:01110:00100", _V_microrepl_isreadonly=True)
        TSHIRT          = _C_microbit_image_class("11011:11111:01110:01110:01110", _V_microrepl_isreadonly=True)
        ROLLERSKATE     = _C_microbit_image_class("00011:00011:11111:11111:01010", _V_microrepl_isreadonly=True)
        DUCK            = _C_microbit_image_class("01100:11100:01111:01110:00000", _V_microrepl_isreadonly=True)
        HOUSE           = _C_microbit_image_class("00100:01110:11111:01110:01010", _V_microrepl_isreadonly=True)
        TORTOISE        = _C_microbit_image_class("00000:01110:11111:01010:00000", _V_microrepl_isreadonly=True)
        BUTTERFLY       = _C_microbit_image_class("11011:11111:00100:11111:11011", _V_microrepl_isreadonly=True)
        STICKFIGURE     = _C_microbit_image_class("00100:11111:00100:01010:10001", _V_microrepl_isreadonly=True)
        GHOST           = _C_microbit_image_class("11111:10101:11111:11111:10101", _V_microrepl_isreadonly=True)
        SWORD           = _C_microbit_image_class("00100:00100:00100:01110:00100", _V_microrepl_isreadonly=True)
        GIRAFFE         = _C_microbit_image_class("11000:01000:01000:01110:01010", _V_microrepl_isreadonly=True)
        SKULL           = _C_microbit_image_class("01110:10101:11111:01110:01110", _V_microrepl_isreadonly=True)
        UMBRELLA        = _C_microbit_image_class("01110:11111:00100:10100:01100", _V_microrepl_isreadonly=True)
        SNAKE           = _C_microbit_image_class("11000:11011:01010:01110:00000", _V_microrepl_isreadonly=True)

    class Button:
        """
        Class representing one of the micro:bit's buttons (microbit.button_a and
        microbit.button_b).
        """
        _M_ubit_conn = None
        _M_button_name = None

        def __init__(self, conn, name):
            self._M_ubit_conn = conn
            self._M_button_name = name

        def __str__(self):
            return

        def is_pressed(self):
            s = self._M_ubit_conn.execute("microbit.%s.is_pressed()" % (self._M_button_name))
            if s == "True":
                return True
            elif s == "False":
                return False
            else:
                return None

        def was_pressed(self):
            s = self._M_ubit_conn.execute("microbit.%s.was_pressed()" % (self._M_button_name))
            if s == "True":
                return True
            elif s == "False":
                return False
            else:
                return None

        def get_presses(self):
            s = self._M_ubit_conn.execute("microbit.%s.get_presses()" % (self._M_button_name))
            try:
                return int(s)
            except:
                return None

    class MicroBitDigitalPin(_C_microbit_pin):
        """
        Class representing a digital pin on the micro:bit (pins 5-9, 11-16, 19
        and 20).
        """
        _M_ubit_conn = None

        def __init__(self, conn, name):
            self._M_ubit_conn = conn
            self._M_pin_name = name

        def read_digital(self):
            s = self._M_ubit_conn.execute("microbit.%s.read_digital()" % (self._M_pin_name))
            try:
                return int(s)
            except:
                return None

        def write_digital(self, value):
            self._M_ubit_conn.execute("microbit.%s.write_digital(%d)" % (self._M_pin_name, value))
            return None

    class MicroBitAnalogDigitalPin(_C_microbit_pin):
        """
        Class representing an analog pin on the micro:bit (pins 3, 4 and 10).
        """
        _M_ubit_conn = None

        def __init__(self, conn, name):
            self._M_ubit_conn = conn
            self._M_pin_name = name

        def read_analog(self):
            s = self._M_ubit_conn.execute("microbit.%s.read_analog()" % (self._M_pin_name))
            try:
                return int(s)
            except:
                return None

        def write_analog(self, value):
            self._M_ubit_conn.execute("microbit.%s.write_analog(%d)" % (self._M_pin_name, value))
            return None

        def set_analog_period(self, period):
            self._M_ubit_conn.execute("microbit.%s.set_analog_period(%d)" % (self._M_pin_name, period))
            return None

        def set_analog_period_microseconds(self, period):
            self._M_ubit_conn.execute("microbit.%s.set_analog_period_microseconds(%d)" % (self._M_pin_name, period))
            return None

    class MicroBitTouchPin(_C_microbit_pin):
        """
        Class representing one of the three large pins on the micro:bit's pin
        array (called touch pins).
        """
        _M_ubit_conn = None

        def __init__(self, conn, name):
            self._M_ubit_conn = conn
            self._M_pin_name = name

        def is_touched(self):
            s = self._M_ubit_conn.execute("microbit.%s.is_touched()" % (self._M_pin_name))
            if s == "True":
                return True
            elif s == "False":
                return False
            else:
                return None

    # functions
    # constructor
    def __init__(self):
        self._M_ubit_conn = self._C_microbit_connection()

        self.button_a = self.Button(self._M_ubit_conn, "button_a")
        self.button_b = self.Button(self._M_ubit_conn, "button_b")

        self.pin0 = self.MicroBitTouchPin(self._M_ubit_conn, "pin0")
        self.pin1 = self.MicroBitTouchPin(self._M_ubit_conn, "pin1")
        self.pin2 = self.MicroBitTouchPin(self._M_ubit_conn, "pin2")
        self.pin3 = self.MicroBitAnalogDigitalPin(self._M_ubit_conn, "pin3")
        self.pin4 = self.MicroBitAnalogDigitalPin(self._M_ubit_conn, "pin4")
        self.pin5 = self.MicroBitDigitalPin(self._M_ubit_conn, "pin5")
        self.pin6 = self.MicroBitDigitalPin(self._M_ubit_conn, "pin6")
        self.pin7 = self.MicroBitDigitalPin(self._M_ubit_conn, "pin7")
        self.pin8 = self.MicroBitDigitalPin(self._M_ubit_conn, "pin8")
        self.pin9 = self.MicroBitDigitalPin(self._M_ubit_conn, "pin9")
        self.pin10 = self.MicroBitAnalogDigitalPin(self._M_ubit_conn, "pin10")
        self.pin11 = self.MicroBitDigitalPin(self._M_ubit_conn, "pin11")
        self.pin12 = self.MicroBitDigitalPin(self._M_ubit_conn, "pin12")
        self.pin13 = self.MicroBitDigitalPin(self._M_ubit_conn, "pin13")
        self.pin14 = self.MicroBitDigitalPin(self._M_ubit_conn, "pin14")
        self.pin15 = self.MicroBitDigitalPin(self._M_ubit_conn, "pin15")
        self.pin16 = self.MicroBitDigitalPin(self._M_ubit_conn, "pin16")
        self.pin19 = self.MicroBitDigitalPin(self._M_ubit_conn, "pin19")
        self.pin20 = self.MicroBitDigitalPin(self._M_ubit_conn, "pin20")

        self.display = self._C_microbit_display(self._M_ubit_conn)

        self.uart = self._C_microbit_uart()

        self.spi = self._C_microbit_spi(self._M_ubit_conn, self.pin13,
                                        self.pin15, self.pin14)

        self.i2c = self._C_microbit_i2c(self._M_ubit_conn)

        self.accelerometer = self._C_microbit_accelerometer(self._M_ubit_conn)
        self.compass = self._C_microbit_compass(self._M_ubit_conn)

    def panic(self, n):
        self._M_ubit_conn.execute("microbit.panic(%d)" % (n))
        self._M_ubit_conn.post_reset()
        return None

    def reset(self):
        self._M_ubit_conn.execute("microbit.reset()")
        self._M_ubit_conn.post_reset()
        return None

    def sleep(self, n):
        # NOTE: this could use time.sleep instead
        self._M_ubit_conn.execute("microbit.sleep(%d)" % (n))
        return None

    def running_time(self):
        s = self._M_ubit_conn.execute("microbit.running_time()")
        try:
            return int(s)
        except:
            return None

    def temperature(self):
        s = self._M_ubit_conn.execute("microbit.temperature()")
        try:
            return int(s)
        except:
            return None

microbit = _C_microbit()
microbit.reset()
