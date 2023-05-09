#!/root/wk/py392/bin/python

"""
Настройки ethernet порта:
- DHCP
- Static IP

Настройки Wi-Fi модема:
- login/password

Алгоритм:
Пользователь вводит данные, нажимает ОК или что там будет.
Введенные данные сохраняются в общй конфигурационный файл config.yaml.
Затем происходят следующие действия:
1. Спасаем файл конфигурации "/etc/network/interfaces", создавая его резервную копию "/etc/network/interfaces.backup";
2. Удаляем оригинал "/etc/network/interfaces";
3. Формируем новый "/etc/network/interfaces" файл на основе введеных пользователем данных;
4. Записываем новый конфиг и проверим его наличие;
5. Если все успешно, то рестартуем сетевые интерфейсы (пока для простоты будут перезагружаться и wi-fi и eth
независимо от того, что настраивал пользователь), чтобы новый конфиг применился;
6. Еще бы как-то проверять, что настройки применились и все работает...

"""

import yaml
import subprocess as p


def make_config_backup(file: str) -> list:
    """
    Функция создает резервную копию конфигурационного файла.
    Копия сохраняется там же, где лежит оригинал, но с расширением ".backup"
    :param file: тип str, абсолютный путь до спасаемого файла
    :return: тип list, код операции (0-успех, 1-ошибка) и описание ошибки (понадобится для логов)
    """
    return_code = 0
    error_desc = ""
    output = p.run(["cp", file, f"{file}.backup"], capture_output=True)
    return_code = output.returncode
    if return_code != 0:
        error_desc = output.stderr

    return [return_code, error_desc]


def del_old_network_config(file: str) -> list:
    """
    Функция удаляет файл, указанный в аргументе.
    :param file: тип str, абсолютный путь до удаляемого файла /a/b/c/file
    :return: тип list, код операции (0-успех, 1-ошибка) и описание ошибки (понадобится для логов)
    """
    return_code = 0
    error_desc = ""
    output = p.run(["rm", file], capture_output=True)
    return_code = output.returncode
    if return_code != 0:
        error_desc = output.stderr

    return [return_code, error_desc]


def form_network_settings() -> str:
    """

    :return:
    """

    ETH0_DHCP_STRING = "auto eth0\n   iface eth0 inet dhcp"
    ETH0_CONN_SETTINGS_STRING = ""
    WIFI_CONN_SETTINGS_STRING = ""

    template = "# /etc/network/interfaces -- configuration file for ifup(8), ifdown(8)\n\n" \
               "# The loopback interface\nauto lo\niface lo inet loopback\n"

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
        WIFI_CONN_SETTINGS_STRING = f"\n# Wireless interfaces wlan0\nauto wlan0\niface wlan0 inet dhcp\n" \
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


def write_network_configs(network_conf: str, path: str) -> list:
    """
    Сохраняет сформированный текст конфигурации сетевых интерфейсов в файл

    :param network_conf: тип str, текст конфигурации
    :param path: тип str, абсолютный путь файла /a/b/c/fileName
    :return: тип list, код операции (0-успех, 1-ошибка) и описание ошибки (понадобится для логов)
    """
    return_code = 0
    error_desc = ""
    try:
        network_configs = network_conf
        with open(path, "w") as f:
            f.write(network_configs)
    except Exception as exc:
        return_code = 1
        error_desc = exc

    return [return_code, error_desc]


def restart_network_interfaces(interface: str) -> list:
    """
    Function is restarting NetworkManager process to accepting configs which has been wrote
    linux cmd: ifdown interfaceName && ifup interfaceName
    :param interface: тип str, название сетевого интерфейса
    :return: тип list, код операции (0-успех, 1-ошибка) и описание ошибки (понадобится для логов)
    """

    return_code = 0
    error_desc = ""

    cmd = f"ifdown {interface} && sudo ifup {interface}"
    # output = p.Popen(cmd, shell=True, stdout=p.PIPE)
    # output = p.Popen(cmd, shell=True)
    output = p.run(cmd, shell=True, capture_output=True)
    return_code = output.returncode
    if return_code != 0:
        error_desc = output.stderr

    return [return_code, error_desc]


def test():
    # orig_conf_file = "/etc/network/interfaces"
    #
    # new_conf_file = ""
    # test_conf_file = "/root/wk/korobka/int"
    # global_st = 0
    #
    # """ 1. Создаем копию конфиги """
    # print("1. Create copy of orig config")
    # st = make_config_backup(orig_conf_file)
    # if st[0] == 0:
    #     global_st = 0
    # else:
    #     global_st = 1
    #     print(st)
    #
    # print("1. done")
    #
    # """ 2. Удаляем оригинал """
    # print("2. Delete orig config")
    # if global_st == 0:
    #     st = del_old_network_config(orig_conf_file)
    #     if st[0] == 0:
    #         global_st = 0
    #     else:
    #         global_st = 1
    #         print(st)
    #
    # print("2. done")
    #
    # """ 3. Формируем новый конфиг """
    # print("3. Forming new config")
    # if global_st == 0:
    #     new_conf_file = form_network_settings()
    #
    # print("3. done")
    # print(new_conf_file)
    # """ 4. Подсовываем файл с новой конфигой """
    # print("4. Added new config")
    # st = write_network_configs(new_conf_file, orig_conf_file)
    # if st == 0:
    #     global_st = 0
    # else:
    #     global_st = 1
    #     print(st)
    #
    # print("4 done")
    #
    # """ 5. Рестартуем сетевые интерфейсы """
    # print("5. Restarting network")
    # if global_st == 0:
    #     st = restart_network_interfaces()
        # print(st)
    #
    # print("5 done")

    print("RESTART wlan0")
    st = restart_network_interfaces("wlan2")
    print(st)


if __name__ == "__main__":
    test()
