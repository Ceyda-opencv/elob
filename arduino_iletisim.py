import serial
import pyfirmata


def ac(x):
    d.write(b'1')


def kapat(y):
    d.write(b'0')


d = serial.Serial("COM5", 9600, timeout=1)

while True:
    z = 0
    def ileri():
        while 1 == y:
            ac(1)

            z = z+1
            if z == 1:
                break

    def geri():
        while 0 == y:
            z = 0
            ac(0)
            z = z+1
            if z ==1:
                break

def birak(y):
    while 1 == y:
        kapat(1)
        break
# import serial
#
# def ac(x):
#     d.write(b'1')
#
#
# def kapat():
#     d.write(b'0')
#
#1

# # d = serial.Serial("/dev/cu.usbmodem14201", 9600, timeout=1)
# d = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
# while 1:
#     x=input("1 veya 0 gir laaayn")
#     if x=="q":
#         break
#     else:
#         ac(x)
