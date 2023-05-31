import time
from threading import Thread
import serial
import struct
import mqtt_communication
import yaml
import network_configurator
import os
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
        tmp = data.split("/")
        match tmp[0]:
            case "electric":
                wb_dev = "outletcontrol_34"
                mqtt_ch = tmp[1]
                val = int(tmp[2])
                mqtt_communication.wb_mqtt_switch(wb_dev, mqtt_ch, val)
            case "light":
                wb_dev = "lightcontrol_145"
                mqtt_ch = tmp[1]
                val = int(tmp[2])
                mqtt_communication.wb_mqtt_switch(wb_dev, mqtt_ch, val)
            case "network":
                match tmp[1]:
                    case "wifi":
                        match tmp[2]:
                            case "state":
                                wifi_state = tmp[-1]
                                if wifi_state == "off":
                                    network_configurator.config_wifi_settings()
                                write_to_config_file("wifi", "state", wifi_state)
                            case "ssid":
                                wifi_ssid = tmp[-1]
                                write_to_config_file("wifi", "ssid", wifi_ssid)
                            case "password":
                                wifi_passwd = tmp[-1]
                                write_to_config_file("wifi", "password", wifi_passwd)
                                network_configurator.config_wifi_settings()

                    case "eth0":
                        match tmp[2]:
                            case "mode":
                                eth0_mode = tmp[-1]
                                write_to_config_file("eth0", "mode", eth0_mode)
                            case "ip":
                                eth0_ip = tmp[-1]
                                write_to_config_file("eth0", "ip", eth0_ip)
                            case "mask":
                                eth0_mask = tmp[-1]
                                write_to_config_file("eth0", "mask", eth0_mask)
                                network_configurator.config_eth_settings()
            case "temperature":
                match tmp[1]:
                    case "room1":
                        match tmp[2]:
                            case "setpoint":
                                setpoint = int(tmp[-1])
                                print(setpoint, type(setpoint))
                                dev1 = "0x84fd27fffe6d74bb"
                                dev2 = "0x84fd27fffe0e709f"
                                mqtt_communication.mqtt_set_heating_setpoint(dev1, setpoint)
                                mqtt_communication.mqtt_set_heating_setpoint(dev2, setpoint)

            case "system":
                print(tmp)
                os.system('reboot')


def write_to_config_file(interface: str, param: str, val: str) -> None:
    with open("/root/wk/korobka_app/korobka/config.yaml", "r") as f:
        data = yaml.safe_load(f)
        data["network"][f"{interface}"][f"{param}"] = val
    with open('/root/wk/korobka_app/korobka/config.yaml', 'w') as file:
        yaml.dump(data, file, sort_keys=False)


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
            response = com.readline()
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

    # while True:
    #     serial_read(True, serial_port, test_cb)

    # eof = struct.pack('B', 0xff)
    # cmd = 'electric_ctrl.t0.txt="' + "abcde" + '"'
    # try:
    #     serial_port.write(cmd.encode())
    #     serial_port.write(eof)
    #     serial_port.write(eof)
    #     serial_port.write(eof)
    # except Exception as exc:
    #     print("Exception while serial_write method.", exc)


if __name__ == "__main__":
    _test_main()
