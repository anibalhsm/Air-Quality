import datetime as dt

from requests import RequestException

from app.api_wrappers.plume_wrapper import PlumeWrapper
from app.daos.plume_dao import PlumeDAO
from app.models.plume_platform import PlumePlatform


class PlumeService:
    def __init__(self, dao: PlumeDAO):
        self.plume_api = PlumeWrapper.env_factory()
        self.dao = dao

    def get_platforms(self):
        try:
            sensors = {sensor["device_id"]: sensor for sensor in
                       self.plume_api.request_json_sensors(timeout=5)["sensors"]}
        except RequestException:
            sensors = dict()

        for platform in self.dao.get_platforms():
            # determine sync status
            sensor = sensors.get(platform.serial_number)
            if sensor is not None:
                if sensor.get("last_sync") is None:
                    platform.sync_status = "un-synced"
                else:
                    platform.sync_status = dt.datetime.fromtimestamp(sensor["last_sync"]).strftime("%d/%m/%Y")
            yield platform.__dict__

    def get_platform(self, platform_id: int):
        return self.dao.get_platform(platform_id)

    def add_platform(self, platform):
        self.dao.add_platform(platform)

    def modify_platform(self, platform: PlumePlatform):
        self.dao.update_platform(platform)

    def delete_platform(self, platform_id: int):
        self.dao.delete_platform(platform_id)
