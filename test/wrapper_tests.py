import datetime
import os

from app.api_wrappers.plume_wrapper import PlumeWrapper
from app.api_wrappers.sensor_community_wrapper import SCWrapper
from app.api_wrappers.zephyr_wrapper import ZephyrWrapper

ZEPHYR_USERNAME = os.environ.get("ZEPHYR_USERNAME")
ZEPHYR_PASSWORD = os.environ.get("ZEPHYR_PASSWORD")

SC_USERNAME = os.environ.get("SC_USERNAME")
SC_PASSWORD = os.environ.get("SC_PASSWORD")

PLUME_EMAIL = os.environ.get("PLUME_EMAIL")
PLUME_PASSWORD = os.environ.get("PLUME_PASSWORD")


def zephyr_test():
    zw = ZephyrWrapper(ZEPHYR_USERNAME, ZEPHYR_PASSWORD)
    sensors = zw.get_sensors(start=datetime.datetime(2021, 9, 19),
                             end=datetime.datetime(2021, 9, 20),
                             sensors=zw.get_sensor_ids(),
                             slot="B")
    for sensor in sensors:
        print(sensor.id)
        print(sensor.dataframe)


def sensor_community_test():
    scw = SCWrapper(SC_USERNAME, SC_PASSWORD)
    sensors = scw.get_sensors(end=datetime.datetime.today() - datetime.timedelta(days=1),
                              start=datetime.datetime(2021, 10, 18),
                              sensors={'66007': 'SDS011', '66008': 'SHT31'})
    for sensor in sensors:
        print(sensor.id)
        print(sensor.dataframe)


def plume_test(start, end):
    pw = PlumeWrapper(PLUME_EMAIL, PLUME_PASSWORD, 85)
    sensors = pw.get_sensors(start=start, end=end, sensors=pw.get_sensor_ids(), timeout=120)
    for sensor in sensors:
        print(sensor.id)
        print(sensor.dataframe)


if __name__ == '__main__':
    pw = PlumeWrapper(PLUME_EMAIL, PLUME_PASSWORD, 85)
    print(pw.convert_serial_number_to_platform_id(()))

    # sensor_community_test()
    # zephyr_test()
    # plume_test(datetime.datetime.now() - datetime.timedelta(2), datetime.datetime.now() - datetime.timedelta(1))
    # plume_test(datetime.datetime(2021, 1, 1), datetime.datetime(2022, 1, 1))
