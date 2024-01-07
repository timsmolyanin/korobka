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
                        ("/devices/DataAnalyzeModule/controls/LeakSensorStatus", 0),
                        ("/devices/DataAnalyzeModule/controls/Temp1Status", 0),
                        ("/devices/DataAnalyzeModule/controls/Temp2Status", 0),
                        ("/devices/DataAnalyzeModule/controls/ThermoHeaterStatus", 0),
                        ("/devices/DataAnalyzeModule/controls/TemperatureGlobaErrorlFlag", 0),
                        ("/devices/DataAnalyzeModule/controls/WaterGlobaErrorlFlag", 0),
                        ("/devices/0x50325ffffe033772/controls/current_heating_setpoint", 0),
                        ("/devices/ElectroHeaterModule/controls/Heater1 Setpoint", 0),
                        ("/devices/wb-mwac_123/controls/K1", 0),
                        ("/devices/wb-mwac_123/controls/K2", 0),
                        ("/devices/DataAnalyzeModule/controls/Temp1BatteryStatus", 0),
                        ("/devices/DataAnalyzeModule/controls/Temp2BatteryStatus", 0),
                        ("/devices/DataAnalyzeModule/controls/ThermoHeaterBatteryStatus", 0),
                        ("/devices/DataAnalyzeModule/controls/WaterTap1Status", 0),
                        ("/devices/DataAnalyzeModule/controls/WaterTap2Status", 0)
                        ]

mqtt_topics_data_analyze_module = {
    "input_water_leak_last_seen": "/devices/0xa4c138da7c2d6d15/controls/last_seen",
    "input_temp_sens1_last_seen": "/devices/0x00158d00091c5add/controls/last_seen",
    "input_temp_sens2_last_seen": "/devices/0x00158d0009753163/controls/last_seen",
    "input_thermo_heater_last_seen": "/devices/0x50325ffffe033772/controls/last_seen",
    "input_water_leak_battery": "/devices/0xa4c138da7c2d6d15/controls/battery",
    "input_temp1_battery": "/devices/0x00158d00091c5add/controls/battery",
    "input_temp2_battery": "/devices/0x00158d0009753163/controls/battery",
    "input_thermo_heater_battery": "/devices/0x50325ffffe033772/controls/battery_low",
    "input_temp_sens1_value": "/devices/0x00158d00091c5add/controls/temperature",
    "input_temp_sens2_value": "/devices/0x00158d0009753163/controls/temperature",
    "input_water_heater1_setpoint_value": "/devices/0x50325ffffe033772/controls/current_heating_setpoint",
    "input_water_leak": "/devices/0xa4c138da7c2d6d15/controls/water_leak",
    "input_outlet_group1_state": "/devices/wb-mr3_147/controls/K1",
    "input_outlet_group2_state": "/devices/wb-mr3_147/controls/K2",
    "input_outlet_group3_state": "/devices/wb-mr3_147/controls/K3",
    "input_light1_state": "/devices/wb-led_66/controls/Channel 1",
    "input_light2_state": "/devices/wb-led_66/controls/Channel 2",
    "input_light3_state": "/devices/wb-led_66/controls/Channel 3",
    "input_temp_sens_norm_time": "/devices/DataAnalyzeModule/controls/TempSenNormTime",
    "input_water_sens_norm_time": "/devices/DataAnalyzeModule/controls/WaterLeakSenNormTime",
    "input_thermo_heat_norm_time": "/devices/DataAnalyzeModule/controls/ThermoHeatNormTime",
    "input_cold_water_tap": "/devices/DataAnalyzeModule/controls/ColdWaterTap",
    "input_hot_water_tap": "/devices/DataAnalyzeModule/controls/HotWaterTap",
    "input_water_tape1_status": "/devices/DataAnalyzeModule/controls/WaterTap1Status",
    "input_water_tape2_status": "/devices/DataAnalyzeModule/controls/WaterTap2Status",
    "output_water_tape1_state": "/devices/wb-mwac_123/controls/K1/on",
    "output_water_tape2_state": "/devices/wb-mwac_123/controls/K2/on",
    "output_water_tape1_status": "/devices/DataAnalyzeModule/controls/WaterTap1Status",
    "output_water_tape2_status": "/devices/DataAnalyzeModule/controls/WaterTap2Status",
    "output_water_alarm": "/devices/wb-mwac_123/controls/Alarm/on",
    "output_water_leak_status": "/devices/DataAnalyzeModule/controls/LeakSensorStatus",
    "output_temp1_status": "/devices/DataAnalyzeModule/controls/Temp1Status",
    "output_temp2_status": "/devices/DataAnalyzeModule/controls/Temp2Status",
    "output_thermo_heater_status": "/devices/DataAnalyzeModule/controls/ThermoHeaterStatus",
    "output_temp_global_error": "/devices/DataAnalyzeModule/controls/TemperatureGlobaErrorlFlag",
    "output_water_global_error": "/devices/DataAnalyzeModule/controls/WaterGlobaErrorlFlag",
    "output_outlets_global_state": "/devices/DataAnalyzeModule/controls/OutletsGlobalState",
    "output_light_global_state": "/devices/DataAnalyzeModule/controls/LightGlobalState",
    "output_leak_sens_last_time": "/devices/DataAnalyzeModule/controls/LeakSensorLastTime (minutes)",
    "output_temp1_sens_last_time": "/devices/DataAnalyzeModule/controls/Temp1SensorLastTime (minutes)",
    "output_temp2_sens_last_time": "/devices/DataAnalyzeModule/controls/Temp2SensorLastTime (minutes)",
    "output_thermo_heater_last_time": "/devices/DataAnalyzeModule/controls/ThermoHeaterLastTime (minutes)",
    "output_temp1_battery_status": "/devices/DataAnalyzeModule/controls/Temp1BatteryStatus",
    "output_temp2_battery_status": "/devices/DataAnalyzeModule/controls/Temp2BatteryStatus",
    "output_thermo_heater_battery_status": "/devices/DataAnalyzeModule/controls/ThermoHeaterBatteryStatus",
    "input_electro_heater1_setpoint_value": "/devices/ElectroHeaterModule/controls/Heater1 Setpoint",
}

mqtt_topics_system_module = {
    "input_wifi_state": "/devices/SystemModule/controls/WiFi State",
    "input_wifi_client_ssid": "/devices/SystemModule/controls/WiFi Client SSID",
    "input_wifi_client_password": "/devices/SystemModule/controls/WiFi Client Password",
    "input_eth_mode": "/devices/SystemModule/controls/ETH Mode",
    "input_eth_ip": "/devices/SystemModule/controls/ETH IP",
    "input_eth_mask": "/devices/SystemModule/controls/ETH Mask",
    "input_eth_gateway": "/devices/SystemModule/controls/ETH Gateway",
}