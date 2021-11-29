from selenium import webdriver
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import urllib.parse

import random
import getpass
import datetime

import numpy

options = Options()
options.add_argument(f"--user-data-dir=C:/Users/{getpass.getuser()}/AppData/Local/Google/Chrome/User Data/Default")
options.add_argument("--profile-directory=Default")
options.headless = False
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu/')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("--log-level=3")
options.add_argument('--hide-scrollbars')
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_experimental_option("useAutomationExtension",False)


driver = webdriver.Chrome(executable_path='./chromedriver.exe',options = options)


 #launch url
url = "http://linkedin.com/"

messages = ["""Merci de m’avoir accepté dans votre réseau ...
Je suis un Élève ingénieur je cherche une opportunité de stage""",
"""Hi, thank you for accepting me into your network, 
I'm looking for an end-of-study internship, 
I had learned many essential skills with a good experience that will assist me in the internship.
If you allow me to send you my CV."""]

limite = 20

search_words = "production manager"

driver.get(url)
try:
    email = driver.find_element_by_id("session_key")
    password = driver.find_element_by_id("session_password")
    submit   = driver.find_element_by_css_selector("button.sign-in-form__submit-button")

    #Empty fields if there are empty
    email.send_keys(Keys.CONTROL, 'a')
    email.send_keys(Keys.DELETE)
    password.send_keys(Keys.CONTROL, 'a')
    password.send_keys(Keys.DELETE)

    time.sleep(3)

    email.send_keys("youremail@email.com")
    password.send_keys("YOUR_PASSWORD")
    time.sleep(3)
    submit.click()
except:
    println('Already logged in')
    pass

time.sleep(4)

words = urllib.parse.quote(search_words)

suc_count = 0

def println(*args,**kwargs):
    now = datetime.datetime.now()
    logT = f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] : '
    print(logT,*args,**kwargs)


def sendToPpls(persons):
    global suc_count
    dle = False
    minn, maxx = 10 , 20
    for person in persons:
        try:
            time.sleep(random.randint(minn, maxx))
            try:
                connect = person.find_element_by_css_selector('.artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view.artdeco-button--muted')
                minn, maxx = 2 , 5
                println("en attente")
                continue
            except:
                connect = person.find_element_by_css_selector('.artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view')
                text = connect.find_element_by_css_selector('span').text
                if(text == "Message"):
                    minn, maxx = 1 , 2
                    println('Already connected')
                    continue
                minn, maxx = 10 , 20
                suc_count = suc_count + 1
            name = person.find_element_by_css_selector('.entity-result__title-line a>span>span').text
            println(f"Num : {suc_count}, Sending to {name}")
            connect.click()
            time.sleep(2)
            addnote = driver.find_element_by_css_selector('.mr1.artdeco-button.artdeco-button--muted.artdeco-button--2.artdeco-button--secondary.ember-view')
            addnote.click()
            time.sleep(2)
            text = driver.find_element_by_css_selector('[name="message"]')
            message = random.choice(messages)
            text.send_keys(message)
            time.sleep(2)
            send = driver.find_element_by_css_selector('.ml1.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view')
            send.click()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message)
            pass
    if suc_count > limite:
        suc_count = 0
        dle = True
    nextPage(dle) 
      

def people_page(driver):  ##coords and dimensions to scroll through page
    container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    containerLoc = container.location
    containerSize = container.size
    startY = containerLoc["y"]
    height = containerSize["height"]

    return startY, height

counter = 0
def nextPage(dle=False):
    if dle == True:
        one_hour = 3600
        delay_time = one_hour*random.randint(2, 8)/10
        time.sleep(delay_time)
    global counter 
    counter = counter + 1
    query = f"https://www.linkedin.com/search/results/people/?keywords={words}&page={counter}&origin=CLUSTER_EXPANSION"
    driver.get(query)

    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'"))
    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    # time.sleep(3)
    startY, height = people_page(driver)
    step = (height - startY)*0.01
    for l in numpy.arange(startY, height, step): ##slow scroll through product page
        driver.execute_script("window.scrollTo(0, {});".format(l))
    time.sleep(3)
    persons = driver.find_elements_by_css_selector('.reusable-search__result-container')
    time.sleep(random.randint(5, 10))
    sendToPpls(persons)

nextPage()

