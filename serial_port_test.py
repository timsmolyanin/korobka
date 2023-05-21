import serial
import time
import struct
import threading


def read(sp):
    response = sp.read(100)
    if response == b'':
        # Nextion send empty string every second
        pass
    else:
        decode_data = response.decode('Ascii')
        if str(decode_data[-2:]).encode('Ascii') == b'\r\n':
            # убираем /r/n в конце строки, получается список [decode_data], поэтому отдаем нулевой id
            print(decode_data.splitlines()[0])
            # self.cb(decode_data.splitlines()[0])
            response = ""


def write(sp, cmd):
    eof = struct.pack('B', 0xff)

    try:
        sp.write(cmd.encode())
        sp.write(eof)
        sp.write(eof)
        sp.write(eof)
    except Exception as exc:
        print("Exception while serial_write method.", exc)


def const_writing(sp):
    while True:
        time.sleep(2)
        cmd_off = 'electric_ctrl.b3.picc=53'
        cmd_on = 'electric_ctrl.b3.picc=55'
        write(sp, cmd_off)
        time.sleep(2)
        write(sp, cmd_on)


def const_reading(sp):
    while True:
        read(sp)
        # time.sleep(1)


def test():
    serial_port = serial.Serial(port="COM3", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS,
                                timeout=1)

    t1 = threading.Thread(target=const_writing, args=(serial_port, ))
    t2 = threading.Thread(target=const_reading, args=(serial_port, ))
    t1.start()
    t2.start()


if __name__ == "__main__":
    test()
