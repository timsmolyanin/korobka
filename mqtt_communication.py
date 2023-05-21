import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import serial_port
import time
import json

from threading import Thread


class MQTTSubscriberThread(Thread):
    def __init__(self, mqtt_client, host, port, topics_list, comport, parent=None):
        super(MQTTSubscriberThread, self).__init__(parent)
        self.mqtt_client = mqtt_client
        self.host = host
        self.port = port
        self.topics_list = topics_list
        # self.logger = logger
        self.mqtt_client.connect(self.host, self.port, 60)
        # self.logger.info("MQTT")

        self.comport = comport

        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        print(self.topics_list)
        self.mqtt_client.subscribe(self.topics_list)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(f"Topic: {msg.topic}, value: {str(msg.payload)}")
        topic_name = msg.topic.split("/")
        # print(msg.payload.decode("utf-8"))
        topic_val = msg.payload.decode("utf-8")
        # print(topic_name, topic_val, type(topic_val))
        if topic_name[2] == "outletcontrol_34":
            ch = topic_name[-1]
            if ch == "OutletGroup1":
                if topic_val == "1":
                    cmd1 = "electric_ctrl.b0.picc=43"
                    cmd2 = "electric_ctrl.b0.picc2=44"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
                else:
                    cmd1 = "electric_ctrl.b0.picc=41"
                    cmd2 = "electric_ctrl.b0.picc2=42"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
            elif ch == "OutletGroup2":
                if topic_val == "1":
                    cmd1 = "electric_ctrl.b1.picc=47"
                    cmd2 = "electric_ctrl.b1.picc2=48"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
                else:
                    cmd1 = "electric_ctrl.b1.picc=45"
                    cmd2 = "electric_ctrl.b1.picc2=46"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
            elif ch == "OutletGroup3":
                if topic_val == "1":
                    cmd1 = "electric_ctrl.b2.picc=51"
                    cmd2 = "electric_ctrl.b2.picc2=52"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
                else:
                    cmd1 = "electric_ctrl.b2.picc=49"
                    cmd2 = "electric_ctrl.b2.picc2=50"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
        elif topic_name[2] == "lightcontrol_145":
            ch = topic_name[-1]
            if ch == "LightGroup1":
                if topic_val == "1":
                    cmd1 = "light_ctrl.b0.picc=43"
                    cmd2 = "light_ctrl.b0.picc2=44"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
                else:
                    cmd1 = "light_ctrl.b0.picc=41"
                    cmd2 = "light_ctrl.b0.picc2=42"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
            elif ch == "LightGroup2":
                if topic_val == "1":
                    cmd1 = "light_ctrl.b1.picc=47"
                    cmd2 = "light_ctrl.b1.picc2=48"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
                else:
                    cmd1 = "light_ctrl.b1.picc=45"
                    cmd2 = "light_ctrl.b1.picc2=46"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
            elif ch == "LightGroup3":
                if topic_val == "1":
                    cmd1 = "light_ctrl.b2.picc=51"
                    cmd2 = "light_ctrl.b2.picc2=52"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
                else:
                    cmd1 = "light_ctrl.b2.picc=49"
                    cmd2 = "light_ctrl.b2.picc2=50"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
            if ch == "LightGroup4":
                if topic_val == "1":
                    cmd1 = "light_ctrl.b3.picc=55"
                    cmd2 = "light_ctrl.b3.picc2=56"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
                else:
                    cmd1 = "light_ctrl.b3.picc=53"
                    cmd2 = "light_ctrl.b3.picc2=54"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
            elif ch == "LightGroup5":
                if topic_val == "1":
                    cmd1 = "light_ctrl.b4.picc=59"
                    cmd2 = "light_ctrl.b4.picc2=60"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
                else:
                    cmd1 = "light_ctrl.b4.picc=57"
                    cmd2 = "light_ctrl.b4.picc2=58"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
            elif ch == "LightGroup6":
                if topic_val == "1":
                    cmd1 = "light_ctrl.b5.picc=63"
                    cmd2 = "light_ctrl.b5.picc2=64"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
                else:
                    cmd1 = "light_ctrl.b5.picc=61"
                    cmd2 = "light_ctrl.b5.picc2=62"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
        elif topic_name[2] == "0xa4c1387ec9c1d434":
            if topic_val == "false":
                smart_valve_controller("open")
                cmd1 = "water_ctrl.q0.picc=171"
                cmd2 = "water_ctrl.q6.picc=183"
                cmd3 = "water_ctrl.q7.picc=185"
                serial_port.serial_write(self.comport, cmd1)
                serial_port.serial_write(self.comport, cmd2)
                serial_port.serial_write(self.comport, cmd3)
            elif topic_val == 'true':
                smart_valve_controller("close")
                cmd1 = "water_ctrl.q0.picc=177"
                cmd2 = "water_ctrl.q6.picc=184"
                cmd3 = "water_ctrl.q7.picc=186"
                serial_port.serial_write(self.comport, cmd1)
                serial_port.serial_write(self.comport, cmd2)
                serial_port.serial_write(self.comport, cmd3)

    def run(self):
        while True:
            try:
                self.mqtt_client.loop_forever()
            except Exception as exc:
                print(exc)


def wb_mqtt_switch(mqtt_dev_id: str, mqtt_control: str, val: int):
    try:
        mqtt_host = "192.168.4.9"
        topic = f"/devices/{mqtt_dev_id}/controls/{mqtt_control}/on"
        publish.single(topic, val, hostname=mqtt_host)
    except Exception as exc:
        print(exc)


def smart_valve_controller(val):
    cmd = None
    if val == "open":
        cmd = {
            "state": "ON"
        }
    elif val == "close":
        cmd = {
            "state": "OFF"
        }
    cmd_str = json.dumps(cmd)
    try:
        mqtt_host = "192.168.4.9"
        topic = "zigbee2mqtt/0xa4c13844020516ee/set"
        publish.single(topic, cmd_str, hostname=mqtt_host)
    except Exception as exc:
        print(exc)


def _test_main():
    # publish.single("/devices/outletcontrol_34/controls/OutletGroup1/on", 0, hostname="192.168.44.10")
    # wb_mqtt_switch()
    # client = mqtt.Client()
    # mqtt_subscribe_topics = "/devices/outletcontrol_34/controls/OutletGroup1"
    # mqtt_test = MQTTSubscriberThread(client, "192.168.4.9", 1883, mqtt_subscribe_topics)
    # mqtt_test.setDaemon(True)
    # mqtt_test.start()

    val = {
        "state": "OFF"
    }
    cmd = json.dumps(val)
    # print(cmd)
    smart_valve_controller(cmd)


if __name__ == "__main__":
    _test_main()
