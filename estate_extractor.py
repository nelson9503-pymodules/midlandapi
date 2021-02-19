from .token_manager import TokenManager
import requests
import json


class EstateExtractor:

    def __init__(self):
        self.token_manager = TokenManager()
        self.token = self.token_manager.get_token()

    def extract(self) -> dict:
        results = self.__extract_all_estates()
        return results
    
    def __extract_all_estates(self) -> dict:
        total_pages = self.__get_total_page()
        results = {}
        for page in range(1, total_pages+1):
            print("midlandapi: extracting estates...\t{}/{}".format(page, total_pages))
            estates = self.__get_raw_data(page)["result"]
            for estate in estates:
                result = {}
                try:
                    result["id"] = estate["id"]
                except:
                    continue
                try:
                    result["region"] = estate["region"]["name"]
                except:
                    results["region"] = ""
                try:
                    result["subregion"] = estate["subregion"]["name"]
                except:
                    result["subregion"] = ""
                try:
                    result["district"] = estate["district"]["name"]
                except:
                    result["district"] = ""
                try:
                    result["coordinates"] = [estate["location"]
                                             ["lat"], estate["location"]["lon"]]
                except:
                    results["coordinates"] = []
                try:
                    result["developer"] = estate["developer"]["name"]
                except:
                    result["developer"] = ""
                try:
                    result["url"] = estate["url_desc_zh-hk"]
                except:
                    continue
                results[estate["name"]] = result
        return results

    def __get_raw_data(self, page: int) -> dict:
        url = "https://data.midland.com.hk/search/v1/estates?hash=true&lang=zh-hk&currency=HKD&unit=feet&search_behavior=normal&page={}&limit=50".format(
            page)
        while True:
            header = {"authorization": "Bearer {}".format(self.token)}
            r = requests.get(url, headers=header)
            if "Unauthorized" in r.text and "401" in r.text:
                self.token = self.token_manager.get_token()
            elif "502 Bad Gateway" in r.text:
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
    
    def __get_total_page(self) -> int:
        data = self.__get_raw_data(1)
        count = int(data["count"])
        total_pages = count // 50
        if count % 50 > 0:
            total_pages += 1
        return total_pages


