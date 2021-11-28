from selenium import webdriver #connect python with webbrowser-chrome
from selenium.webdriver.common.keys import Keys

def main():
 #launch url
 url = “http://linkedin.com/"
 nurl = “http://linkedin.com/mynetwork/"
driver = webdriver.Chrome('C:\\Users\\hp\\Desktop\\chromedriver.exe')
driver.get(url)