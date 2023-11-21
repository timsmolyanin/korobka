list_of_mqtt_topics = [("/devices/outletcontrol_34/controls/OutletGroup1", 0),
                        ("/devices/outletcontrol_34/controls/OutletGroup2", 0),
                        ("/devices/outletcontrol_34/controls/OutletGroup3", 0),
                        ("/devices/lightcontrol_145/controls/LightGroup3", 0),
                        ("/devices/lightcontrol_145/controls/LightGroup4", 0),
                        ("/devices/lightcontrol_145/controls/LightGroup5", 0),
                        ("/devices/0xa4c1387ec9c1d434/controls/water_leak", 0),
                        ("/devices/0xa4c1386c14f32cb1/controls/water_leak", 0),
                        ("/devices/network/controls/Ethernet IP", 0),
                        ("/devices/network/controls/Wi-Fi IP", 0),
                        ("/devices/network/controls/Wi-Fi IP Online Status", 0),
                        ("/devices/0x00158d00091c5b60/controls/battery", 0),
                        ("/devices/0x00158d00091c5b60/controls/temperature", 0),
                        ("/devices/0x00158d00091c5aea/controls/battery", 0),
                        ("/devices/0x00158d00091c5aea/controls/temperature", 0),
                        ("/devices/0x84fd27fffe0e709f/controls/current_heating_setpoint", 0),
                        ("/devices/0x84fd27fffe0e709f/controls/battery_low", 0),
                        ("/devices/0x84fd27fffe6d74bb/controls/current_heating_setpoint", 0),
                        ("/devices/0x84fd27fffe6d74bb/controls/battery_low", 0),
                        ("/devices/wb-led_127/controls/Channels 1_2", 0),
                        ("/devices/wb-led_127/controls/Channels 3_4", 0),
                        ("/devices/wb-led_127/controls/Channels 1_2 Brightness", 0),
                        ("/devices/wb-led_127/controls/Channels 3_4 Brightness", 0),
                        ("/devices/WaterConsuming/controls/Hot Last Day Consuming", 0),
                        ("/devices/WaterConsuming/controls/Hot Last Month Consuming", 0),
                        ("/devices/WaterConsuming/controls/Hot Total Consuming", 0),
                        ("/devices/WaterConsuming/controls/Cold Last Day Consuming", 0),
                        ("/devices/WaterConsuming/controls/Cold Last Month Consuming", 0),
                        ("/devices/WaterConsuming/controls/Cold Total Consuming", 0),
                        ("/devices/0x00158d00091c5aea/controls/last_seen", 0),
                        ("/devices/0x84fd27fffe6d74bb/controls/last_seen", 0)
                        ]

mqtt_topics_control_logic = {
    "input_hot_water_leak": "/devices/0xa4c1387ec9c1d434/controls/water_leak",
    "input_cold_water_leak" : "/devices/0xa4c1386c14f32cb1/controls/water_leak",
    "input_cold_water_counter": "/devices/watercontrol_79/controls/P1 Counter",
    "input_hot_water_counter": "/devices/watercontrol_79/controls/P2 Counter",
    "input_sens1_last_seen": "/devices/0x00158d00091c5aea/controls/last_seen",
    "input_sens2_last_seen": "/devices/0x84fd27fffe6d74bb/controls/last_seen",
    "input_wifi_state": "/devices/SystemModule/controls/WiFi State",
    "input_wifi_ssid": "/devices/SystemModule/controls/WiFi SSID",
    "input_wifi_passw": "/devices/SystemModule/controls/WiFi Password",
    "input_eth0_mode": "/devices/SystemModule/controls/Eth0 Mode",
    "input_eth0_ip": "/devices/SystemModule/controls/Eth0 IP 	",
    "input_eth0_mask": "/devices/SystemModule/controls/Eth0 Mask",
    "input_eth0_gateway": "/devices/SystemModule/controls/Eth0 Gateway IP",
}