from threading import Thread
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import random
import time
import datetime
import mqtt_communication_module
from loguru import logger


# Теперь у нас будет один файл со всеми списками топиков, которые нам нужны            <---NEW--->
from list_of_mqtt_topics import mqtt_topics_data_analyze_module

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")


class DataAnalyzeModule(Thread):
    def __init__(self, mqtt_broker:str, mqtt_port:int, mqtt_user: str, mqtt_password:str,
                    topic_list: dict, parent=None):
        
        super(DataAnalyzeModule, self).__init__(parent)
        
        self.broker = mqtt_broker
        self.port = mqtt_port
        self.client = ""
        self.client_id = f"korobka-mqtt-{random.randint(0, 100)}"
        self.topic_list = topic_list

        self.water_leak_sensor_last_seen_value = 0
        self.temp1_sensor_last_seen_value = 0
        self.temp2_sensor_last_seen_value = 0
        self.thermo_heater_last_seen_value = 0
        
        self.outlet_group1_state_value = False
        self.outlet_group2_state_value = False

        self.light_dim1_state_value = False
        self.light_dim2_state_value = False
        self.light_light1_state_value = False
        self.light_light2_state_value = False
        self.light_light3_state_value = False

        self.temp1_local_status = 0
        self.temp2_local_status = 0
        self.temp_heater_status = 0
        self.temp_global_error_flag = False
        self.water_global_error_flag = False

        self.temp_sens1_value = 0
        self.temp_sens2_value = 0

        self.electrol_heater1_setpoint_value = 0
        self.water_heater1_setpoint_value = 0

        self.water_leak_status = False

        self.water_leak_sensor_norm_time = 2880
        self.temp_sensor_norm_time = 60
        self.thermo_heater_norm_time = 60

        self.on_message_config = {
            self.topic_list["input_water_leak_last_seen"] : self.set_water_leak_last_seen,
            self.topic_list["input_temp_sens1_last_seen"] : self.set_temp_sens1_last_seen,
            self.topic_list["input_temp_sens2_last_seen"] : self.set_temp_sens2_last_seen,
            self.topic_list["input_thermo_heater_last_seen"] : self.set_thermo_heater_last_seen,
            self.topic_list["input_outlet_group1_state"] : self.set_outlet_group1,
            self.topic_list["input_outlet_group2_state"] : self.set_outlet_group2,
            self.topic_list["input_dim1_state"] : self.set_dim1,
            self.topic_list["input_dim2_state"] : self.set_dim2,
            self.topic_list["input_light1_state"] : self.set_light1,
            self.topic_list["input_light2_state"] : self.set_light2,
            self.topic_list["input_light3_state"] : self.set_light3,
            self.topic_list["input_temp_sens1_value"] : self.set_temp_sens1_value,
            self.topic_list["input_temp_sens2_value"] : self.set_temp_sens2_value,
            self.topic_list["input_electro_heater1_setpoint_value"] : self.set_electro_heater1_setpoint,
            self.topic_list["input_water_heater1_setpoint_value"] : self.set_water_heater1_setpoint,
            self.topic_list["input_water_leak"] : self.water_leak_event,
            self.topic_list["input_temp_sens_norm_time"] : self.set_temp_sens_norm_time,
            self.topic_list["input_water_sens_norm_time"] : self.set_water_sens_norm_time,
            self.topic_list["input_thermo_heat_norm_time"] : self.set_thermo_heat_norm_time,
            self.topic_list["input_water_leak_battery"] : self.set_water_leak_battery,
            self.topic_list["input_temp1_battery"] : self.set_temp1_battery,
            self.topic_list["input_temp2_battery"] : self.set_temp2_battery,
            self.topic_list["input_thermo_heater_battery"] : self.thermo_heater_battery,
        }

        self.mqtt = mqtt_communication_module.Mqtt(mqtt_broker, mqtt_port, mqtt_user, mqtt_password, self.name, self.on_message_config, self.topic_list)
        self.mqtt.start()
        

    def run(self):
        #Логгер
        logger.debug(f"Control logic {self.name} is started")
        while True:
            time.sleep(1)
            self.current_time = self.get_current_unixms_time()

            # Считаем кол-во минут с последнего сеанса связи с датчиками
            water_leak_time_min = int((self.current_time - self.water_leak_sensor_last_seen_value) / 1000 / 60)
            temp1_sensor_time_min = int((self.current_time - self.temp1_sensor_last_seen_value) / 1000 / 60)
            temp2_sensor_time_min = int((self.current_time - self.temp2_sensor_last_seen_value) / 1000 / 60)
            thermo_heater_time_min = int((self.current_time - self.thermo_heater_last_seen_value) / 1000 / 60)
            print(water_leak_time_min, temp1_sensor_time_min, temp2_sensor_time_min, thermo_heater_time_min)

            self.mqtt.publish_topic(self.topic_list["output_leak_sens_last_time"], water_leak_time_min)
            self.mqtt.publish_topic(self.topic_list["output_temp1_sens_last_time"], temp1_sensor_time_min)
            self.mqtt.publish_topic(self.topic_list["output_temp2_sens_last_time"], temp2_sensor_time_min)
            self.mqtt.publish_topic(self.topic_list["output_thermo_heater_last_time"], thermo_heater_time_min)

            # Проверяем когда был последний раз сеанс связи с датчиком, есил было давно, значит он отвалился
            if temp1_sensor_time_min > self.temp_sensor_norm_time:
                self.temp1_local_status = 1
                self.mqtt.publish_topic(self.topic_list["output_temp1_status"], 1)
            elif temp1_sensor_time_min <= self.temp_sensor_norm_time:
                self.temp1_local_status = 0
            
            if temp2_sensor_time_min > self.temp_sensor_norm_time:
                self.mqtt.publish_topic(self.topic_list["output_temp2_status"], 1)
                self.temp2_local_status = 1
            elif temp2_sensor_time_min <= self.temp_sensor_norm_time:
                self.temp2_local_status = 0
            
            if thermo_heater_time_min > self.thermo_heater_norm_time:
                self.temp_heater_status = 1
            elif thermo_heater_time_min <= self.thermo_heater_norm_time:
                self.temp_heater_status = 0
            
            if water_leak_time_min > self.water_leak_sensor_norm_time:
                self.water_leak_status = 1
                self.mqtt.publish_topic(self.topic_list["output_water_leak_status"], 1)
            elif water_leak_time_min <= self.water_leak_sensor_norm_time:
                self.water_leak_status = 0
                self.mqtt.publish_topic(self.topic_list["output_water_leak_status"], 0)
            
            if self.temp1_local_status == 1 or self.temp2_local_status == 1 or self.temp_heater_status == 1:
                self.temp_global_error_flag = True
                self.mqtt.publish_topic(self.topic_list["output_temp_global_error"], 1)
            else:
                self.temp_global_error_flag = False
                self.mqtt.publish_topic(self.topic_list["output_temp_global_error"], 0)
            
             # Проверяем соответствует ли температуры уставке
            if not self.temp1_local_status == 1:
                if int(self.temp_sens1_value) < self.electrol_heater1_setpoint_value:
                    self.mqtt.publish_topic(self.topic_list["output_temp1_status"], 2)  # Low
                elif int(self.temp_sens1_value) > self.electrol_heater1_setpoint_value:
                    self.mqtt.publish_topic(self.topic_list["output_temp1_status"], 3)  # High
                else:
                    self.mqtt.publish_topic(self.topic_list["output_temp1_status"], 0)  # Fine

            if not self.temp2_local_status == 1:
                if int(self.temp_sens2_value) < self.electrol_heater1_setpoint_value:   
                    self.mqtt.publish_topic(self.topic_list["output_temp2_status"], 2)  # Low
                elif int(self.temp_sens2_value) > self.electrol_heater1_setpoint_value: 
                    self.mqtt.publish_topic(self.topic_list["output_temp2_status"], 3)  # High
                else:   
                    self.mqtt.publish_topic(self.topic_list["output_temp2_status"], 0)  # Fine

            # Проверяем кол-во включенных розеток. Если хоть одна включена - True, в противном случае - False
            if self.outlet_group1_state_value or self.outlet_group2_state_value:
                self.mqtt.publish_topic(self.topic_list["output_outlets_global_state"], 1)
            else:
                self.mqtt.publish_topic(self.topic_list["output_outlets_global_state"], 0)
            
            # Проверяем кол-во включенных каналов реле света и диммера. Если хоть один включен - True, в противном случае - False
            if self.light_dim1_state_value or self.light_dim2_state_value or self.light_light1_state_value or self.light_light2_state_value or self.light_light3_state_value:
                self.mqtt.publish_topic(self.topic_list["output_light_global_state"], 1)
            else:
                self.mqtt.publish_topic(self.topic_list["output_light_global_state"], 0)
    
    def thermo_heater_battery(self, value):
        if not self.temp_heater_status == 1:
            if value == "false":
                self.mqtt.publish_topic(self.topic_list["output_thermo_heater_battery_status"], 0)
            if value == "true":
                self.mqtt.publish_topic(self.topic_list["output_thermo_heater_battery_status"], 1)
            

    def set_temp2_battery(self, value):
        if not self.temp2_local_status == 1:
            if int(value) > 10:
                self.mqtt.publish_topic(self.topic_list["output_temp2_battery_status"], 0)
            elif int(value) < 10:
                self.mqtt.publish_topic(self.topic_list["output_temp2_battery_status"], 1)

    def set_temp1_battery(self, value):
        if not self.temp1_local_status == 1:
            if int(value) > 10:
                self.mqtt.publish_topic(self.topic_list["output_temp1_battery_status"], 0)
            elif int(value) < 10:
                self.mqtt.publish_topic(self.topic_list["output_temp1_battery_status"], 1)

    def set_water_leak_battery(self, value):
        if not self.water_leak_status == 1:
            if int(value) > 10:
                self.mqtt.publish_topic(self.topic_list["output_water_battery_status"], 0)
            elif int(value) < 10:
                self.mqtt.publish_topic(self.topic_list["output_water_battery_status"], 1)

    def set_temp_sens_norm_time(self, value):
        try:
            int_value = int(float(value))
            self.temp_sensor_norm_time = int_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int. {e}")
    
    def set_water_sens_norm_time(self, value):
        try:
            int_value = int(float(value))
            self.water_leak_sensor_norm_time = int_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int. {e}")

    def set_thermo_heat_norm_time(self, value):
        try:
            int_value = int(float(value))
            self.thermo_heater_norm_time = int_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int. {e}")

    def water_leak_event(self, value):
        try:
            if value == "false":
                self.water_leak_sensor_state = False
                self.mqtt.publish_topic(self.topic_list["output_water_tape1_state"], "0")
                self.mqtt.publish_topic(self.topic_list["output_water_tape2_state"], "0")
                self.mqtt.publish_topic(self.topic_list["output_water_alarm"], "0")
            elif value == "true":
                self.water_leak_sensor_state = True
                self.mqtt.publish_topic(self.topic_list["output_water_tape1_state"], "1")
                self.mqtt.publish_topic(self.topic_list["output_water_tape2_state"], "1")
                self.mqtt.publish_topic(self.topic_list["output_water_alarm"], "1")
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int. {e}")
            
    def set_water_heater1_setpoint(self, value):
        try:
            int_value = int(float(value))
            self.water_heater1_setpoint_value = int_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int. {e}")
        
    def set_electro_heater1_setpoint(self, value):
        try:
            int_value = int(value)
            self.electrol_heater1_setpoint_value = int_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int. {e}")

    def set_temp_sens2_value(self, value):
        try:
            float_value = float(value)
            self.temp_sens2_value = float_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->float. {e}")
    
    def set_temp_sens1_value(self, value):
        try:
            float_value = float(value)
            self.temp_sens1_value = float_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->float. {e}")
    
    def set_dim1(self, value):
        try:
            bool_value = bool(int(value))
            self.light_dim1_state_value = bool_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int->bool. {e}")
    
    def set_dim2(self, value):
        try:
            bool_value = bool(int(value))
            self.light_dim2_state_value = bool_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int->bool. {e}")
    
    def set_light1(self, value):
        try:
            bool_value = bool(int(value))
            self.light_light1_state_value = bool_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int->bool. {e}")
    
    def set_light2(self, value):
        try:
            bool_value = bool(int(value))
            self.light_light2_state_value = bool_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int->bool. {e}")
    
    def set_light3(self, value):
        try:
            bool_value = bool(int(value))
            self.light_light3_state_value = bool_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int->bool. {e}")

    def set_outlet_group2(self, value):
        try:
            bool_value = bool(int(value))
            self.outlet_group2_state_value = bool_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int->bool. {e}")
    
    def set_outlet_group1(self, value):
        try:
            bool_value = bool(int(value))
            self.outlet_group1_state_value = bool_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int->bool. {e}")

    def set_water_leak_last_seen(self, value):
        try:
            if not self.water_leak_sensor_state:
                int_value = int(value)
                self.water_leak_sensor_last_seen_value = int_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int. {e}")

    def set_thermo_heater_last_seen(self, value):
        try:
            int_value = int(value)
            self.thermo_heater_last_seen_value = int_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int. {e}")

    def set_temp_sens1_last_seen(self, value):
        try:
            int_value = int(value)
            self.temp1_sensor_last_seen_value = int_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int. {e}")

    def set_temp_sens2_last_seen(self, value):
        try:
            int_value = int(value)
            self.temp2_sensor_last_seen_value = int_value
        except Exception as e:
            logger.debug(f"Ошибка при переводе str->int. {e}")         
                
    def get_current_unixms_time(self):
        date = datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)
        seconds =(date.total_seconds())
        return round(seconds*1000)


def test():
    broker = "192.168.4.3"
    port = 1883

    pid_test = DataAnalyzeModule(broker, port, topic_list=mqtt_topics_data_analyze_module, mqtt_user=None, mqtt_password=None)
    pid_test.start()

        

if __name__ == "__main__":
    test()