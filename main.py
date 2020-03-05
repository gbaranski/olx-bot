from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
import time
driver = Chrome()

login = "login"
password = "pass"
messageString = "Dzien dobry, testuje aktualnie bota, przepraszam za utrudnienie :)"



def sendMessage(messageUrl):
    driver.get(messageUrl)
    print("Message is sending!")
    messageTextAreaPath = "//*[@id=\"ask-text\"]"
    messageTextArea = driver.find_element_by_xpath(messageTextAreaPath)
    messageTextArea.send_keys(messageString)
    submitButtonPath = "//*[@id=\"contact-form\"]/fieldset/div[3]/div/span/input"
    submitButton = driver.find_element_by_xpath(submitButtonPath)
    submitButton.click()
    time.sleep(3)
    getListOfOffers("https://www.olx.pl/pomorskie/q-macbook/")


def openOfferPage(offerUrl):
    print(offerUrl)
    driver.get(offerUrl)
    messageUrl = driver.find_element_by_class_name('button-email').get_attribute('href')
    sendMessage(messageUrl)
    

def getListOfOffers(url):
    print("Getting list of offers")
    driver.get(url)
    offerListNumber = str(3)
    i = 0
    while True:
        i = i + 1
        offerListNumberString = str(offerListNumber) 
        if offerListNumber == 10:
            offerListNumber = 11
        if offerListNumber == 13:
            offerListNumber = 14
        offerPrePath = "//*[@id=\"offers_table\"]/tbody/tr["
        offerPostPath = "]/td/div/table/tbody/tr[1]/td[2]/div/h3/a"
        offerPath = offerPrePath + offerListNumberString + offerPostPath
        pricePrePath = "//*[@id=\"offers_table\"]/tbody/tr["
        pricePostPath = "]/td/div/table/tbody/tr[1]/td[3]/div/p/strong"
        pricePath = pricePrePath + offerListNumberString + pricePostPath
        offerListNumberString = (int(offerListNumberString) - int(3))
        offerName = driver.find_element_by_xpath(offerPath).text
        offerUrl = driver.find_element_by_xpath(offerPath).get_attribute('href')
        priceNumber = driver.find_element_by_xpath(pricePath).text
        offerListNumber = int(offerListNumber) + int(1)
        print(str(i) + "." + offerName)
        print("price: " + priceNumber)
        print("Do you want it? Write yes/no")
        shouldISendMessage = input()
        if (shouldISendMessage == "yes"):
            openOfferPage(offerUrl)
            break
        if offerListNumber == 44:
            break

def doAuth(loginUrl):
    driver.get(loginUrl)
    mojOlxButtonPath = "//*[@id=\"topLoginLink\"]"
    mojOlxButton = driver.find_element_by_xpath(mojOlxButtonPath)
    mojOlxButton.click()
    time.sleep(3)
    print("Logging using predefined password and login")
    loginFieldPath = "//*[@id=\"userEmail\"]"
    passwordFieldPath = "//*[@id=\"userPass\"]"
    loginField = driver.find_element_by_xpath(loginFieldPath)
    passworldField = driver.find_element_by_xpath(passwordFieldPath)
    loginField.send_keys(login)
    passworldField.send_keys(password)
    buttonPath = "//*[@id=\"se_userLogin\"]"
    loginButton = driver.find_element_by_xpath(buttonPath)
    time.sleep(2) # safe logging in
    loginButton.click()
    time.sleep(2) # safe logging in
    getListOfOffers("https://www.olx.pl/pomorskie/q-macbook/")

doAuth("https://www.olx.pl")