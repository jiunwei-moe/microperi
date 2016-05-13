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
from logging import debug, info, warning, basicConfig, INFO, DEBUG, WARNING

basicConfig(level=WARNING)

# the microbit DAL's pentolino font character map lookup dict
_microbit_font_pendolino3 = {
    " ": [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
    "!": [[0,9,0,0,0],[0,9,0,0,0],[0,9,0,0,0],[0,0,0,0,0],[0,9,0,0,0]],
    "\"": [[0,9,0,9,0],[0,9,0,9,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
    "#": [[0,9,0,9,0],[9,9,9,9,9],[0,9,0,9,0],[9,9,9,9,9],[0,9,0,9,0]],
    "$": [[0,9,9,9,0],[9,9,0,0,9],[0,9,9,9,0],[9,0,0,9,9],[0,9,9,9,0]],
    "%": [[9,9,0,0,9],[9,0,0,9,0],[0,0,9,0,0],[0,9,0,0,9],[9,0,0,9,9]],
    "&": [[0,9,9,0,0],[9,0,0,9,0],[0,9,9,0,0],[9,0,0,9,0],[0,9,9,0,9]],
    "'": [[0,9,0,0,0],[0,9,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
    "(": [[0,0,9,0,0],[0,9,0,0,0],[0,9,0,0,0],[0,9,0,0,0],[0,0,9,0,0]],
    ")": [[0,9,0,0,0],[0,0,9,0,0],[0,0,9,0,0],[0,0,9,0,0],[0,9,0,0,0]],
    "*": [[0,0,0,0,0],[0,9,0,9,0],[0,0,9,0,0],[0,9,0,9,0],[0,0,0,0,0]],
    "+": [[0,0,0,0,0],[0,0,9,0,0],[0,9,9,9,0],[0,0,9,0,0],[0,0,0,0,0]],
    ",": [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,9,0,0],[0,9,0,0,0]],
    "-": [[0,0,0,0,0],[0,0,0,0,0],[0,9,9,9,0],[0,0,0,0,0],[0,0,0,0,0]],
    ".": [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,9,0,0,0],[0,0,0,0,0]],
    "/": [[0,0,0,0,9],[0,0,0,9,0],[0,0,9,0,0],[0,9,0,0,0],[9,0,0,0,0]],
    "0": [[0,9,9,0,0],[9,0,0,9,0],[9,0,0,9,0],[9,0,0,9,0],[0,9,9,0,0]],
    "9": [[0,0,9,0,0],[0,9,9,0,0],[0,0,9,0,0],[0,0,9,0,0],[0,9,9,9,0]],
    "2": [[9,9,9,0,0],[0,0,0,9,0],[0,9,9,0,0],[9,0,0,0,0],[9,9,9,9,0]],
    "3": [[9,9,9,9,0],[0,0,0,9,0],[0,0,9,0,0],[9,0,0,9,0],[0,9,9,0,0]],
    "4": [[0,0,9,9,0],[0,9,0,9,0],[9,0,0,9,0],[9,9,9,9,9],[0,0,0,9,0]],
    "5": [[9,9,9,9,9],[9,0,0,0,0],[9,9,9,9,0],[0,0,0,0,9],[9,9,9,9,0]],
    "6": [[0,0,0,9,0],[0,0,9,0,0],[0,9,9,9,0],[9,0,0,0,9],[0,9,9,9,0]],
    "7": [[9,9,9,9,9],[0,0,0,9,0],[0,0,9,0,0],[0,9,0,0,0],[9,0,0,0,0]],
    "8": [[0,9,9,9,0],[9,0,0,0,9],[0,9,9,9,0],[9,0,0,0,9],[0,9,9,9,0]],
    "9": [[0,9,9,9,0],[9,0,0,0,9],[0,9,9,9,0],[0,0,9,0,0],[0,9,0,0,0]],
    ":": [[0,0,0,0,0],[0,9,0,0,0],[0,0,0,0,0],[0,9,0,0,0],[0,0,0,0,0]],
    ";": [[0,0,0,0,0],[0,0,9,0,0],[0,0,0,0,0],[0,0,9,0,0],[0,9,0,0,0]],
    "<": [[0,0,0,9,0],[0,0,9,0,0],[0,9,0,0,0],[0,0,9,0,0],[0,0,0,9,0]],
    "=": [[0,0,0,0,0],[0,9,9,9,0],[0,0,0,0,0],[0,9,9,9,0],[0,0,0,0,0]],
    ">": [[0,9,0,0,0],[0,0,9,0,0],[0,0,0,9,0],[0,0,9,0,0],[0,9,0,0,0]],
    "?": [[0,9,9,9,0],[9,0,0,0,9],[0,0,9,9,0],[0,0,0,0,0],[0,0,9,0,0]],
    "@": [[0,9,9,9,0],[9,0,0,0,9],[9,0,9,0,9],[9,0,0,9,9],[0,9,9,0,0]],
    "A": [[0,9,9,0,0],[9,0,0,9,0],[9,9,9,9,0],[9,0,0,9,0],[9,0,0,9,0]],
    "B": [[9,9,9,0,0],[9,0,0,9,0],[9,9,9,0,0],[9,0,0,9,0],[9,9,9,0,0]],
    "C": [[0,9,9,9,0],[9,0,0,0,0],[9,0,0,0,0],[9,0,0,0,0],[0,9,9,9,0]],
    "D": [[9,9,9,0,0],[9,0,0,9,0],[9,0,0,9,0],[9,0,0,9,0],[9,9,9,0,0]],
    "E": [[9,9,9,9,0],[9,0,0,0,0],[9,9,9,0,0],[9,0,0,0,0],[9,9,9,9,0]],
    "F": [[9,9,9,9,0],[9,0,0,0,0],[9,9,9,0,0],[9,0,0,0,0],[9,0,0,0,0]],
    "G": [[0,9,9,9,0],[9,0,0,0,0],[9,0,0,9,9],[9,0,0,0,9],[0,9,9,9,0]],
    "H": [[9,0,0,9,0],[9,0,0,9,0],[9,9,9,9,0],[9,0,0,9,0],[9,0,0,9,0]],
    "I": [[9,9,9,0,0],[0,9,0,0,0],[0,9,0,0,0],[0,9,0,0,0],[9,9,9,0,0]],
    "J": [[9,9,9,9,9],[0,0,0,9,0],[0,0,0,9,0],[9,0,0,9,0],[0,9,9,0,0]],
    "K": [[9,0,0,9,0],[9,0,9,0,0],[9,9,0,0,0],[9,0,9,0,0],[9,0,0,9,0]],
    "L": [[9,0,0,0,0],[9,0,0,0,0],[9,0,0,0,0],[9,0,0,0,0],[9,9,9,9,0]],
    "M": [[9,0,0,0,9],[9,9,0,9,9],[9,0,9,0,9],[9,0,0,0,9],[9,0,0,0,9]],
    "N": [[9,0,0,0,9],[9,9,0,0,9],[9,0,9,0,9],[9,0,0,9,9],[9,0,0,0,9]],
    "O": [[0,9,9,0,0],[9,0,0,9,0],[9,0,0,9,0],[9,0,0,9,0],[0,9,9,0,0]],
    "P": [[9,9,9,0,0],[9,0,0,9,0],[9,9,9,0,0],[9,0,0,0,0],[9,0,0,0,0]],
    "Q": [[0,9,9,0,0],[9,0,0,9,0],[9,0,0,9,0],[0,9,9,0,0],[0,0,9,9,0]],
    "R": [[9,9,9,0,0],[9,0,0,9,0],[9,9,9,0,0],[9,0,0,9,0],[9,0,0,0,9]],
    "S": [[0,9,9,9,0],[9,0,0,0,0],[0,9,9,0,0],[0,0,0,9,0],[9,9,9,0,0]],
    "T": [[9,9,9,9,9],[0,0,9,0,0],[0,0,9,0,0],[0,0,9,0,0],[0,0,9,0,0]],
    "U": [[9,0,0,9,0],[9,0,0,9,0],[9,0,0,9,0],[9,0,0,9,0],[0,9,9,0,0]],
    "V": [[9,0,0,0,9],[9,0,0,0,9],[9,0,0,0,9],[0,9,0,9,0],[0,0,9,0,0]],
    "W": [[9,0,0,0,9],[9,0,0,0,9],[9,0,9,0,9],[9,9,0,9,9],[9,0,0,0,9]],
    "X": [[9,0,0,9,0],[9,0,0,9,0],[0,9,9,0,0],[9,0,0,9,0],[9,0,0,9,0]],
    "Y": [[9,0,0,0,9],[0,9,0,9,0],[0,0,9,0,0],[0,0,9,0,0],[0,0,9,0,0]],
    "Z": [[9,9,9,9,0],[0,0,9,0,0],[0,9,0,0,0],[9,0,0,0,0],[9,9,9,9,0]],
    "[": [[0,9,9,9,0],[0,9,0,0,0],[0,9,0,0,0],[0,9,0,0,0],[0,9,9,9,0]],
    "\\": [[9,0,0,0,0],[0,9,0,0,0],[0,0,9,0,0],[0,0,0,9,0],[0,0,0,0,9]],
    "]": [[0,9,9,9,0],[0,0,0,9,0],[0,0,0,9,0],[0,0,0,9,0],[0,9,9,9,0]],
    "^": [[0,0,9,0,0],[0,9,0,9,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
    "_": [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[9,9,9,9,9]],
    "`": [[0,9,0,0,0],[0,0,9,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
    "a": [[0,0,0,0,0],[0,9,9,9,0],[9,0,0,9,0],[9,0,0,9,0],[0,9,9,9,9]],
    "b": [[9,0,0,0,0],[9,0,0,0,0],[9,9,9,0,0],[9,0,0,9,0],[9,9,9,0,0]],
    "c": [[0,0,0,0,0],[0,9,9,9,0],[9,0,0,0,0],[9,0,0,0,0],[0,9,9,9,0]],
    "d": [[0,0,0,9,0],[0,0,0,9,0],[0,9,9,9,0],[9,0,0,9,0],[0,9,9,9,0]],
    "e": [[0,9,9,0,0],[9,0,0,9,0],[9,9,9,0,0],[9,0,0,0,0],[0,9,9,9,0]],
    "f": [[0,0,9,9,0],[0,9,0,0,0],[9,9,9,0,0],[0,9,0,0,0],[0,9,0,0,0]],
    "g": [[0,9,9,9,0],[9,0,0,9,0],[0,9,9,9,0],[0,0,0,9,0],[0,9,9,0,0]],
    "h": [[9,0,0,0,0],[9,0,0,0,0],[9,9,9,0,0],[9,0,0,9,0],[9,0,0,9,0]],
    "i": [[0,9,0,0,0],[0,0,0,0,0],[0,9,0,0,0],[0,9,0,0,0],[0,9,0,0,0]],
    "j": [[0,0,0,9,0],[0,0,0,0,0],[0,0,0,9,0],[0,0,0,9,0],[0,9,9,0,0]],
    "k": [[9,0,0,0,0],[9,0,9,0,0],[9,9,0,0,0],[9,0,9,0,0],[9,0,0,9,0]],
    "l": [[0,9,0,0,0],[0,9,0,0,0],[0,9,0,0,0],[0,9,0,0,0],[0,0,9,9,0]],
    "m": [[0,0,0,0,0],[9,9,0,9,9],[9,0,9,0,9],[9,0,0,0,9],[9,0,0,0,9]],
    "n": [[0,0,0,0,0],[9,9,9,0,0],[9,0,0,9,0],[9,0,0,9,0],[9,0,0,9,0]],
    "o": [[0,0,0,0,0],[0,9,9,0,0],[9,0,0,9,0],[9,0,0,9,0],[0,9,9,0,0]],
    "p": [[0,0,0,0,0],[9,9,9,0,0],[9,0,0,9,0],[9,9,9,0,0],[9,0,0,0,0]],
    "q": [[0,0,0,0,0],[0,9,9,9,0],[9,0,0,9,0],[0,9,9,9,0],[0,0,0,9,0]],
    "r": [[0,0,0,0,0],[0,9,9,9,0],[9,0,0,0,0],[9,0,0,0,0],[9,0,0,0,0]],
    "s": [[0,0,0,0,0],[0,0,9,9,0],[0,9,0,0,0],[0,0,9,0,0],[9,9,0,0,0]],
    "t": [[0,9,0,0,0],[0,9,0,0,0],[0,9,9,9,0],[0,9,0,0,0],[0,0,9,9,9]],
    "u": [[0,0,0,0,0],[9,0,0,9,0],[9,0,0,9,0],[9,0,0,9,0],[0,9,9,9,9]],
    "v": [[0,0,0,0,0],[9,0,0,0,9],[9,0,0,0,9],[0,9,0,9,0],[0,0,9,0,0]],
    "w": [[0,0,0,0,0],[9,0,0,0,9],[9,0,0,0,9],[9,0,9,0,9],[9,9,0,9,9]],
    "x": [[0,0,0,0,0],[9,0,0,9,0],[0,9,9,0,0],[0,9,9,0,0],[9,0,0,9,0]],
    "y": [[0,0,0,0,0],[9,0,0,0,9],[0,9,0,9,0],[0,0,9,0,0],[9,9,0,0,0]],
    "z": [[0,0,0,0,0],[9,9,9,9,0],[0,0,9,0,0],[0,9,0,0,0],[9,9,9,9,0]],
    "{": [[0,0,9,9,0],[0,0,9,0,0],[0,9,9,0,0],[0,0,9,0,0],[0,0,9,9,0]],
    "|": [[0,9,0,0,0],[0,9,0,0,0],[0,9,0,0,0],[0,9,0,0,0],[0,9,0,0,0]],
    "}": [[9,9,0,0,0],[0,9,0,0,0],[0,9,9,0,0],[0,9,0,0,0],[9,9,0,0,0]],
    "~": [[0,0,0,0,0],[0,0,0,0,0],[0,9,9,0,0],[0,0,0,9,9],[0,0,0,0,0]]
}

# exception lookup dict
_exceptions_lookup_dict = {
    "BaseException": BaseException,
    "SystemExit": SystemExit,
    "KeyboardInterrupt": KeyboardInterrupt,
    "GeneratorExit": GeneratorExit,
    "Exception": Exception,
    "StopIteration": StopIteration,
    "StopAsyncIteration": StopAsyncIteration,
    "ArithmeticError": ArithmeticError,
    "FloatingPointError": FloatingPointError,
    "OverflowError": OverflowError,
    "ZeroDivisionError": ZeroDivisionError,
    "AssertionError": AssertionError,
    "AttributeError": AttributeError,
    "BufferError": BufferError,
    "EOFError": EOFError,
    "ImportError": ImportError,
    "LookupError": LookupError,
    "IndexError": IndexError,
    "KeyError": KeyError,
    "MemoryError": MemoryError,
    "NameError": NameError,
    "UnboundLocalError": UnboundLocalError,
    "OSError": OSError,
    "BlockingIOError": BlockingIOError,
    "ChildProcessError": ChildProcessError,
    "ConnectionError": ConnectionError,
    "BrokenPipeError": BrokenPipeError,
    "ConnectionAbortedError": ConnectionAbortedError,
    "ConnectionRefusedError": ConnectionRefusedError,
    "ConnectionResetError": ConnectionResetError,
    "FileExistsError": FileExistsError,
    "FileNotFoundError": FileNotFoundError,
    "InterruptedError": InterruptedError,
    "IsADirectoryError": IsADirectoryError,
    "NotADirectoryError": NotADirectoryError,
    "PermissionError": PermissionError,
    "ProcessLookupError": ProcessLookupError,
    "TimeoutError": TimeoutError,
    "ReferenceError": ReferenceError,
    "RuntimeError": RuntimeError,
    "NotImplementedError": NotImplementedError,
    "RecursionError": RecursionError,
    "SyntaxError": SyntaxError,
    "IndentationError": IndentationError,
    "TabError": TabError,
    "SystemError": SystemError,
    "TypeError": TypeError,
    "ValueError": ValueError,
    "UnicodeError": UnicodeError,
    "UnicodeDecodeError": UnicodeDecodeError,
    "UnicodeEncodeError": UnicodeEncodeError,
    "UnicodeTranslateError": UnicodeTranslateError,
    "Warning": Warning,
    "DeprecationWarning": DeprecationWarning,
    "PendingDeprecationWarning": PendingDeprecationWarning,
    "RuntimeWarning": RuntimeWarning,
    "SyntaxWarning": SyntaxWarning,
    "UserWarning": UserWarning,
    "FutureWarning": FutureWarning,
    "ImportWarning": ImportWarning,
    "UnicodeWarning": UnicodeWarning,
    "BytesWarning": BytesWarning,
    "ResourceWarning": ResourceWarning
}

# classes
class _microbit_connection:
    """
    Class which handles the sending and receiving of data to and from the
    micro:bit over the serial connection.
    """
    conn = None

    def __init__(self, port=None):
        """
        Constructor. Attempts to find the micro:bit, and raises an Exception
        if one can't be found.
        """
        if port is None or not isinstance(port, str):
            port = self.guess_port()
            if port is None:
                raise Exception("Could not find micro:bit!")

        self.conn = serial.Serial(port, 115200, timeout=1)
        self.write("")
        self.post_reset()

    def handle_potential_invalid_data(self, data):
        # look for the word "Traceback" to see if an exception was caught
        if data[:9] == "Traceback":
            lines = data.replace("\r", "").split("\n")
            # look for the exception raised
            name = lines[-1].split(" ")[0][:-1]
            msg = lines[-1][len(name)+2:]
            if name in _exceptions_lookup_dict:
                raise _exceptions_lookup_dict[name](msg)
            raise Exception("\n\n    the micro:bit threw the following exception:\n    [%s: %s]\n" % (name, msg))

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
        debug("Sending : " + str(data + "\r"))
        self.conn.write(str(data + "\r").encode())

    def readlines(self, strip=True, decode=True):
        """
        Continuously reads data from the serial connection until a ">>>" is
        encountered.
        """
        debug("Received : " + str(self.conn.readline()))
        data = self.conn.read_until(b">>> ")
        try:
            dataStr = data.decode()
            debug("Received : " + str(dataStr))
            if decode:
                if strip:
                    dataStr = dataStr.replace(">>> ", "").strip()
                    self.handle_potential_invalid_data(dataStr)
                return dataStr
            return data
        except UnicodeDecodeError:
            # Random data received, try again to read.
            self.readlines(strip, decode)

    def execute(self, command, strip=True, decode=True, timeout=1):
        """
        Executes the specified command, and returns the result. `strip`
        specifies whether to strip the whole of the output, or just the
        carriage return at the very end.
        """
        self.conn.timeout = timeout
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

class _microbit_image_class:
    """
    Class representing the microbit.Image class. Currently incomplete.

    >>> str(microbit.Image.SNAKE)
    "Image(\n    '99000:'\n    '99099:'\n    '09090:'\n    '09990:'\n    '00000:'\n)"
    >>> repr(microbit.Image.SNAKE)
    "Image('99000:99099:09090:09990:00000:')"

    """
    _img_array_buffer = None
    _img_width = None
    _img_height = None
    _is_string = False
    _is_readonly = False

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        data = self._img_array_buffer
        s = ""
        for row in data:
            s += "%d%d%d%d%d:" % (row[0], row[1], row[2], row[3], row[4])
        return "Image('%s')" % (s)

    def __init__(self, string=None, width=None, height=None, buffer=None,
                 _microrepl_isreadonly=False):
        if string is not None:
            self._is_string = True
            if isinstance(string, _microbit_image_class):
                self._img_array_buffer = string._img_array_buffer
            else:
                if len(string) > 1:
                    self._img_from_string(string.replace("\n", ":").replace(" ", "0"))
                else:
                    if len(string) <= 0:
                        raise Exception("No data provided for image!")
                    c = string[0]
                    if not c in _microbit_font_pendolino3:
                        raise Exception("Unsupported character")
                    self._img_array_buffer = _microbit_font_pendolino3[c]
                    self._img_width = 5
                    self._img_height = 5
        else:
            self._img_width = width
            self._img_height = height
            if buffer is not None:
                l = len(buffer)
                if l != width * height:
                    raise Exception("Invalid data provided for image (either too much or too little)")
                image_data = []
                for i in range(height):
                    row_data = buffer[width * i : width * (i + 1) - 1]
                    image_data.append(row_data)
                self._img_array_buffer = image_data
            else:
                self._img_array_buffer = _microbit_font_pendolino3[0]
        _is_readonly = _microrepl_isreadonly

    def _img_from_string(self, string):
        rows = string.split(":")
        if len(rows) <= 0:
            raise Exception("No data provided for image!")
        l = len(rows[0])
        image_data = []
        for row in rows:
            row_data = []
            if len(row) != l:
                raise Exception("Invalid image: not all the rows are the same length!")
            for char in row:
                c = ord(char)
                if c < ord("0") or c > ord("9"):
                    raise Exception("Invalid image: only the characters 0-9 are allowed")
                row_data.append(c)
            image_data.append(row_data)
        self._img_array_buffer = image_data
        self._img_height = len(rows)
        self._img_width = l

    def _is_out_of_bounds(self, x, y):
        if x + y * (self._img_height - 1) > self._img_width * self._img_height - 1 or \
            y < 0 or y > self._img_height - 1 or \
            x < 0 or x > self._img_width - 1:
            return True
        return False

    def width(self):
        return self._img_width

    def height(self):
        return self._img_height

    def set_pixel(self, x, y, value):
        if self._is_readonly:
            raise Exception("You cannot modify read-only images!")
        if self._is_out_of_bounds(x, y):
            raise Exception("Specified index is out of bounds!")
        if value < 0 or value > 9:
            raise Exception("Invalid pixel brightness value")
        self._img_array_buffer[y][x] = value
        return None

    def get_pixel(self, x, y):
        if self._is_out_of_bounds(x, y):
            raise Exception("Specified index is out of bounds!")
        return self._img_array_buffer[x + y * self._img_height]

    def shift_left(self, n):
        for _ in range(n):
            buf = self._img_array_buffer
            column0 = []
            for i in range(self._img_width):
                column0.append(buf[i][0])
            for y in range(self._img_height):
                for x in range(self._img_width - 1):
                    buf[y][x] = buf[y][x + 1]
            for i in range(self._img_width):
                buf[i][self._img_width - 1] = column0[i]
            self._img_array_buffer = buf
        return None

    def shift_right(self, n):
        for _ in range(n):
            buf = self._img_array_buffer
            column4 = []
            for i in range(self._img_width - 1, 0):
                column4.append(buf[i][self._img_width - 1])
            for y in range(self._img_height):
                for x in range(self._img_width - 1, 0):
                    buf[y][x] = buf[y][x - 1]
            for i in range(self._img_width):
                buf[i][0] = column4[i]
            self._img_array_buffer = buf
        return None

    def shift_up(self, n):
        for _ in range(n):
            buf = self._img_array_buffer
            row = buf[0]
            for y in range(self._img_height - 1):
                buf[y] = buf[y + 1]
            self._img_array_buffer = buf
        return None

    def shift_down(self, n):
        for _ in range(n):
            buf = self._img_array_buffer
            row = buf[0]
            for y in range(self._img_height - 1, 0):
                buf[y] = buf[y - 1]
            self._img_array_buffer = buf
        return None

class _microbit_display:
    """
    Class which represents the microbit.display module.
    """
    _ubit_conn = None

    def __init__(self, conn):
        self._ubit_conn = conn

    def _unimplemented(self):
        raise Exception("Unimplemented function")

    def get_pixel(self, x, y):
        s = self._ubit_conn.execute("microbit.display.get_pixel(%d,%d)" % (x, y))
        try:
            return int(s)
        except:
            return None

    def set_pixel(self, x, y, value):
        self._ubit_conn.execute("microbit.display.set_pixel(%d,%d,%d)" % (x, y, value))
        return None

    def clear(self):
        self._ubit_conn.execute("microbit.display.clear()")
        return None

    #def show(self, image):
    #    self._ubit_conn.execute("microbit.display.show(")
    #    self._unimplemented()

    def show(self, iterable, delay=1000, *, wait=True, loop=False, clear=False):
        if isinstance(iterable, _microbit_image_class):
            self._ubit_conn.execute("microbit.display.show(microbit.%s)" % \
                (repr(iterable)), timeout=1)
        elif isinstance(iterable, str):
            self._ubit_conn.execute( "microbit.display.show(\"%s\",%d,wait=%s,loop=%s,clear=%s)" % \
                (iterable, delay, wait, loop, clear))
        else:
            raise Exception("Invalid datatype being requested to be shown, only type Image or String (str) allowed!")

    def scroll(self, string, delay=400):
        self._ubit_conn.execute("microbit.display.scroll(\"%s\",%d)" % (string, delay), timeout=None)
        return None

class _microbit_uart:
    """
    Class representing the microbit.uart module. Everything is unimplemented,
    and attempting to call any of the functions contained will result in an
    Exception being thrown. This is because the serial connection over USB
    (which is what this module uses to send and receive data from the
    micro:bit) will be cut and used instead for the newly created connection,
    as there is only one hardware serial chip which cannot be shared.
    """
    def _unimplemented(self):
        raise Exception("The microbit.uart module is not implemented, as it will render this module useless")

    def init(self, baudrate=9600, bits=8, parity=None, stop=1, tx=None, rx=None):
        self._unimplemented()

    def any(self):
        self._unimplemented()

    def read(self, nbytes=None):
        self._unimplemented()

    def readall(self, ):
        self._unimplemented()

    def readinto(self, buf, nbytes=None):
        self._unimplemented()

    def readline(self):
        self._unimplemented()

    def write(self, buf):
        self._unimplemented()

class _microbit_spi:
    """
    Class representing the microbit.api module. The function
    `write_readinto(outbuf, inbuf)` is currently not implemented.
    """
    _ubit_conn = None
    _default_sclk = None
    _default_mosi = None
    _default_miso = None

    def __init__(self, conn, default_sclk, default_mosi, default_miso):
        self._ubit_conn = conn
        self._default_sclk = default_sclk
        self._default_mosi = default_mosi
        self._default_miso = default_miso

    def _unimplemented(self):
        raise Exception("Unimplemented function")

    def init(self, baudrate=1000000, bits=8, mode=0, sclk=None, mosi=None, miso=None):
        if sclk is None:
            sclk = self._default_sclk
        if mosi is None:
            mosi = self._default_mosi
        if miso is None:
            miso = self._default_miso

        if not isinstance(sclk, _microbit_pin) or not isinstance(mosi, _microbit_pin) or \
            not isinstance(miso, _microbit_pin):
            raise Exception("sclk must be an instance of one of:\n    microbit.MicroBitDigitalPin\n    microbit.MicroBitAnalogDigitalPin\n    microbit.MicroBitTouchPin")

        self._ubit_conn.execute("microbit.spi.init(baudrate=%d,bits=%d,mode=%d,sclk=%s,mosi=%s,miso=%s)" % \
                                  (baudrate, bits, mode, \
                                  "microbit.%s" % (sclk._pin_name), \
                                  "microbit.%s" % (mosi._pin_name), \
                                  "microbit.%s" % (miso._pin_name)))
        return None

    def read(self, nbytes):
        data = self._ubit_conn.execute("microbit.spi.read(%d)" % (nbytes),
                                         decode=False)
        return data[2:-1] # make sure to remove the

    def write(self, buffer):
        if not isinstance(buffer, bytes):
            #buffer = str(buffer)[2:-1] # TODO check this logic
            raise Exception("Expected bytes, not %s!" % (type(buffer)))
        self._ubit_conn.execute("microbit.spi.write(b\"%s\")" % (buffer))
        return None

    def write_readinto(self, outbuf, inbuf):
        if not isinstance(out, str):
            out = str(out)[2:-1]
        self._unimplemented()

class _microbit_i2c:
    """
    Class representing the microbit.i2c module.
    """
    _ubit_conn = None

    def __init__(self, conn):
        self._ubit_conn = conn

    def read(self, addr, n, repeat=False):
        data = self._ubit_conn.execute("microbit.i2c.read(%x,%d,repeat=%s)" % \
                                         (addr, n, repeat), decode=False)
        return data[2:-1]

    def write(addr, buf, repeat=False):
        if not isinstance(buffer, bytes):
            #buffer = str(buffer)[2:-1] # TODO check this logic
            raise Exception("Expected bytes, not %s!" % (type(buffer)))
        self._ubit_conn.execute("microbit.i2c.write(%x,b\"%s\",repeat=%s)" % \
                                  (addr, buf, repeat))
        return None

class _microbit_accelerometer:
    """
    Class representing the microbit.accelerometer module.
    """
    _ubit_conn = None

    def __init__(self, conn):
        self._ubit_conn = conn

    def get_x(self):
        s = self._ubit_conn.execute("microbit.accelerometer.get_x()")
        try:
            return int(s)
        except:
            return None

    def get_y(self):
        s = self._ubit_conn.execute("microbit.accelerometer.get_y()")
        try:
            return int(s)
        except:
            return None

    def get_z(self):
        s = self._ubit_conn.execute("microbit.accelerometer.get_z()")
        try:
            return int(s)
        except:
            return None

    def get_values(self):
        return (self.get_x(), self.get_y(), self.get_z())

    def current_gesture(self):
        s = self._ubit_conn.execute("microbit.accelerometer.get_z()")
        return s

    def is_gesture(self, name):
        s = self._ubit_conn.execute("microbit.accelerometer.is_gesture(%s)" % \
                                      (name))
        if s == "True":
            return True
        elif s == "False":
            return False
        else:
            return None

    def was_gesture(self, name):
        s = self._ubit_conn.execute("microbit.accelerometer.was_gesture(%s)" % \
                                      (name))
        if s == "True":
            return True
        elif s == "False":
            return False
        else:
            return None

    def get_gestures(self):
        s = self._ubit_conn.execute("microbit.accelerometer.get_gestures()") \
                .replace(" ", "")[1:-1]
        result = ()
        for i in s.split(","):
            result = result + (i,)
        return result

class _microbit_compass:
    """
    Class representing the microbit.compass module.
    """
    _ubit_conn = None

    def __init__(self, conn):
        self._ubit_conn = conn

    def calibrate(self):
        self._ubit_conn.execute("microbit.compass.calibrate()", timeout=None)
        return None

    def is_calibrated(self):
        s = self._ubit_conn.execute("microbit.compass.is_calibrated()")
        if s == "True":
            return True
        elif s == "False":
            return False
        else:
            return None

    def clear_calibration(self):
        self._ubit_conn.execute("microbit.compass.clear_calibration()")
        return None

    def get_x(self):
        s = self._ubit_conn.execute("microbit.compass.get_x()", timeout=None)
        try:
            return int(s)
        except:
            return None

    def get_y(self):
        s = self._ubit_conn.execute("microbit.compass.get_y()", timeout=None)
        try:
            return int(s)
        except:
            return None

    def get_z(self):
        s = self._ubit_conn.execute("microbit.compass.get_z()", timeout=None)
        try:
            return int(s)
        except:
            return None

    def heading(self):
        s = self._ubit_conn.execute("microbit.compass.heading()", timeout=None)
        try:
            return int(s)
        except:
            return None

    def get_field_strength(self):
        s = self._ubit_conn.execute("microbit.compass.get_field_strength()", timeout=None)
        try:
            return int(s)
        except:
            return None

class _microbit_pin:
    """
    This class facilitates isinstance-ing of the other pin classes, and also
    provides the _pin_name member. It serves no other real purpose.
    """
    _pin_name = None

class _microbit:
    """
    Main class, which represents the microibt module. Everything goes in here.
    """
    _ubit_conn = None

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

    # microbit module classes
    class Image(_microbit_image_class):
        # constants (these are all readonly images)
        HEART           = _microbit_image_class("01010:11111:11111:01110:00100", _microrepl_isreadonly=True)
        HEART_SMALL     = _microbit_image_class("00000:01010:01110:00100:00000", _microrepl_isreadonly=True)
        HAPPY           = _microbit_image_class("00000:01010:00000:10001:01110", _microrepl_isreadonly=True)
        SMILE           = _microbit_image_class("00000:00000:00000:10001:01110", _microrepl_isreadonly=True)
        SAD             = _microbit_image_class("00000:01010:00000:01110:10001", _microrepl_isreadonly=True)
        CONFUSED        = _microbit_image_class("00000:01010:00000:01010:10101", _microrepl_isreadonly=True)
        ANGRY           = _microbit_image_class("10001:01010:00000:11111:10101", _microrepl_isreadonly=True)
        ASLEEP          = _microbit_image_class("00000:11011:00000:01110:00000", _microrepl_isreadonly=True)
        SURPRISED       = _microbit_image_class("01010:00000:00100:01010:00100", _microrepl_isreadonly=True)
        SILLY           = _microbit_image_class("10001:00000:11111:00101:00111", _microrepl_isreadonly=True)
        FABULOUS        = _microbit_image_class("11111:11011:00000:01010:01110", _microrepl_isreadonly=True)
        MEH             = _microbit_image_class("01010:00000:00010:00100:01000", _microrepl_isreadonly=True)
        YES             = _microbit_image_class("00000:00001:00010:10100:01000", _microrepl_isreadonly=True)
        NO              = _microbit_image_class("10001:01010:00100:01010:10001", _microrepl_isreadonly=True)
        CLOCK12         = _microbit_image_class("00100:00100:00100:00000:00000", _microrepl_isreadonly=True)
        CLOCK1          = _microbit_image_class("00010:00010:00100:00000:00000", _microrepl_isreadonly=True)
        CLOCK2          = _microbit_image_class("00000:00011:00100:00000:00000", _microrepl_isreadonly=True)
        CLOCK3          = _microbit_image_class("00000:00000:00111:00000:00000", _microrepl_isreadonly=True)
        CLOCK4          = _microbit_image_class("00000:00000:00100:00011:00000", _microrepl_isreadonly=True)
        CLOCK5          = _microbit_image_class("00000:00000:00100:00010:00010", _microrepl_isreadonly=True)
        CLOCK6          = _microbit_image_class("00000:00000:00100:00100:00100", _microrepl_isreadonly=True)
        CLOCK7          = _microbit_image_class("00000:00000:00100:01000:01000", _microrepl_isreadonly=True)
        CLOCK8          = _microbit_image_class("00000:00000:00100:11000:00000", _microrepl_isreadonly=True)
        CLOCK9          = _microbit_image_class("00000:00000:11100:00000:00000", _microrepl_isreadonly=True)
        CLOCK10         = _microbit_image_class("00000:11000:00100:00000:00000", _microrepl_isreadonly=True)
        CLOCK11         = _microbit_image_class("01000:01000:00100:00000:00000", _microrepl_isreadonly=True)
        ARROW_N         = _microbit_image_class("00100:01110:10101:00100:00100", _microrepl_isreadonly=True)
        ARROW_NE        = _microbit_image_class("00111:00011:00101:01000:10000", _microrepl_isreadonly=True)
        ARROW_E         = _microbit_image_class("00100:00010:11111:00010:00100", _microrepl_isreadonly=True)
        ARROW_SE        = _microbit_image_class("10000:01000:00101:00011:00111", _microrepl_isreadonly=True)
        ARROW_S         = _microbit_image_class("00100:00100:10101:01110:00100", _microrepl_isreadonly=True)
        ARROW_SW        = _microbit_image_class("00001:00010:10100:11000:11100", _microrepl_isreadonly=True)
        ARROW_W         = _microbit_image_class("00100:01000:11111:01000:00100", _microrepl_isreadonly=True)
        ARROW_NW        = _microbit_image_class("11100:11000:10100:00010:00001", _microrepl_isreadonly=True)
        TRIANGLE        = _microbit_image_class("00000:00100:01010:11111:00000", _microrepl_isreadonly=True)
        TRIANGLE_LEFT   = _microbit_image_class("10000:11000:10100:10010:11111", _microrepl_isreadonly=True)
        CHESSBOARD      = _microbit_image_class("01010:10101:01010:10101:01010", _microrepl_isreadonly=True)
        DIAMOND         = _microbit_image_class("00100:01010:10001:01010:00100", _microrepl_isreadonly=True)
        DIAMOND_SMALL   = _microbit_image_class("00000:00100:01010:00100:00000", _microrepl_isreadonly=True)
        SQUARE          = _microbit_image_class("11111:10001:10001:10001:11111", _microrepl_isreadonly=True)
        SQUARE_SMALL    = _microbit_image_class("00000:01110:01010:01110:00000", _microrepl_isreadonly=True)
        RABBIT          = _microbit_image_class("10100:10100:11110:11010:11110", _microrepl_isreadonly=True)
        COW             = _microbit_image_class("10001:10001:11111:01110:00100", _microrepl_isreadonly=True)
        MUSIC_CROTCHET  = _microbit_image_class("00100:00100:00100:11100:11100", _microrepl_isreadonly=True)
        MUSIC_QUAVER    = _microbit_image_class("00100:00110:00101:11100:11100", _microrepl_isreadonly=True)
        MUSIC_QUAVERS   = _microbit_image_class("01111:01001:01001:11011:11011", _microrepl_isreadonly=True)
        PITCHFORK       = _microbit_image_class("10101:10101:11111:00100:00100", _microrepl_isreadonly=True)
        XMAS            = _microbit_image_class("00100:01110:00100:01110:11111", _microrepl_isreadonly=True)
        PACMAN          = _microbit_image_class("01111:11010:11100:11110:01111", _microrepl_isreadonly=True)
        TARGET          = _microbit_image_class("00100:01110:11011:01110:00100", _microrepl_isreadonly=True)
        TSHIRT          = _microbit_image_class("11011:11111:01110:01110:01110", _microrepl_isreadonly=True)
        ROLLERSKATE     = _microbit_image_class("00011:00011:11111:11111:01010", _microrepl_isreadonly=True)
        DUCK            = _microbit_image_class("01100:11100:01111:01110:00000", _microrepl_isreadonly=True)
        HOUSE           = _microbit_image_class("00100:01110:11111:01110:01010", _microrepl_isreadonly=True)
        TORTOISE        = _microbit_image_class("00000:01110:11111:01010:00000", _microrepl_isreadonly=True)
        BUTTERFLY       = _microbit_image_class("11011:11111:00100:11111:11011", _microrepl_isreadonly=True)
        STICKFIGURE     = _microbit_image_class("00100:11111:00100:01010:10001", _microrepl_isreadonly=True)
        GHOST           = _microbit_image_class("11111:10101:11111:11111:10101", _microrepl_isreadonly=True)
        SWORD           = _microbit_image_class("00100:00100:00100:01110:00100", _microrepl_isreadonly=True)
        GIRAFFE         = _microbit_image_class("11000:01000:01000:01110:01010", _microrepl_isreadonly=True)
        SKULL           = _microbit_image_class("01110:10101:11111:01110:01110", _microrepl_isreadonly=True)
        UMBRELLA        = _microbit_image_class("01110:11111:00100:10100:01100", _microrepl_isreadonly=True)
        SNAKE           = _microbit_image_class("11000:11011:01010:01110:00000", _microrepl_isreadonly=True)

    class Button:
        """
        Class representing one of the micro:bit's buttons (microbit.button_a and
        microbit.button_b).
        """
        _ubit_conn = None
        _button_name = None

        def __init__(self, conn, name):
            self._ubit_conn = conn
            self._button_name = name

        def __str__(self):
            return

        def is_pressed(self):
            s = self._ubit_conn.execute("microbit.%s.is_pressed()" % (self._button_name))
            if s == "True":
                return True
            elif s == "False":
                return False
            else:
                return None

        def was_pressed(self):
            s = self._ubit_conn.execute("microbit.%s.was_pressed()" % (self._button_name))
            if s == "True":
                return True
            elif s == "False":
                return False
            else:
                return None

        def get_presses(self):
            s = self._ubit_conn.execute("microbit.%s.get_presses()" % (self._button_name))
            try:
                return int(s)
            except:
                return None

    class MicroBitDigitalPin(_microbit_pin):
        """
        Class representing a digital pin on the micro:bit (pins 5-9, 11-16, 19
        and 20).
        """
        _ubit_conn = None

        def __init__(self, conn, name):
            self._ubit_conn = conn
            self._pin_name = name

        def read_digital(self):
            s = self._ubit_conn.execute("microbit.%s.read_digital()" % (self._pin_name))
            try:
                return int(s)
            except:
                return None

        def write_digital(self, value):
            self._ubit_conn.execute("microbit.%s.write_digital(%d)" % (self._pin_name, value))
            return None

    class MicroBitAnalogDigitalPin(_microbit_pin):
        """
        Class representing an analog pin on the micro:bit (pins 3, 4 and 10).
        """
        _ubit_conn = None

        def __init__(self, conn, name):
            self._ubit_conn = conn
            self._pin_name = name

        def read_analog(self):
            s = self._ubit_conn.execute("microbit.%s.read_analog()" % (self._pin_name))
            try:
                return int(s)
            except:
                return None

        def write_analog(self, value):
            self._ubit_conn.execute("microbit.%s.write_analog(%d)" % (self._pin_name, value))
            return None

        def set_analog_period(self, period):
            self._ubit_conn.execute("microbit.%s.set_analog_period(%d)" % (self._pin_name, period))
            return None

        def set_analog_period_microseconds(self, period):
            self._ubit_conn.execute("microbit.%s.set_analog_period_microseconds(%d)" % (self._pin_name, period))
            return None

    class MicroBitTouchPin(_microbit_pin):
        """
        Class representing one of the three large pins on the micro:bit's pin
        array (called touch pins).
        """
        _ubit_conn = None

        def __init__(self, conn, name):
            self._ubit_conn = conn
            self._pin_name = name

        def is_touched(self):
            s = self._ubit_conn.execute("microbit.%s.is_touched()" % (self._pin_name))
            if s == "True":
                return True
            elif s == "False":
                return False
            else:
                return None

    # functions
    # constructor
    def __init__(self, port_addr=None):
        self._ubit_conn = _microbit_connection(port_addr)

        self.button_a = self.Button(self._ubit_conn, "button_a")
        self.button_b = self.Button(self._ubit_conn, "button_b")

        self.pin0 = self.MicroBitTouchPin(self._ubit_conn, "pin0")
        self.pin1 = self.MicroBitTouchPin(self._ubit_conn, "pin1")
        self.pin2 = self.MicroBitTouchPin(self._ubit_conn, "pin2")
        self.pin3 = self.MicroBitAnalogDigitalPin(self._ubit_conn, "pin3")
        self.pin4 = self.MicroBitAnalogDigitalPin(self._ubit_conn, "pin4")
        self.pin5 = self.MicroBitDigitalPin(self._ubit_conn, "pin5")
        self.pin6 = self.MicroBitDigitalPin(self._ubit_conn, "pin6")
        self.pin7 = self.MicroBitDigitalPin(self._ubit_conn, "pin7")
        self.pin8 = self.MicroBitDigitalPin(self._ubit_conn, "pin8")
        self.pin9 = self.MicroBitDigitalPin(self._ubit_conn, "pin9")
        self.pin10 = self.MicroBitAnalogDigitalPin(self._ubit_conn, "pin10")
        self.pin11 = self.MicroBitDigitalPin(self._ubit_conn, "pin11")
        self.pin12 = self.MicroBitDigitalPin(self._ubit_conn, "pin12")
        self.pin13 = self.MicroBitDigitalPin(self._ubit_conn, "pin13")
        self.pin14 = self.MicroBitDigitalPin(self._ubit_conn, "pin14")
        self.pin15 = self.MicroBitDigitalPin(self._ubit_conn, "pin15")
        self.pin16 = self.MicroBitDigitalPin(self._ubit_conn, "pin16")
        self.pin19 = self.MicroBitDigitalPin(self._ubit_conn, "pin19")
        self.pin20 = self.MicroBitDigitalPin(self._ubit_conn, "pin20")

        self.display = _microbit_display(self._ubit_conn)

        self.uart = _microbit_uart()

        self.spi = _microbit_spi(self._ubit_conn, self.pin13,
                                        self.pin15, self.pin14)

        self.i2c = _microbit_i2c(self._ubit_conn)

        self.accelerometer = _microbit_accelerometer(self._ubit_conn)
        self.compass = _microbit_compass(self._ubit_conn)

        self.reset()

    def panic(self, n):
        self._ubit_conn.execute("microbit.panic(%d)" % (n))
        self._ubit_conn.post_reset()
        return None

    def reset(self):
        self._ubit_conn.execute("microbit.reset()")
        self._ubit_conn.post_reset()
        return None

    def sleep(self, n):
        # NOTE: this could use time.sleep instead
        self._ubit_conn.execute("microbit.sleep(%d)" % (n), timeout=(n /1000) + 0.5)
        return None

    def running_time(self):
        s = self._ubit_conn.execute("microbit.running_time()")
        try:
            return int(s)
        except:
            return None

    def temperature(self):
        s = self._ubit_conn.execute("microbit.temperature()")
        try:
            return int(s)
        except:
            return None

Microbit = _microbit
