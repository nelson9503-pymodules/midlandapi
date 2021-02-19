from .token_manager import TokenManager
import requests
import json


class UnitExtractor:

    def __init__(self):
        self.token_manager = TokenManager()
        self.token = self.token_manager.get_token()

    def extract(self, building_id: str) -> dict:
        units = self.__get_raw_data(building_id)
        units = self.__extract_all_units(units)
        return units

    def __extract_all_units(self, units: dict) -> dict:
        if "building" in units:
            building = units["building"]
            building_id = building["id"]
            building_name = building["name"]
        else:
            building_id = ""
            building_name = ""
        if "estate" in units:
            estate = units["estate"]
            estate_id = estate["id"]
            estate_name = estate["name"]
        else:
            estate_id = ""
            estate_name = ""
        units = units["data"]
        results = {}
        for unit in units:
            unit_id = unit["unit_id"]
            unit_floor = unit["floor"]
            unit_name = unit["flat_name"]
            unit_build_area = unit["area"]
            unit_real_area = unit["net_area"]
            results[unit_id] = {
                "floor": unit_floor,
                "name": unit_name,
                "build_area": unit_build_area,
                "real_area": unit_real_area,
                "estate_id": estate_id,
                "estate_name": estate_name,
                "building_id": building_id,
                "building_name": building_name
            }
        return results

    def __get_raw_data(self, building_id: str) -> dict:
        url = "https://data.midland.com.hk/listing/v1/transactions/buildings/{}?lang=zh-hk".format(
            building_id)
        while True:
            header = {"authorization": "Bearer {}".format(self.token)}
            r = requests.get(url, headers=header)
            if "Unauthorized" in r.text and "401" in r.text:
                self.token = self.token_manager.get_token()
            else:
                break
        txt = r.text
        txt = json.dumps(txt)
        if txt[0] == '"':
            txt = txt[1:]
        if txt[-1] == '"':
            txt = txt[:-1]
        txt = txt.replace('\\"', '"')
        result = json.loads(txt)
        return result
