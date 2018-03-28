from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import traceback


class jis_code():

    def __init__(self):
        self.JISURL = "http://www.jisc.go.jp/app/jis/general/GnrJISSearch.html"

    # Chromeのセッチング
    def chrome(self, driverPath):
        option = Options()
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(
            executable_path=driverPath, chrome_options=option)

    def getJIS(self, code):
        self.driver.get(self.JISURL)
        self.driver.implicitly_wait(1)

        self.jisPage = jisPages(self.driver, code)
        try:
            self.jisPage.inputText("jisStdNo")
            self.jisPage.pushBut("//input[@value='一覧表示']")
            self.jisPage.ckickLink()
            self.jisPage.set_items()
        except:
            # print(traceback.format_exc())
            print("Syntacs Error")

        # シャットダウン
        self.driver.quit()


class jisPages():
    def __init__(self, driver, code):
        self.driver = driver
        self.code = code
        self.items = {}

    # テキストに文字いれて送信
    def inputText(self, searchName):
        try:
            self.driver.find_element_by_name(searchName).send_keys(self.code)
        except:
            print("Theare is not [ " + searchName + "] TextBox in the page")

    # ボタンを押す
    def pushBut(self, valueName):
        try:
            self.driver.find_element_by_xpath(valueName).click()
            self.driver.implicitly_wait(1)
        except:
            print("Theare is not Button has [ " + valueName + " ] in the page")

    # リンクをクリックする。
    def ckickLink(self):
        try:
            self.driver.find_element_by_link_text("JIS"+self.code).click()
            self.driver.implicitly_wait(1)
        except:
            print("Theare is not Button has [ JIS" + self.code + " ] in the page")

    def set_items(self):
        # 項目を取得
        jisItem = self.driver.find_elements_by_tag_name('th')
        jisValue = self.driver.find_elements_by_tag_name('td')

        for i in range(0, len(jisItem)):
            self.items[jisItem[i].text] = jisValue[i].text


if __name__ == '__main__':
    test = jis_code()
    test.chrome("./chromedriver")
    test.getJIS("G3101")
    print(test.jisPage.items)
