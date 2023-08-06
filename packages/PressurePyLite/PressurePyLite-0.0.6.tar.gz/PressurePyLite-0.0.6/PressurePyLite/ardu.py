import serial
import time


class Arduino:
    """ ardu = Arduino("/dev/cu.usbserial-2320", "/dev/cu.usbmodem23301") """

    sensor: serial
    pump: serial
    target_pressure: float
    experiment_started: bool
    counter: int

    def __init__(self, sensor_port, pump_port, target_pressure):
        """ Set the Ports and logs the files """

        self.sensor = serial.Serial(sensor_port, '9600')
        self.pump = serial.Serial(pump_port, '9600')
        self.target_pressure = target_pressure
        self.experiment_started = False
        self.counter = 0

    def read_port(self):
        # make sure to read the last line sent
        bytes_ = self.sensor.readlines(1)[-1]
        while self.sensor.inWaiting() > 0:
            time.sleep(0.05)
            bytes_ = self.sensor.readlines(1)[-1]
            time.sleep(0.05)

        # convert bytes to string
        str_rn = bytes_.decode()
        str_ = str_rn.rstrip()
        split = str_.split('/')

        # the format is: "pressure/temperature"
        return float(split[0]), float(split[1])


    def pump_connect(self, pressure, status):
        self.pump.write(bytes(str(pressure) + '/' + str(self.target_pressure) + '/' + str(status) + '/\n', 'utf-8'))
