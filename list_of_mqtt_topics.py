list_of_mqtt_topics = [("/devices/wb-led_66/controls/Channel 1", 0),
                        ("/devices/wb-led_66/controls/Channel 2", 0),
                        ("/devices/wb-led_66/controls/Channel 3", 0),
                        ("/devices/wb-led_66/controls/Channel 1 Brightness", 0),
                        ("/devices/wb-led_66/controls/Channel 2 Brightness", 0),
                        ("/devices/wb-led_66/controls/Channel 3 Brightness", 0),
                        ("/devices/wb-mr3_147/controls/K1", 0),
                        ("/devices/wb-mr3_147/controls/K2", 0),
                        ("/devices/wb-mr3_147/controls/K3", 0),
                        ("/devices/0x00158d00091c5add/controls/temperature", 0),
                        ("/devices/0x00158d00091c5add/controls/battery", 0),
                        ("/devices/0x00158d0009753163/controls/temperature", 0),
                        ("/devices/0x00158d0009753163/controls/battery", 0),
                        ("/devices/0xa4c138da7c2d6d15/controls/water_leak", 0),
                        ("/devices/network/controls/Wi-Fi IP", 0),
                        ("/devices/network/controls/Wi-Fi IP Online Status", 0),
                        ("/devices/network/controls/Ethernet IP", 0),
                        ("/devices/DataAnalyzeModule/controls/LightGlobalState", 0),
                        ("/devices/DataAnalyzeModule/controls/OutletsGlobalState", 0),
                        ("/devices/DataAnalyzeModule/controls/LeakSensorTimeError", 0),
                        ("/devices/DataAnalyzeModule/controls/Temp1SensorTimeError", 0),
                        ("/devices/DataAnalyzeModule/controls/Temp2SensorTimeError", 0),
                        ("/devices/0x50325ffffe033772/controls/current_heating_setpoint", 0),
                        ("/devices/ElectrolHeaterModule/controls/Heater1 Setpoint", 0),
                        ("/devices/DataAnalyzeModule/controls/TempRegulator1Status", 0),
                        ("/devices/DataAnalyzeModule/controls/TempRegulator3Status", 0),
                        ("/devices/DataAnalyzeModule/controls/ThermoHeaterTimeError", 0),
                        ("/devices/wb-mwac_123/controls/K1", 0),
                        ("/devices/wb-mwac_123/controls/K2", 0)
                        ]

mqtt_topics_data_analyze_module = {
    "input_water_leak_last_seen": "/devices/0xa4c138da7c2d6d15/controls/last_seen",
    "input_temp_sens1_last_seen": "/devices/0x00158d00091c5add/controls/last_seen",
    "input_temp_sens2_last_seen": "/devices/0x00158d0009753163/controls/last_seen",
    "input_thermo_heater_last_seen": "/devices/0x50325ffffe033772/controls/last_seen",
    "input_temp_sens1_value": "/devices/0x00158d00091c5add/controls/temperature",
    "input_temp_sens2_value": "/devices/0x00158d0009753163/controls/temperature",
    "input_electro_heater1_setpoint_value": "/devices/ElectrolHeaterModule/controls/Heater1 Setpoint",
    "input_water_heater1_setpoint_value": "/devices/0x50325ffffe033772/controls/current_heating_setpoint",
    "input_water_leak": "/devices/0xa4c138da7c2d6d15/controls/water_leak",
    "input_outlet_group1_state": "/devices/wb-mr3_147/controls/K1",
    "input_outlet_group2_state": "/devices/wb-mr3_147/controls/K2",
    "input_outlet_group3_state": "/devices/wb-mr3_147/controls/K3",
    "input_light1_state": "/devices/wb-led_66/controls/Channel 1",
    "input_light2_state": "/devices/wb-led_66/controls/Channel 2",
    "input_light3_state": "/devices/wb-led_66/controls/Channel 3",
    "input_light4_state": "/devices/wb-led_66/controls/Channel 4",
    "output_water_leak_time_error": "/devices/DataAnalyzeModule/controls/LeakSensorTimeError",
    "output_temp_sens1_time_error": "/devices/DataAnalyzeModule/controls/Temp1SensorTimeError",
    "output_temp_sens2_time_error": "/devices/DataAnalyzeModule/controls/Temp2SensorTimeError",
    "output_thermo_heater_time_error": "/devices/DataAnalyzeModule/controls/ThermoHeaterTimeError",
    "output_outlets_global_state": "/devices/DataAnalyzeModule/controls/OutletsGlobalState",
    "output_light_global_state": "/devices/DataAnalyzeModule/controls/LightGlobalState",
    "output_leak_sens_last_time": "/devices/DataAnalyzeModule/controls/LeakSensorLastTime (minutes)",
    "output_temp1_sens_last_time": "/devices/DataAnalyzeModule/controls/Temp1SensorLastTime (minutes)",
    "output_temp2_sens_last_time": "/devices/DataAnalyzeModule/controls/Temp2SensorLastTime (minutes)",
    "output_thermo_heater_last_time": "/devices/DataAnalyzeModule/controls/ThermoHeaterLastTime (minutes)",
    "output_temp_regulator1_status": "/devices/DataAnalyzeModule/controls/TempRegulator1Status",
    "output_temp_regulator3_status": "/devices/DataAnalyzeModule/controls/TempRegulator3Status",
    "output_water_tape1_state": "/devices/wb-mwac_123/controls/K1/on",
    "output_water_tape2_state": "/devices/wb-mwac_123/controls/K2/on",
    "output_water_alarm": "/devices/wb-mwac_123/controls/Alarm/on",
}