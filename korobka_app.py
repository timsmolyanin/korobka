#!/root/wk/py310/bin/python

import paho.mqtt.client as mqtt
import nextion_mqtt_bridge
import data_analyze_module
import list_of_mqtt_topics
import system_module


def main():
    comport = "/dev/ttyUSB0"
    # comport = "COM4"
    baudrate = 115200
    # broker = "192.168.44.11"
    broker = "127.0.0.1"
    port = 1883

    mqtt_topics_data_analyze_module = list_of_mqtt_topics.mqtt_topics_data_analyze_module
    next_mqtt_bridge = nextion_mqtt_bridge.NextionMqttBridge(mqtt_port=port, mqtt_broker=broker, mqtt_passw=None, mqtt_user=None,
                                            comport_baudrate=baudrate, comport_name=comport)
    
    next_mqtt_bridge.start()
    next_mqtt_bridge.mqtt_start()

    data_analyze_mod = data_analyze_module.DataAnalyzeModule(broker, port, topic_list=mqtt_topics_data_analyze_module, mqtt_user=None, mqtt_password=None)
    data_analyze_mod.start()

    system_mod = system_module.SystemModule(broker, port, None, None)


if __name__ == "__main__":
    main()
