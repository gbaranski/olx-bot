from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver= webdriver.Firefox()

driver.get('http://calculator.gbaranski.com')

fl_size = driver.find_element_by_id("FLsize")
fl_size.send_keys('10')

dl_speed = driver.find_element_by_id("DLspeed")
dl_speed.send_keys('10')

result = driver.find_element_by_id("resultTime").text
print(result)