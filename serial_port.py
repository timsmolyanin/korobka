from threading import Thread
import serial


class SerialPort(Thread):
    def __init__(self, comport, baudrate, callback, parent=None):
        super(SerialPort, self).__init__(parent)
        self.serial_port = None
        self.comport = comport
        self.baudrate = baudrate
        self.cb = callback

        print("Created object of Serial Port")
        self.serial_port = serial.Serial(port=self.comport,
                                         baudrate=self.baudrate,
                                         parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE,
                                         bytesize=serial.EIGHTBITS,
                                         timeout=1)

    def serial_read(self):
        if self.serial_port.isOpen():
            response = ""
            while True:
                try:
                    response = self.serial_port.read(100)
                    if response == b'':
                        pass
                    else:
                        self.cb(response)
                        response = ""
                except Exception as exc:
                    print("Exception while serial_read method.", exc)
        else:
            print("Not open")

    def serial_write(self):
        if self.serial_port.isOpen():
            cmd = ""
            try:
                self.serial_port.write(cmd)
            except Exception as exc:
                print("Exception while serial_write method.", exc)
        else:
            print("Not open")

    def run(self):
        while True:
            try:
                self.serial_read()
            except Exception as exc:
                print(exc)
