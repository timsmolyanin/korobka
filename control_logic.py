from threading import Thread
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import random
import time
import datetime
import nmcli
from loguru import logger
import git
from subprocess import call


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

        self.sens1_last_seen_value = 0
        self.sens2_last_seen_value = 0
        self.ms_since_epoch = 0


        self.wifi_state = 0
        
        self.wifi_client_ssid = None
        self.wifi_client_password = None
        
        self.eth_mode = None
        self.eth_ip = None
        self.eth_mask = None
        self.eth_gateway = None

        self.url = "https://github.com/timsmolyanin/korobka"
    

    def run(self):
        #Логгер
        logger.debug(f"Control logic {self.name} is started")
        while True:
            time.sleep(1)
            date= datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)
            seconds =(date.total_seconds())
            self.ms_since_epoch = round(seconds*1000)
            test1 = self.ms_since_epoch - self.sens1_last_seen_value
            test2 = self.ms_since_epoch - self.sens2_last_seen_value
            # print(f"Sens1 last seen {test1} ms ago" )
            # print(f"Sens2 last seen {test2} ms ago" )

    def update_software(self, value):
        try:
            logger.debug("Start to update")
            g = git.cmd.Git("/root/wk/abc/korobka")
            repo = git.Repo("/root/wk/abc/korobka")
            logger.debug("Try to reset --hard")
            repo.git.reset('--hard')
            logger.debug("reset hard is finished, try to pull")
            g.pull()
            logger.debug("Pull finished")

            logger.debug("try to restart service")
            call(["systemctl", "restart", "korobka_app.service"])
        except Exception as e:
            logger.debug("update failed", e)

    def set_eth_mode(self, mode):
        if mode == "":
            pass
        else:
            if mode == "static":
                self.eth_mode = self.eth_static_mode
            if mode == "dhcp":
                self.eth_mode = self.eth_dhcp_mode
    
    def set_eth_ip(self, value):
        self.eth_ip = str(value)
    
    def set_eth_mask(self, value):
        self.eth_mask = str(value)
    
    def set_eth_gateway(self, value):
        self.eth_gateway = str(value)
    
    def delete_wifi_conn(self):
        for conn in nmcli.connection():
            if conn.conn_type == 'wifi':
                try:
                    nmcli.connection.delete(name=conn.name)
                except Exception as exc:
                    print(exc)
                
    def eth_static_mode(self):
        if self.eth_gateway == "None":
            logger.debug("Выполняется настройка статического IP адреса без шлюза")
            nmcli.connection.modify("wb-eth0", {
                "ipv4.addresses": f"{self.eth_ip}/{self.eth_mask}",
                "ipv4.method": "manual"
            })
        else:
            logger.debug("Выполняется настройка статического IP адреса с указанием шлюза")
            nmcli.connection.modify("wb-eth0", {
                "ipv4.addresses": f"{self.eth_ip}/{self.eth_mask}",
                "ipv4.gateway": f"{self.eth_gateway}",
                "ipv4.method": "manual"
            })
    
    def eth_dhcp_mode(self):
        logger.debug("Выполняется получение IP адреса от сервера DHCP")
        nmcli.connection.modify('wb-eth0', {
            "ipv4.method": "auto"
        })
    
    def wifi_client_mode(self):
        try:
            logger.debug(f'Подключение к Wi-Fi сети "{self.wifi_client_ssid}", используя пароль "{self.wifi_client_password}"')
            nmcli.device.wifi_connect(ssid=self.wifi_client_ssid, password=self.wifi_client_password)
            logger.debug(f'Успешное подключение')
        except Exception as exception:
            logger.debug("Ошибка при подключении к сети:")
            logger.debug(f"{exception}")


    def set_wifi_client_ssid(self, value):
        self.wifi_client_ssid = str(value)
        
    def set_wifi_client_password(self, value):
        self.wifi_client_password = str(value)

    def wifi_adapter_off(self):
        nmcli.radio.wifi_off()
        logger.debug(f"{self.name}: Wifi adapter is OFF")
        
    def wifi_adapter_on(self):
        nmcli.radio.wifi_on()
        logger.debug(f"{self.name}: Wifi adapter is ON")
    
    def wifi_accept(self, value):
        if int(value) == 0:
            return
        if int(value) == 1:
            self.delete_wifi_conn()
            self.set_wifi_state(1)
            time.sleep(5)
            self.wifi_client_mode()

    def set_wifi_state(self, value):
        self.wifi_state = int(value)
        if self.wifi_state == 2:
            return
        if self.wifi_state == 0:
            self.wifi_adapter_off()
        if self.wifi_state == 1:
            self.wifi_adapter_on()

    def sens2_last_seen(self, value):
        self.sens2_last_seen_value = int(value)

    def sens1_last_seen(self, value):
        self.sens1_last_seen_value = int(value)

    
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


    def system_reboot(self, value):
        logger.debug("try to restart service")
        call(["reboot", ])

    
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
            self.topic_list["input_sens1_last_seen"] : self.sens1_last_seen,
            self.topic_list["input_sens2_last_seen"] : self.sens2_last_seen,
            self.topic_list["input_wifi_state"] : self.set_wifi_state,
            self.topic_list["input_wifi_ssid"] : self.set_wifi_client_ssid,
            self.topic_list["input_wifi_passw"] : self.set_wifi_client_password,
            self.topic_list["input_eth0_mode"] : self.set_eth_mode,
            self.topic_list["input_eth0_ip"] : self.set_eth_ip,
            self.topic_list["input_eth0_mask"] : self.set_eth_mask,
            self.topic_list["input_eth0_gateway"] : self.set_eth_gateway,
            self.topic_list["input_update_state"] : self.update_software,
            self.topic_list["input_wifi_accept"] : self.wifi_accept,
            self.topic_list["input_system_reboot"] : self.system_reboot,
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

def test2():
    print("Start to update")
    g = git.cmd.Git("/root/wk/abc/korobka")
    repo = git.Repo("/root/wk/abc/korobka")
    print("Try to reset --hard")
    repo.git.reset('--hard')
    print("reset hard is finished, try to pull")
    g.pull()
    print("Pull finished")
        

if __name__ == "__main__":
    test()