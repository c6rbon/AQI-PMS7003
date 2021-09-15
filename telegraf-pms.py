from pms7003 import Pms7003Sensor, PmsSensorException
import argparse
import logging


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='--device: serial device')
    parser.add_argument('--device', default='/dev/serial0',
                    help='serial device to read from e.g. /dev/serial0')
    args = parser.parse_args()
    
    sensor = Pms7003Sensor(args.device)

    while True:
        try:
            data = sensor.read()
            for field in data:
                print('aqi_sensor ', field, '=', data[field], sep='')
        except PmsSensorException:
            logging.error('Connection problem')

    sensor.close()
