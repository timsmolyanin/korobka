
"""
Настройки ethernet порта:
- DHCP
    - method=auto
- Static IP
    - IP address
    - Mask (slash-format)
    - Gateway IP (if exist)

Настройки Wi-Fi модема:
- Network name (SSID)
- Password

"""

import yaml
import nmcli


class MyException(Exception):
    """
    Надо будет переименовать, возможно в другой файл вынести.
    В общем чего-то с ним сделать... Здесь он быть не должен
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def config_eth_settings() -> None:
    """
    Функция для настройки Ethernet порта (wb-eth0).
    IP адрес интерфейсу можно задать вручную ли через DHCP.
    :return:
    """
    eth0_ip = None
    eth0_mask = None
    eth0_gateway = None
    eth_mode = None
    print("Начато конфигурирование wb-eth0 адаптера")
    print("Открытие файла конфигурации")
    with open("/root/wk/korobka_app/korobka/config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    eth_configs = config["network"]["eth0"]

    eth_mode = eth_configs["mode"]
    if eth_mode == "static":
        print("Выбрана настройка статического IP адреса")
        eth0_ip = eth_configs["ip"]
        eth0_mask = eth_configs["mask"]
        eth0_gateway = eth_configs["gateway"]
        if eth0_gateway == "None":
            print("Выполнить настройку статического IP адреса без шлюза")
            nmcli.connection.modify("wb-eth0", {
                "ipv4.addresses": f"{eth0_ip}/{eth0_mask}",
                "ipv4.method": "manual"
            })
        else:
            print("Выполнить настройку статического IP адреса c шлюзом")
            nmcli.connection.modify("wb-eth0", {
                "ipv4.addresses": f"{eth0_ip}/{eth0_mask}",
                "ipv4.gateway": f"{eth0_gateway}",
                "ipv4.method": "manual"
            })
    elif eth_mode == "dhcp":
        print("Выбрано получение IP адреса от сервера DHCP")
        print("Выполнить получение IP адреса от сервера DHCP")
        nmcli.connection.modify('wb-eth0', {
            "ipv4.method": "auto"
        })

    print("Отрубить wb-eth0")
    nmcli.connection.down("wb-eth0")
    print("Врубить wb-eth0")
    nmcli.connection.up("wb-eth0")


def config_wifi_settings() -> None:
    """
    Функция для конфигурирования Wi-Fi адаптера
    :return:
    """
    wifi_state = None
    wifi_ssid = None
    wifi_password = None
    print("Начато конфигурирование Wi-Fi адаптера")
    print("Открытие файла конфигурации")
    # with open("/root/wk/korobka_app/korobka/config.yaml") as f:
    with open("/root/wk/test/config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    wifi_configs = config["network"]["wifi"]
    wifi_state = wifi_configs["state"]
    if wifi_state == "off":
        print("Выключить Wi-Fi адаптер")
        nmcli.radio.wifi_off()
    elif wifi_state == "on":
        print('Удалить старые wifi подключения')
        delete_wifi_conn()
        print("Включить Wi-Fi адаптер")
        nmcli.radio.wifi_on()
        wifi_ssid = str(wifi_configs["ssid"])
        wifi_password = str(wifi_configs["password"])
        print(wifi_ssid, wifi_password)
        try:
            print(f"Подключение к Wi-Fi сети {wifi_ssid}, пароль {wifi_password}")
            nmcli.device.wifi_connect(ssid=wifi_ssid, password=wifi_password)
        except Exception as exc:
            print(exc)

def delete_wifi_conn() -> None:
    wifi_con_to_del = None
    connections = nmcli.connection()
    for conn in connections:
        if conn.conn_type == 'wifi':
            wifi_con_to_del = conn.name
    
        if wifi_con_to_del is not None:
            try:
                nmcli.connection.delete(name=wifi_con_to_del)
            except Exception as exc:
                print(exc)

# for testing
if __name__ == "__main__":
    # print(nmcli.device.wifi())
    # nmcli.connection.delete('wb=wlan0')
    config_wifi_settings()
    # config_eth_settings()

