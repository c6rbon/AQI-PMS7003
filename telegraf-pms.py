import argparse
import json
import logging
from pms7003 import Pms7003Sensor, PmsSensorException

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='--device: serial device')
    parser.add_argument('--device', default='/dev/serial0',
                    help='serial device to read from e.g. /dev/serial0')
    parser.add_argument('--json_out', default='/var/www/html/t/current.json',
                    help='output file for latest values')
    args = parser.parse_args()
    
    sensor = Pms7003Sensor(args.device)
    json_file = args.json_out

    while True:
        try:
            data = sensor.read()
            for field in data:
                print('aqi_sensor ', field, '=', data[field], sep='')
            with open(json_file, 'w') as outfile:
                json.dump(data, outfile)
        except PmsSensorException:
            logging.error('Connection problem')

    sensor.close()
