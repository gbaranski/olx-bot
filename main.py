from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import time
import readchar
driver = Chrome()

login = "gbaranski19@gmail.com"
password = "pass"
messageString = "Dzien dobry, \n Czy bylby Pan zainteresowany wymiana na komputer PC?"



def sendMessage(offerUrl):
    print("Message is sending!")
    additionalBrowser = Chrome()
    additionalBrowser.get(offerUrl)
    messageUrl = driver.find_element_by_class_name('button-email').get_attribute('href')
    sendMessage(messageUrl)
    additionalBrowser.get(messageUrl)
    messageTextArea = driver.find_element_by_xpath("//*[@id=\"ask-text\"]")
    messageTextArea.send_keys(messageString)
    submitButton = driver.find_element_by_xpath("//*[@id=\"contact-form\"]/fieldset/div[3]/div/span/input")
    submitButton.click()

    
def getNextPageUrl():
    print("Changing to next page")
    try:
        nextButtonURL = driver.find_element_by_xpath("//*[@id=\"body-container\"]/div[3]/div/div[8]/span[9]/a").get_attribute('href')
        print(nextButtonURL)
        getListOfOffers(nextButtonURL)
    except NoSuchElementException as exception:
        print("Its last page!")

def additionalOfferInfo(offerUrl):
    print("Printing description of a offer")
    additionalBrowser = Chrome()
    additionalBrowser.get(offerUrl)
    offerDescription = additionalBrowser.find_element_by_xpath("//*[@id=\"textContent\"]").text
    additionalBrowser.close()
    return offerDescription


def askUserDoesHeWant(offerUrl):
    print("If you want it, press Y, else N. For offer description I. For link L")
    userKey = readchar.readkey()
    if (userKey == "y" or userKey == 'Y'):
        print("yes")
        offerDatabase = open("offerDatabase.txt", "a")
        offerDatabase.write(offerUrl)
        sendMessage(offerUrl)
    elif (userKey == 'n' or userKey == 'N'):
        print("no")
    elif (userKey == 'i' or userKey == 'I'):
        print("------------------------------")
        print(additionalOfferInfo(offerUrl))
        askUserDoesHeWant(offerUrl)
    elif (userKey == 'l' or userKey == 'L'):
        print(offerUrl)
    elif (userKey == readchar.key.CTRL_C):
        print("Bye")
        driver.exit()
        exit()
    else:
        askUserDoesHeWant(offerUrl)    

def checkIfFileContainsString(stringToSearch):
    offerDatabase = open("offerDatabase.txt", "r")
    for line in offerDatabase:
        if (stringToSearch in line):
            return True
            offerDatabase.close()
 
def getListOfOffers(offerListUrl):
    print("Getting list of offers")
    driver.get(offerListUrl)
    arrayOfferNames = driver.find_elements_by_xpath("//a[contains(@class, 'marginright5') and contains(@class, 'link') and contains(@class, 'linkWithHash') and contains(@class, 'detailsLink') and not(contains(@class, 'detailsLinkPromoted'))]")
    arrayOfferPrices = driver.find_elements_by_xpath('//*[@id="offers_table"]/tbody/tr[3]/td/div/table/tbody/tr[1]/td[3]/div/p/strong')
    for offerName, offerPrice in zip(arrayOfferNames, arrayOfferPrices):
        print("------------------------------")
        if (checkIfFileContainsString(offerName.get_attribute('href'))):
            print("One offer has been skipped!")
        else:
            print(offerName.text)
            print(offerPrice.text)
            askUserDoesHeWant(offerName.get_attribute("href"))
    getNextPageUrl()
 

def doAuth(loginUrl):
    driver.get(loginUrl)
    mojOlxButton = driver.find_element_by_xpath("//*[@id=\"topLoginLink\"]")
    mojOlxButton.click()
    time.sleep(3)
    print("Logging using predefined password and login")
    loginField = driver.find_element_by_xpath("//*[@id=\"userEmail\"]")
    passworldField = driver.find_element_by_xpath("//*[@id=\"userPass\"]")
    loginField.send_keys(login)
    passworldField.send_keys(password)
    loginButton = driver.find_element_by_xpath("//*[@id=\"se_userLogin\"]")
    time.sleep(2) # safe logging in
    loginButton.click()
    time.sleep(2) # safe logging in
    getListOfOffers("https://www.olx.pl/pomorskie/q-macbook/")

#doAuth("https://www.olx.pl")
getListOfOffers("https://www.olx.pl/pomorskie/q-macbook/")