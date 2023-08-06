from ardu import Arduino

import argparse


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
        sensor = "/dev/cu.usbserial-2320"
    else:
        sensor = args["sensor"]
    if args["pump"] is None:
        pump = "/dev/cu.usbmodem23301"
    else:
        pump = args["pump"]
    if args["target_pressure"] is None:
        target_pressure = 120
    else:
        target_pressure = args["target_pressure"]

    ardu = Arduino(sensor, pump)

    while True:
        p, t = ardu.read_port()
        ardu.pump_connect(p, target_pressure, "go")


if __name__ == "__main__":
    main()
