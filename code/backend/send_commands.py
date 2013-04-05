#!/usr/bin/python
import os, sys
import serial

arg=" ".join(sys.argv[1:])
ser = serial.Serial("/dev/ttyACM0", 9600)
ser.write(arg+'\n')
print ser.readline()
