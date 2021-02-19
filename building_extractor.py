from .token_manager import TokenManager
import requests
import json


class BuildingExtractor:

    def __init__(self):
        self.token_manager = TokenManager()
        self.token = self.token_manager.get_token()

    def extract(self, estate_id: str) -> dict:
        buildings = self.__get_raw_data(estate_id)
        if buildings == False:
            return {}
        buildings = self.__extract_all_buildings(buildings)
        return buildings

    def __extract_all_buildings(self, buildings: dict) -> dict:
        if "phase" in buildings:
            phases = buildings["phase"]
            results = {}
            for phase in phases:
                phase_id = phase["id"]
                phase_name = phase["name"]
                for building in phase["buildings"]:
                    building_id = building["id"]
                    building_name = building["name"]
                    results[building_id] = {
                        "phase_id": phase_id,
                        "phase_name": phase_name,
                        "building_name": building_name
                    }
        elif "building" in buildings:
            building = buildings["building"]
            building_id = building["id"]
            building_name = building["name"]
            results = {}
            if "phase" in building:
                phase_id = building["estate"]["id"]
                phase_name = building["estate"]["name"]
            else:
                phase_id = ""
                phase_name = ""
            results[building_id] = {
                "phase_id": phase_id,
                "phase_name": phase_name,
                "building_name": building_name
            }
        return results

    def __get_raw_data(self, estate_id: str) -> dict:
        if estate_id[0] == "E":
            url = "https://data.midland.com.hk/listing/v1/transaction/ESTATE/{}/list?lang=zh-hk".format(
                estate_id)
        elif estate_id[0] == "B":
            url = "https://data.midland.com.hk/listing/v1/transactions/buildings/{}?lang=zh-hk".format(
                estate_id)
        elif estate_id[0] == "P":
            url = "https://data.midland.com.hk/listing/v1/transaction/PHASE/{}/list?lang=zh-hk".format(
                estate_id)
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
