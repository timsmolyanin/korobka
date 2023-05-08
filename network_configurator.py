#!/root/wk/py392/bin/python

"""
Настройки ethernet порта:
- DHCP
- Static IP

Настройки Wi-Fi модема:
- login/password

Алгоритм:
Когда пользователь осуществляет настройку сети, сначала осуществляется запись в
конфигурационный файл введеных пользователем данных.
Затем вызывается функция, которая считывает с конфигурационного файла настройки
и которая записывает введенные настройки в /etc/network/interfaces файл.


"""

import yaml
import subprocess as p

def form_network_settings() -> str:
    """

    :return:
    """

    ETH0_DHCP_STRING = "auto eth0\n   iface eth0 inet dhcp"
    ETH0_CONN_SETTINGS_STRING = ""
    WIFI_CONN_SETTINGS_STRING = ""

    template = "# /etc/network/interfaces -- configuration file for ifup(8), ifdown(8)\n\n" \
               "# The loopback interface\nauto lo\niface lo inet loopback"

    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # WIFI
    wifi_configs = config["network"]["wifi"]
    eth_configs = config["network"]["eth0"]

    if not wifi_configs["state"]:
        WIFI_CONN_SETTINGS_STRING = "# Wi-Fi is not used"
    else:
        wifi_ssid = wifi_configs["ssid"]
        wifi_password = wifi_configs["password"]
        WIFI_CONN_SETTINGS_STRING = f"# Wireless interfaces wlan0\nauto wlan0\niface wlan0 inet dhcp\n" \
                                    f"   wpa-ssid {wifi_ssid}\n   wpa-psk {wifi_password}"

    # print(WIFI_CONN_SETTINGS_STRING)

    # ETHERNET
    eth_mode = eth_configs["mode"]
    if eth_mode == "static":
        eth0_ip = eth_configs["ip"]
        eth0_mask = eth_configs["mask"]
        eth0_gateway = eth_configs["gateway"]
        if eth0_gateway == "None":
            ETH0_CONN_SETTINGS_STRING = f"# Ethernet Port1 eth0\niface eth0 inet static\n   address {eth0_ip}\n" \
                                f"   netmask {eth0_mask}"
        else:
            ETH0_CONN_SETTINGS_STRING = f"# Ethernet Port1 eth0\niface eth0 inet static\n   address {eth0_ip}\n" \
                                    f"   netmask {eth0_mask}\n   gateway {eth0_gateway}"
    elif eth_mode == "dhcp":
        ETH0_CONN_SETTINGS_STRING = ETH0_DHCP_STRING

    # print(ETH0_CONN_SETTINGS_STRING)

    network_settings = f"{template}{WIFI_CONN_SETTINGS_STRING}\n\n{ETH0_CONN_SETTINGS_STRING}"
    return network_settings


def write_network_configs(network_conf: str, path: str) -> None:
    """

    :param path:
    :param network_conf:
    :return:
    """
    network_configs = network_conf
    with open(path, "w") as f:
        f.write(network_configs)


def test():
    n = form_network_settings()
    # print(n)
    # создаем бэкап файл прежней конфигурации
    p.run(["cp", "/etc/network/interfaces", "/etc/network/interfaces.backup"])

    # удаляем файл со старой конфигурацией
    p.run(["rm", "/etc/network/interfaces"])

    # подсовываем файл с новой конфигой
    path = "/etc/network/interfaces"
    write_network_configs(n, path)

    # далее необходимо перезагрузить интерфейсы и как-то проверить, что конфиги приняты



if __name__ == "__main__":
    test()
