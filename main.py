import serial_port
import mqtt_communication
import paho.mqtt.client as mqtt


def main():
    sp = serial_port.serial_connect("COM3", 115200)
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
                                 ("/devices/0xa4c1387ec9c1d434/controls/water_leak", 0)
                                 ]

        mqtt_test = mqtt_communication.MQTTSubscriberThread(client, "192.168.4.9", 1883, mqtt_subscribe_topics, sp[1])
        mqtt_test.start()

        nex_reader = serial_port.NextionReader(sp[0], sp[1])
        nex_reader.start()


if __name__ == "__main__":
    main()
