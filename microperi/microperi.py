#! /usr/bin/env python3
# Part of MicroPeri https://github.com/JoeGlancy/microperi
#
# See LICENSE file for copyright and license details

# MicroPeri is a library for using the BBC Microbit with MicroPython as an external peripheral device or sensor.

import serial, sys
from serial.tools.list_ports import comports
from ast import literal_eval


def find_microbit():
    """
    From https://github.com/ntoll/microrepl
    Returns the port for the first micro:bit found connected to the computer
    running this script. If no micro:bit is found, returns None.
    """
    ports = comports()
    platform = sys.platform
    if platform.startswith('linux'):
        for port in ports:
            if 'VID:PID=0D28:0204' in port[2].upper():
                return port[0]
    elif platform.startswith('darwin'):
        for port in ports:
            if 'VID:PID=0D28:0204' in port[2]:
                return port[0]
    elif platform.startswith('win'):
        for port in ports:
            if 'VID:PID=0D28:0204' in port[2]:
                return port[0]
    return None


port = find_microbit()


def execute_command_results(ser, command, symbol="("):
    ser.write(command)
    ser.readline()
    while True:
        data = ser.readline().decode()
        if len(data) > 0 and data.rstrip() != "":
            break
        elif data.rstrip() == ">>>":
            continue
    return data.rstrip('\n').rstrip('\r')


def get_values(ser):
    c = b"accelerometer.get_values()\r"
    return literal_eval(execute_command_results(ser, c))


def current_gestures(ser):
    c = b"accelerometer.current_gestures()\r"
    return execute_command_results(ser, c, "'")


def get_presses(ser):
    c = b"button_a.get_presses()\r"
    try:
        return bool(int(execute_command_results(ser, c, "'")))
    except:
        print("Unable to get button presses.")
        return False


def init(ser):
    ser.write(b"\r")
    while True:
        data = ser.readline().decode().rstrip()
        if data == ">>>":
            return


if __name__ == "__main__":
    with serial.Serial(port, 115200, timeout=1) as ser:
        init(ser)
        print(repr(get_values(ser)))
        print(get_presses(ser))
        print(current_gestures(ser))
