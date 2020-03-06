from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import time
import readchar
driver = Chrome()

login = "gbaranski19@gmail.com"
password = "Haslo123"
messageString = "Dzien dobry, \n Czy bylby Pan zainteresowany wymiana na komputer PC?"



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
    
def getNextPageUrl():
    print("Changing to next page")
    nextPageButtonPath = "//*[@id=\"body-container\"]/div[3]/div/div[8]/span[9]/a"
    try:
        nextButtonURL = driver.find_element_by_xpath(nextPageButtonPath).get_attribute('href')
        print(nextButtonURL)
        getListOfOffers(nextButtonURL)
    except NoSuchElementException as exception:
        print("Its last page!")

def askUserDoesHeWant(offerUrl):
    print("If you want it, press Y, else N")
    userKey = readchar.readkey()
    if (userKey == "y" or userKey == 'Y'):
        print("yes")
    elif (userKey == 'n' or userKey == 'N'):
        print("no")
    elif (userKey == readchar.key.CTRL_C):
        print("Bye")
        exit()
    else:
        askUserDoesHeWant(offerUrl)    

def getListOfOffers(offerListUrl):
    print("Getting list of offers")
    driver.get(offerListUrl)
    arrayOfferNames = driver.find_elements_by_xpath("//a[contains(@class, 'marginright5') and contains(@class, 'link') and contains(@class, 'linkWithHash') and contains(@class, 'detailsLink')]")
    arrayOfferPrice = driver.find_elements_by_xpath("//p[contains(@class, 'price')]")
    for offerName, offerPrice in zip(arrayOfferNames, arrayOfferPrice):
        print(offerName.text)
        print(offerPrice.text)
        askUserDoesHeWant(offerName.get_attribute("href"))
    getNextPageUrl()


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

#doAuth("https://www.olx.pl")
getListOfOffers("https://www.olx.pl/pomorskie/q-macbook/")