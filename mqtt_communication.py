import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import serial_port
import time


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
        topic_val = int(msg.payload.decode("utf-8"))
        # print(topic_name, topic_val, type(topic_val))
        if topic_name[2] == "outletcontrol_34":
            ch = topic_name[-1]
            if ch == "OutletGroup1":
                if topic_val == 1:
                    cmd1 = "electric_ctrl.b0.picc=43"
                    cmd2 = "electric_ctrl.b0.picc2=44"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)
                else:
                    cmd1 = "electric_ctrl.b0.picc=41"
                    cmd2 = "electric_ctrl.b0.picc2=42"
                    serial_port.serial_write(self.comport, cmd1)
                    serial_port.serial_write(self.comport, cmd2)

    def run(self):
        while True:
            try:
                self.mqtt_client.loop_forever()
            except Exception as exc:
                print(exc)


def wb_mqtt_switch(mqtt_dev_id: str, mqtt_control: str, val: int):
    try:
        "/devices/outletcontrol_34 /controls/OutletGroup1"
        mqtt_host = "192.168.4.9"
        topic = f"/devices/{mqtt_dev_id}/controls/{mqtt_control}/on"
        publish.single(topic, val, hostname=mqtt_host)
    except Exception as exc:
        print(exc)


def _test_main():
    # publish.single("/devices/outletcontrol_34/controls/OutletGroup1/on", 0, hostname="192.168.44.10")
    # wb_mqtt_switch()
    client = mqtt.Client()
    mqtt_subscribe_topics = "/devices/outletcontrol_34/controls/OutletGroup1"
    mqtt_test = MQTTSubscriberThread(client, "192.168.4.9", 1883, mqtt_subscribe_topics)
    # mqtt_test.setDaemon(True)
    mqtt_test.start()


if __name__ == "__main__":
    _test_main()
