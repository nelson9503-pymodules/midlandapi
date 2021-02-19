import chromedriver_autoinstaller
from selenium import webdriver

class TokenManager:

    def __init__(self):
        pass

    def get_token(self) -> str:
        driver_path = chromedriver_autoinstaller.install(cwd=True)
        chrome = webdriver.Chrome(driver_path)
        url = "https://www.midland.com.hk/zh-hk/list/estate"
        chrome.get(url)
        token = chrome.get_cookie("token")["value"]
        chrome.close()
        return token
