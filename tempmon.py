import argparse
import time
import Adafruit_DHT
import sys
import requests
import json

api_address = ""

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4


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
    return requests.request(method="GET", url=full_address)


def main():
    global api_address

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
    if not sleep_interval:
        sleep_interval = 0

    print("Params from mother ship: {}".format(json.dumps(data, indent=2)))

    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN, delay_seconds=sleep_interval)
        temperature_f = temperature * (9 / 5) + 32

        if humidity is not None and temperature is not None:
            print("Temp={:0.2f}C ({:0.2f}F) Humidity={:0.2f}%".format(temperature, temperature_f, humidity))
            send_data(sensor_id, temperature_f, humidity)
        else:
            print("Failed to retrieve data from humidity sensor")

        time.sleep(sleep_interval)


if __name__ == "__main__":
    main()
    sys.exit(0)
