import serial_port


def test_cb(data):
    print(data)
    decode_data = data.decode('Ascii')
    print(decode_data.split("."))


def main():
    s = serial_port.SerialPort("COM3", 115200, test_cb)
    s.start()


if __name__ == "__main__":
    main()
