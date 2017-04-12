import time
from datetime import datetime
from itertools import islice

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

driver = webdriver.Chrome("/usr/local/share/chromedriver")
driver.get("http://www.youtube.com")
assert "YouTube" in driver.title


# import csv

def collectTranscript (url):
    try:
        browser = webdriver.Chrome("/usr/local/share/chromedriver")
        browser.get(url)
        element = browser.find_element_by_id('action-panel-overflow-button')
        element.click()
        element = browser.find_element_by_css_selector('button.action-panel-trigger-transcript')
        element.click()
        finalText = BeautifulSoup(browser.page_source)
        print finalText
        temp = ''
        for text in finalText.find_all('div', {'class': 'caption-line-text'}):
            if text is None or (len(text) == 0):
                temp = temp + '\n'
            else:
                temp = temp + text.string + '\n'
        browser.quit()
        return temp
    except:
        pass
        browser.quit()
        # print("No transcripts found for video - " + url)
        # browser.quit()


j = 0
n = 2
search = "//input[@id='masthead-search-term']"
searchButton = "//button[@id='search-btn']"
filterButton = "//span[contains(text(),'Filters')]"
nextButton = "//span[contains(text(),'Next')]"
# shortButton = "//span[contains(text(),'Short (< 4 minutes)')]"
videoHead = 'a.yt-uix-tile-link'
pageHead = 'span.yt-uix-button-content'

with open("Queries.csv", "r+") as QObject:
    for l in QObject:
        print l
        textFieldElement = WebDriverWait(driver, 10).until(lambda driver1: driver.find_element_by_xpath(search))
        textFieldElement.clear()
        #time.sleep(2)
        textFieldElement.send_keys(l)
        searchButtonElement = WebDriverWait(driver, 10).until(
            lambda driver1: driver.find_element_by_xpath(searchButton))
        searchButtonElement.click()
        time.sleep(2)
        # filterButtonElement = WebDriverWait(driver, 20).until(lambda driver1: driver.find_element_by_xpath(filterButton))
        # filterButtonElement.click()
        # time.sleep(2)
        # shortButtonElement = WebDriverWait(driver, 20).until(lambda driver1: driver.find_element_by_xpath(shortButton))
        # shortButtonElement.click()
        # time.sleep(1)
        # for j in range(1,20):
        for j in range(0, 2):
            headElement = WebDriverWait(driver, 5).until(
                lambda driver1: driver.find_elements_by_css_selector(videoHead))
            with open("friends.csv", "w") as f:
                for i in range(1, n+1):
                    string = str(((n - 1) * j) + i) + "," + str(datetime.now()) + "," + headElement[i].get_attribute(
                        "href") + "," + headElement[i].get_attribute("title") + "\n"
                    f.write(string)
            with open("friends.csv", "r+") as fObject:
                with open("dataset.csv", "a") as f2:
                    lines = islice(fObject, n)
                    for line in lines:
                        # print(line)
                        columns = line.split(",")
                        # print(columns[2])
                        trans = collectTranscript(columns[2])
                        line = line + "," + str(trans)
                        line = line.replace("\n", " ")
                        line = line + "\n"
                        print(line)
                        f2.write(line)
                        time.sleep(2)
            nextButtonElement = WebDriverWait(driver, 20).until(
                lambda driver1: driver.find_element_by_xpath(nextButton))
            nextButtonElement.click()
            time.sleep(5)

driver.quit()


