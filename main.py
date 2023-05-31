import serial_port
import mqtt_communication
import paho.mqtt.client as mqtt
import yaml


def main():
    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    serial_com_port_name = config["serial"]["port"]
    serial_com_port_speed = config["serial"]["baud"]
    mqtt_broker_address = config["mqtt"]["ip"]
    mqtt_broker_port = config["mqtt"]["port"]
    
    sp = serial_port.serial_connect(serial_com_port_name, serial_com_port_speed)
    if sp[0]:
        client = mqtt.Client()
        mqtt_subscribe_topics = [("/devices/outletcontrol_34/controls/OutletGroup1", 0),
                                 ("/devices/outletcontrol_34/controls/OutletGroup2", 0),
                                 ("/devices/outletcontrol_34/controls/OutletGroup3", 0),
                                 ("/devices/lightcontrol_145/controls/LightGroup1", 0),
                                 ("/devices/lightcontrol_145/controls/LightGroup2", 0),
                                 ("/devices/lightcontrol_145/controls/LightGroup3", 0),
                                 ("/devices/lightcontrol_145/controls/LightGroup4", 0),
                                 ("/devices/lightcontrol_145/controls/LightGroup5", 0),
                                 ("/devices/lightcontrol_145/controls/LightGroup6", 0),
                                 ("/devices/0xa4c1387ec9c1d434/controls/water_leak", 0),
                                 ("/devices/0xa4c1386c14f32cb1/controls/water_leak", 0),
                                 ("/devices/network/controls/Ethernet IP", 0),
                                 ("/devices/network/controls/Wi-Fi IP", 0),
                                 ("/devices/network/controls/Wi-Fi IP Online Status", 0),
                                 ("/devices/0x00158d00091c5b60/controls/battery", 0),
                                 ("/devices/0x00158d00091c5b60/controls/temperature", 0),
                                 ("/devices/0x00158d00091c5aea/controls/battery", 0),
                                 ("/devices/0x00158d00091c5aea/controls/temperature", 0),
                                 ("/devices/0x84fd27fffe0e709f/controls/current_heating_setpoint", 0),
                                 ("/devices/0x84fd27fffe0e709f/controls/battery_low", 0),
                                 ("/devices/0x84fd27fffe6d74bb/controls/current_heating_setpoint", 0),
                                 ("/devices/0x84fd27fffe6d74bb/controls/battery_low", 0)
                                 ]

        mqtt_test = mqtt_communication.MQTTSubscriberThread(client, mqtt_broker_address, mqtt_broker_port, mqtt_subscribe_topics, sp[1])
        mqtt_test.start()

        nex_reader = serial_port.NextionReader(sp[0], sp[1])
        nex_reader.start()

        cmd = "main.q0.picc=2"
        serial_port.serial_write(sp[1], cmd)


if __name__ == "__main__":
    main()
