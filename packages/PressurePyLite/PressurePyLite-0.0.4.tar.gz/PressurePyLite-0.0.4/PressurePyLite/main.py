from PressurePyLite.ardu import Arduino

import argparse
import time


def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--sensor", required=False,
                    help="change the port of the sensor arduino")
    ap.add_argument("-p", "--pump", required=False,
                    help="change the port of the pump arduino")
    ap.add_argument("-t", "--target_pressure", required=False,
                    help="change the pressure")
    args = vars(ap.parse_args())

    if args["sensor"] is None:
        sensor = "/dev/ttyUSB0"
    else:
        sensor = args["sensor"]
    if args["pump"] is None:
        pump = "/dev/ttyACM0"
    else:
        pump = args["pump"]
    if args["target_pressure"] is None:
        target_pressure = 120
    else:
        target_pressure = args["target_pressure"]

    ardu = Arduino(sensor, pump, target_pressure)

    while True:
        p, t = ardu.read_port()
        print(p)
        ardu.pump_connect(p, "go")
        time.sleep(0.2)


if __name__ == "__main__":
    main()
