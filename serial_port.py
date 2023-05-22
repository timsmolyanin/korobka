import time
from threading import Thread
import serial
import struct
import mqtt_communication
import yaml
from datetime import datetime


class NextionReader(Thread):
    """
    Класс для реализации взаимодействия с Nextion через COM-порт.
    Еще чего-то...
    """
    def __init__(self, comport_status, comport, parent=None):
        super(NextionReader, self).__init__(parent)
        self.comport_status = comport_status
        self.comport = comport

    def run(self) -> None:
        while True:
            serial_read(self.comport_status, self.comport, self.cb)

    def cb(self, data):
        print(data)
        tmp = data.split(".")
        wb_dev = None
        mqtt_ch = None
        val = None
        if tmp[0] == "electric":
            wb_dev = "outletcontrol_34"
            mqtt_ch = tmp[1]
            val = int(tmp[2])
            mqtt_communication.wb_mqtt_switch(wb_dev, mqtt_ch, val)
        elif tmp[0] == "light":
            wb_dev = "lightcontrol_145"
            mqtt_ch = tmp[1]
            val = int(tmp[2])
            mqtt_communication.wb_mqtt_switch(wb_dev, mqtt_ch, val)
        # elif tmp[0] == "network":
            # if tmp[1] == "1":
                # with open("config.yaml", "r") as f:
                #     data = yaml.safe_load(f)
                #     data["general"][f"room{room_number}"]["operation_mode"] = operation_method
                # with open('config.yaml', 'w') as file:
                #     yaml.dump(data, file, sort_keys=False)
            # print(tmp)

        # mqtt_ch = tmp[1]
        # val = int(tmp[2])
        # mqtt_communication.wb_mqtt_switch(wb_dev, mqtt_ch, val)


def serial_connect(com: str, baud: int) -> list:
    """
    Метод создает объект соединения и сразу открывает СОМ-порт
    :return: True/False, в зависимости от того, удалось ли открыть указанный СОМ-порт
    """
    print("Connect to COM-port")
    serial_port_open_flag = False
    serial_port = None
    while not serial_port_open_flag:
        time.sleep(1)
        try:
            serial_port = serial.Serial(port=com,
                                        baudrate=baud,
                                        parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        bytesize=serial.EIGHTBITS,
                                        timeout=1)

            serial_port_open_flag = serial_port.isOpen()
        except serial.serialutil.SerialException as exc:
            # TODO: log error
            print(exc)
            serial_port_open_flag = False

        return [serial_port_open_flag, serial_port]


def serial_read(st, com, cb):
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
    while st:
        if not st:
            break
        response = ""
        try:
            response = com.read(100)
            # print(response)
            if response == b'':
                # Nextion send empty string every second
                pass
            else:
                decode_data = response.decode('Ascii')
                if str(decode_data[-2:]).encode('Ascii') == b'\r\n':
                    # убираем /r/n в конце строки, получается список [decode_data], поэтому отдаем нулевой id
                    cb(decode_data.splitlines()[0])
                    response = ""
        except Exception as exc:
            print("Exception while serial_read method.", exc)
            # st = False
            # serial_connect("COM3", 115200)


def serial_write(sp, cmd):
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
    escape = '\xff'
    try:
        sp.write(cmd.encode())
        sp.write(eof)
        sp.write(eof)
        sp.write(eof)
    except Exception as exc:
        print("Exception while serial_write method.", exc)


def _test_main():
    serial_port = serial.Serial(port="COM3",
                                baudrate=115200,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS,
                                timeout=1)
    eof = struct.pack('B', 0xff)
    cmd = 'electric_ctrl.t0.txt="' + "abcde" + '"'
    try:
        serial_port.write(cmd.encode())
        serial_port.write(eof)
        serial_port.write(eof)
        serial_port.write(eof)
    except Exception as exc:
        print("Exception while serial_write method.", exc)


if __name__ == "__main__":
    _test_main()
