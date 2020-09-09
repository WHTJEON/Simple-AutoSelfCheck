#!/usr/local/bin/python3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException
# from selenium.common.exceptions import StaleElementReferenceException
import time
import sys
import os
from datetime import datetime
import json
from webdriver_manager.chrome import ChromeDriverManager


now=datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
date_title = now.strftime("%Y%m%d %H:%M")
date_string = now.strftime("%Y년 %m월 %d일")

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    running_mode = 'Frozen/executable'
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive"
    except NameError:
        application_path = os.getcwd()
        running_mode = 'Interactive'

chromedriver_path = os.path.join(application_path, "chromedriver")
user_data_path = os.path.join(application_path, "user_data.json")

# Selenium ChromeDriver 기본 설정
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1080x1080')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

# for console logging
os.system('clear')

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def selfcheck (city,school_level,school_name,name,birthdate,password):
    print("%s님 %s자 건강 자가진단을 시작합니다."%(name,date_string))

    print("\nChrome Driver 로드 중.. (약 5~10초 정도 소요)")

    start_time=time.time()
    chromedriver_path = os.path.join(os.path.dirname(__file__),"chromedriver")
    #driver = webdriver.Chrome(chromedriver_path,options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.implicitly_wait(6)

    driver.get("https://hcs.eduro.go.kr/#/loginHome")
    time.sleep(2)

    try:
        driver.find_element_by_class_name("closeBtn").click()
    except:
        pass

    driver.find_element_by_id("btnConfirm2").click()

    print("\n로그인 정보 처리 중..")

    driver.find_element_by_css_selector("[title ='학교 입력']").click()
    select_city= Select (driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[2]/div[1]/table/tbody/tr[1]/td/select"))
    select_city.select_by_value(city)
    select_school_level= Select (driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[2]/div[1]/table/tbody/tr[2]/td/select"))
    select_school_level.select_by_value(school_level)
    driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[2]/div[1]/table/tbody/tr[3]/td[1]/input").send_keys(school_name)
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[2]/div[1]/table/tbody/tr[3]/td[1]/input").send_keys(Keys.RETURN)
    time.sleep(1)

    driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[2]/div[1]/ul/li/p/a/em").click()
    driver.find_element_by_class_name("layerFullBtn").click()
    driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/div/div/div[1]/table/tbody/tr[2]/td/input").send_keys(name)
    driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/div/div/div[1]/table/tbody/tr[3]/td/input").send_keys(birthdate)
    driver.find_element_by_id("btnConfirm").click()

    time.sleep(1)

    pw_input = driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/div/div/div[1]/table/tbody/tr/td/input")
    pw_input.send_keys(password)
    driver.find_element_by_id("btnConfirm").click()

    print("\n로그인 완료.")

    time.sleep(1)

    print("\n금일 자가진단 진행 여부 확인중..")

    status = driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/section[2]/div[2]/ul/li/a/button").get_attribute("innerText")

    if status == "미참여":
        print("\n건강 자가진단 진행중..")
        driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/section[2]/div[2]/ul/li/a/button").click()
        driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/div/div[2]/div[2]/dl[1]/dd/ul/li[1]/label").click()
        driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/div/div[2]/div[2]/dl[2]/dd/ul/li[1]/label").click()
        driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/div/div[2]/div[2]/dl[3]/dd/ul/li[1]/label").click()
        driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/div/div[2]/div[2]/dl[4]/dd/ul/li[1]/label").click()
        driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/div/div[2]/div[2]/dl[5]/dd/ul/li[1]/label").click()
        driver.find_element_by_id("btnConfirm").click()
        time.sleep(1)
        print("\n%s자 자가진단을 완료했습니다."%date_string)

    else:
        lastly_checked = driver.find_element_by_xpath("/html/body/app-root/div/div[1]/div/div[2]/section[2]/div[2]/ul/li/a/span[2]").get_attribute("innerText")
        print("\n오늘은 이미 %s에 자가진단에 참여하셨습니다. (%s)"%(lastly_checked,status))

    end_time=time.time()
    time_elapsed=round(end_time-start_time,2)
    print("\n자가진단 프로세스를 종료합니다. (%s초 소요)\n"%time_elapsed)

    driver.quit()


with open(user_data_path, 'r') as json_file:
    json_data = json.load(json_file)
    selfcheck (json_data["city"],json_data["school_level"],json_data["school_name"],json_data["name"],json_data["birthdate"],json_data["password"])
