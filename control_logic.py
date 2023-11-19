from threading import Thread
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import random
import time
from loguru import logger

# Теперь у нас будет один файл со всеми списками топиков, которые нам нужны            <---NEW--->
from list_of_mqtt_topics import mqtt_topics_control_logic

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")

# The `PIDControl` class is a threaded class that implements a PID controller for a given MQTT broker
# and port, with setpoint, feedback, and control topics, and specified PID parameters.
class ControlLogic(Thread):
    def __init__(self, mqtt_broker:str, mqtt_port:int, mqtt_user: str, mqtt_passw:str,
                    topic_list: dict, parent=None):
        
        super(ControlLogic, self).__init__(parent)
        
        self.broker = mqtt_broker
        self.port = mqtt_port
        self.client = ""
        self.client_id = f"korobka-mqtt-{random.randint(0, 100)}"
        self.topic_list = topic_list
    

    def run(self):
        #Логгер
        logger.debug(f"Control logic {self.name} is started")

        
        while True:
            time.sleep(1)
            print(round(time.time() * 1000))

    
    def set_water_valves(self, value):
        if value == "false":
            self.mqtt_publish_topic("/devices/watercontrol_79/controls/K2/on", 0)
            self.mqtt_publish_topic("/devices/watercontrol_79/controls/K1/on", 0)
            self.mqtt_publish_topic("/devices/watercontrol_79/controls/Alarm/on", 0)
        elif value == "true":
            self.mqtt_publish_topic("/devices/watercontrol_79/controls/K2/on", 1)
            self.mqtt_publish_topic("/devices/watercontrol_79/controls/K1/on", 1)
            self.mqtt_publish_topic("/devices/watercontrol_79/controls/Alarm/on", 1)
    

    def calculate_hot_water_consuming(self, value):
        total_consuming = int(value) / 1000
        self.mqtt_publish_topic("/devices/WaterConsuming/controls/Hot Last Day Consuming/on", total_consuming)
        self.mqtt_publish_topic("/devices/WaterConsuming/controls/Hot Last Month Consuming/on", total_consuming)
        self.mqtt_publish_topic("/devices/WaterConsuming/controls/Hot Total Consuming/on", total_consuming)


    def calculate_cold_water_consuming(self, value):
        total_consuming = int(value) / 1000
        self.mqtt_publish_topic("/devices/WaterConsuming/controls/Cold Last Day Consuming/on", total_consuming)
        self.mqtt_publish_topic("/devices/WaterConsuming/controls/Cold Last Month Consuming/on", total_consuming)
        self.mqtt_publish_topic("/devices/WaterConsuming/controls/Cold Total Consuming/on", total_consuming)

    
    def connect_mqtt(self, whois: str) -> mqtt:
        """
        The function `connect_mqtt` connects to an MQTT broker and returns the MQTT client.
        :return: an instance of the MQTT client.
        """
        logger.debug(f"MQTT client in {whois} started connect to broker")
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logger.debug(f"{whois} Connected to MQTT Broker!")
                return
            else:
                logger.debug(f"{whois} Failed to connect, return code {rc}")

        mqtt_client = mqtt.Client(self.client_id)
        mqtt_client.on_connect = on_connect
        mqtt_client.connect(self.broker, self.port)
        return mqtt_client
    
    def subscribe(self, client: mqtt):
        for key, value in self.topic_list.items():
            if not "output" in key:
                client.subscribe(value)
        client.on_message = self.on_message
    
    def on_message(self, client, userdata, msg):
        
        config = {
            self.topic_list["input_hot_water_leak"] : self.set_water_valves,
            self.topic_list["input_cold_water_leak"] : self.set_water_valves,
            self.topic_list["input_hot_water_counter"] : self.calculate_hot_water_consuming,
            self.topic_list["input_cold_water_counter"] : self.calculate_cold_water_consuming,
        }
        
        topic_name = msg.topic 
        topic_value = msg.payload.decode("utf-8")
        
        config[topic_name](topic_value)
            
                
    def mqtt_start(self):
        
        self.client = self.connect_mqtt(self.name)
        self.subscribe(self.client)
        self.client.loop_start()

    #Публикует топик с именем topic_name и значением topic_value
    def mqtt_publish_topic(self, topic_name, topic_value):
        publish.single(str(topic_name), str(topic_value), hostname=self.broker)
    

def test():
    broker = "192.168.44.10"
    port = 1883

    pid_test = ControlLogic(broker, port, topic_list=mqtt_topics_control_logic, mqtt_user=None, mqtt_passw=None)
    pid_test.mqtt_start()
    pid_test.start()
        

if __name__ == "__main__":
    test()