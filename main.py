import serial_port
import mqtt_communication


def test_cb(data):
    tmp = data.split(".")
    wb_dev = None
    mqtt_ch = None
    val = None
    if tmp[0] == "electric":
        wb_dev = "outletcontrol_34"
    mqtt_ch = tmp[1]
    val = int(tmp[2])

    mqtt_communication.wb_mqtt_switch(wb_dev, mqtt_ch, val)


def main():
    s = serial_port.SerialPort("COM3", 115200, test_cb)
    s.start()


if __name__ == "__main__":
    main()
