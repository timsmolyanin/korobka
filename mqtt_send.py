import paho.mqtt.publish as publish
import time


def wb_mqtt_switch(mqtt_dev_id: str, mqtt_control: str, val: int):

    try:
        "/devices/outletcontrol_34 /controls/OutletGroup1"
        mqtt_host = "192.168.44.10"
        topic = f"/devices/{mqtt_dev_id}/controls/{mqtt_control}/on"
        publish.single(topic, val, hostname=mqtt_host)
    except Exception as exc:
        print(exc)


def _test_main():
    publish.single("/devices/outletcontrol_34/controls/OutletGroup1/on", 0, hostname="192.168.44.10")
    # wb_mqtt_switch()


if __name__ == "__main__":
    _test_main()
