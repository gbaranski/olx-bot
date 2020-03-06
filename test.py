from selenium import webdriver
from undetected_chromedriver import Chrome, ChromeOptions
driver = webdriver.Firefox()

driver.get("https://www.olx.pl/pomorskie/q-macbook/")
offername = driver.find_elements_by_xpath("//a[contains(@class, 'marginright5') and contains(@class, 'link') and contains(@class, 'linkWithHash') and contains(@class, 'detailsLink')]")
for link in offername:
    print(link.text)

