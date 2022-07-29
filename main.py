
from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
import os
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import time
import pyautogui
from datetime import datetime

# chromedriver_autoinstaller.install()
option = webdriver.ChromeOptions()
option.add_argument('--save-page-as-mhtml')
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_experimental_option("useAutomationExtension", False)
option.add_experimental_option("excludeSwitches", ["enable-automation"])

option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
SEQUENCE = r"offline_webpage_infor_pages/page_source"
driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=option)

popular_investors = ["rallek", "miyoshi", "reinhardtcoetzee", "sharonconnolly", "cphequities", "rubymza", "richardstroud", "ingruc", "pino428", "triangulacapital", "jordenboer", "slow_and_steady", "monabel", "emge2116", "doopiecash", "magic_kaito", "ioatri",
       "balticseal", "daniel4653", "fifty-five", "calintrading", "sgstjc", "greatcompanies", "karlo_s", "lukaszkisicki", "trojaneto", "chiay0327", "carlos_delarosa", "trex8u247", "estebanopatril", "nintingale", "taherkamari", "zofesu",
      "andreamarcon16", "nestorarmstrong", "bhavesh_spx", "theosanders", "dividends_income", "andresvicunat", "tomwintjes", "nicoroumeau", "mjtfernandez", "myhungetoro", "maxdividend", "victorvatin",
      "aguero1010", "ilakha", "beatthemarketz", "acetoandrea", "jacksmann", "renoi974", "tomchapman1979", "axisnet", "imbolex", "thinhleduc", "jianswang", "marianopardo", "wesl3y", "hyjbrighter", "misterg23", "ligkclaw",
      "alexandrucinca", "rubymza", "jaynemesis", "gserdan", "tradefx525", "eddyb123", "returninvest", "matanspalatrin1", "lee88eng", "bamboo108", "liborvasa", "jeppekirkbonde", "liamdavies", "arash007", "canzhao", "knw500",
      "thibautr", "fundmanagerzech", "sashok281", "alnayef", "campervans", "pizarrosaul", "sandra31168", "social-investor", "prototypevr", "harryh1993", "vidovm", "meldow", "robertunger", "sparkliang", "abbroush",
      "abeershahid", "coolcontribution", "chocowin", "vladd35", "aukie2008", "noasnoas", "b--art", "simonneau"]

positions = ["msft", "goog"]

popular_investors = ["gserdan"]

datetime_now = datetime.today().strftime('%m-%d-%Y-h%H')
directory = r"offline_webpage_portfolio_pages/" + datetime_now
if not os.path.exists(directory):
      os.makedirs(directory)

number_of_record = 0
final_profile = ""
fail_pages = ""
name_check = ""
rank_check = ""

print("Begin crawling: " + str(len(popular_investors)))
for pi in popular_investors:
      for position in positions:
            time.sleep(2)
            try:
                  driver.get("https://www.etoro.com/people/" + pi + "/portfolio/" + position)
                  time.sleep(1)
            except WebDriverException as e:
                  print("No page: " + pi + " is not found")
                  print("Error: " + str(e))
                  fail_pages += pi + ", "
                  continue

            time.sleep(2)
            final_profile = pi
            with open(directory + "/" + pi + "_" + position + ".html", "w", encoding='utf-8') as f:
                  try:
                        f.write(driver.page_source)
                  except WebDriverException as e:
                        print("Cant save " + pi + ".html file")
                        print("Error: " + str(e))
                        fail_pages += pi + ", "

            try:
                  name_check = driver.find_element(By.XPATH, "//h1[@automation-id='user-head-not-nickname']").text
            except NoSuchElementException:
                  name_check = ""

            try:
                  ticket = driver.find_element(By.XPATH, "//p[@automation-id='cd-public-portfolio-breakdown-header-name']").text
            except NoSuchElementException:
                  ticket = ""

            print("name_check: " + name_check)
            print("ticket: " + ticket)

            if len(name_check) != "" and len(ticket) != "":
                  number_of_record += 1
            else:
                  fail_pages += pi + ", "
                  print("failed crawl: " + pi)



print("Report: \n" +
      "Crawled: " + str(number_of_record) + "/" + str(len(popular_investors)) + "\n" +
      "Success Rate: " + str(number_of_record*100/len(popular_investors)) + "\n" +
      "Failed pages: " + fail_pages + "\n" +
      "Stop at: " + final_profile)