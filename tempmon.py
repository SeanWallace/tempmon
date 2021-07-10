import argparse
import time
import adafruit_dht
import board
import requests
import json
import signal
import sys

api_address = ""
dht_device = None
DHT_PIN = board.D4


def get_serial_no():
    serial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                serial = line[10:26]
        f.close()
    except:
        serial = "ERROR000000000"

    return serial


def get_api_params():
    return requests.request(method="GET", url=api_address + "?action=get_api_params")


def send_data(sensor_id, temperature, humidity):
    full_address = "{}?action=add_reading&sensor_id={}&degrees_f={}&humidity={}".format(api_address, sensor_id,
                                                                                        temperature, humidity)
    request_result = None
    try:
        request_result = requests.request(method="GET", url=full_address)
    except Exception as e:
        print("Unexpected error sending data:", e)

    return request_result


def main():
    global api_address, dht_device

    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default='config/config.json', help="Config file location")
    args = parser.parse_args()

    with open(args.config) as json_data_file:
        config_data = json.load(json_data_file)
        api_address = config_data['api_address']

    if api_address is None or api_address == '':
        print("API address invalid!")
        exit(1)

    print('Using API address: {}'.format(api_address))

    sensor_id = get_serial_no()
    r = get_api_params()
    data = r.json()

    sleep_interval = data['post_frequency']
    if not sleep_interval or sleep_interval == 0:
        # Make sure to have some amount of sleeping always so failures don't run away.
        sleep_interval = 1

    print("Params from mother ship: {}".format(json.dumps(data, indent=2)))

    while True:
        humidity = None
        temperature_c = None
        temperature_f = None

        if dht_device is None:
            dht_device = adafruit_dht.DHT11(DHT_PIN)

        try:
            temperature_c = dht_device.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dht_device.humidity
        except RuntimeError as e:
            print("RuntimeError collecting from sensor: {}".format(e.args[0]))
        except Exception as e:
            dht_device.exit()
            dht_device = None

            print("Unexpected error collecting from sensor: {}".format(e))

        if humidity is not None and temperature_c is not None and temperature_f is not None:
            print("Temp={:0.2f}C ({:0.2f}F) Humidity={:0.2f}%".format(temperature_c, temperature_f, humidity))
            send_data(sensor_id, temperature_f, humidity)

        time.sleep(sleep_interval)


def signal_handler(sig, frame):
    global dht_device

    print('Received signal {}, shutting down...'.format(sig))

    if dht_device is not None:
        dht_device.exit()

    sys.exit(0)


if __name__ == "__main__":
    main()
    sys.exit(0)
