#!/root/wk/py310/bin/python

import paho.mqtt.client as mqtt
import nextion_mqtt_bridge
import control_logic
import list_of_mqtt_topics


def main():
    comport = "COM3"
    baudrate = 115200
    broker = "192.168.44.10"
    # broker = "127.0.0.1"
    port = 1883

    mqtt_topics_control_logic = list_of_mqtt_topics.mqtt_topics_control_logic

    next_mqtt_bridge = nextion_mqtt_bridge.NextionMqttBridge(mqtt_port=port, mqtt_broker=broker, mqtt_passw=None, mqtt_user=None,
                                            comport_baudrate=baudrate, comport_name=comport)
    ctrl_logic = control_logic.ControlLogic(broker, port, topic_list=mqtt_topics_control_logic, mqtt_user=None, mqtt_passw=None)

    next_mqtt_bridge.start()
    next_mqtt_bridge.mqtt_start()

    ctrl_logic.mqtt_start()
    ctrl_logic.start()



if __name__ == "__main__":
    main()
