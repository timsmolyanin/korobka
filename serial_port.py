from threading import Thread
import serial
import struct


class SerialPort(Thread):
    """
    Класс для реализации взаимодействия с Nextion через COM-порт.
    Еще чего-то...
    """
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
        """
        Метод, который осуществляет постоянное чтение COM-порта.
        Происходит проверка открыт ли порт, если да, то читаем данные с порта,
        исключаем пустые строки, которые Nextion шлет каждую секунду,
        исключаем данные без терминатора /r/n, т.к. все валидные данные с Nextion должны его содержать,
        и если все хорошо - выдаем данные в callback функцию для дальнейшей обработки.

        Структура данных принимаемых с Nextion:

        !ВОЗМОЖНЫ ИЗМЕНЕНИЯ!

        aaa.bbb.ccc/r/n
        aaa - [electric, light, temperature, water]
        bbb - совпадает с MQTT топиком, example - OutletGroup1
        ccc - ON/OF, чего-то такое
        :return:

        TODO:
        - если серийный порт закрыт, то чего тогда?
        - если данные без терминатора, то чего тогда?
        -
        """
        response = ""
        if self.serial_port.isOpen():
            while True:
                try:
                    response = self.serial_port.read(100)
                    if response == b'':
                        # Nextion send empty string every second
                        pass
                    else:
                        decode_data = response.decode('Ascii')
                        if str(decode_data[-2:]).encode('Ascii') == b'\r\n':
                            # убираем /r/n в конце строки, получается список [decode_data], поэтому отдаем нулевой id
                            self.cb(decode_data.splitlines()[0])
                        response = ""
                except Exception as exc:
                    print("Exception while serial_read method.", exc)
        else:
            print("Not open")

    def serial_write(self, cmd):
        """
        Метод для записи в COM-порт команд для Nextion

        TODO:
        - структура команд
        - если серийный порт закрыт, то чего тогда?
        - если данные без терминатора, то чего тогда?
        -
        :return:
        """
        eof = struct.pack('B', 0xff)

        if self.serial_port.isOpen():
            # cmd = ""
            try:
                self.serial_port.write(cmd.encode())
                self.serial_port.write(eof)
                self.serial_port.write(eof)
                self.serial_port.write(eof)
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


def _test_cb(data):
    print(data)


def _test_main():
    s = SerialPort("COM3", 115200, _test_cb)
    cmd = 'elec_ctrl.b0.picc=28'
    print(cmd)
    s.serial_write(cmd)


if __name__ == "__main__":
    _test_main()
