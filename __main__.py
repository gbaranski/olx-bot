from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from undetected_chromedriver import Chrome, ChromeOptions
import time
import os.path
import readchar

mainBrowser = Chrome()

# CONFIG HERE
searching_url = "https://www.olx.pl/pomorskie/q-macbook/"
login = "gbaranski19@gmail.com"
password = "Haslo123"
messageString = "Dzien dobry, \n Czy jest możliwość wymiany na komputer PC?"


def checkIfMessageCaptchaExist():
    try:
        mainBrowser.find_element_by_id("recaptcha-anchor-label")
    except NoSuchElementException:
        return True
    return False


def sendMessage(offer_url):
    print("Message is sending!")

    main_window = mainBrowser.current_window_handle
    mainBrowser.execute_script("window.open();")
    mainBrowser.switch_to_window(mainBrowser.window_handles[1])
    mainBrowser.get(offer_url)
    message_url = mainBrowser.find_element_by_xpath("//*[@id=\"contact_methods\"]/li[1]/a").get_attribute('href')
    mainBrowser.get(message_url)
    message_text_area = mainBrowser.find_element_by_xpath("//*[@id=\"ask-text\"]")
    message_text_area.send_keys(messageString)
    if checkIfMessageCaptchaExist():
        print(
            "Needed your action! OLX.pl has blocked us and you need to complete captcha. Please do it and press enter")
        input()
        submit_button = mainBrowser.find_element_by_xpath("//*[@id=\"contact-form\"]/fieldset/div[4]/div/span/input")
    else:
        submit_button = mainBrowser.find_element_by_xpath("//*[@id=\"contact-form\"]/fieldset/div[3]/div/span/input")
    submit_button.click()
    time.sleep(2)
    mainBrowser.close()
    mainBrowser.switch_to_window(main_window)


def getNextPageUrl(is_authenticated):
    print("Changing to next page")
    try:
        next_button_url = mainBrowser.find_element_by_xpath(
            "//*[@id=\"body-container\"]/div[3]/div/div[8]/span[9]/a").get_attribute('href')
        print(next_button_url)
        return next_button_url
    except NoSuchElementException as exception:
        print("Its last page!")
        mainTab(is_authenticated)


def additionalOfferInfo(offer_url):
    print("Printing description of a offer")
    print("------------------------------")
    additional_browser = Chrome()
    additional_browser.get(offer_url)
    offer_description = additional_browser.find_element_by_xpath("//*[@id=\"textContent\"]").text
    additional_browser.close()
    return offer_description


def askUserDoesHeWant(offer_url, is_authenticated):
    print("If you want it, press Y, else N. For offer description I. For link L. To open it in your browser press O")
    user_key = readchar.readkey()
    if user_key == "y" or user_key == 'Y':
        if is_authenticated == 'Not logged in':
            print("You cannot send messages when you aren't logged in")
            print("Press B to come back to main tab and log in")
            user_key = readchar.readkey()
            if user_key == "B" or "b":
                mainTab(is_authenticated)
            askUserDoesHeWant(offer_url, is_authenticated)
        else:
            print("Input: Yes")
            offer_database = open("offerDatabase.txt", "a")
            offer_database.write(offer_url)
            offer_database.close()
            sendMessage(offer_url)
    elif user_key == 'n' or user_key == 'N':
        print("Input: No")
        offer_database = open("offerDatabase.txt", "a")
        offer_database.write(offer_url)
        offer_database.close()
    elif user_key == 'i' or user_key == 'I':
        print("------------------------------")
        print(additionalOfferInfo(offer_url))
        askUserDoesHeWant(offer_url, is_authenticated)
    elif user_key == 'l' or user_key == 'L':
        print(offer_url)
        askUserDoesHeWant(offer_url, is_authenticated)
    elif user_key == "o" or user_key == "O":
        additionalBrowser = Chrome()
        additionalBrowser.get(offer_url)
        print("Press enter when you're done")
        input()
        additionalBrowser.close()
    elif user_key == readchar.key.CTRL_C:
        print("Bye")
        mainBrowser.exit()
        exit()
    else:
        askUserDoesHeWant(offer_url, is_authenticated)


def checkIfFileContainsString(string_to_search):
    offer_database = open("offerDatabase.txt", "r")
    for line in offer_database:
        if string_to_search in line:
            offer_database.close()
            return True


def getListOffers(is_authenticated, mode):
    if is_authenticated == 'Not logged in':
        print("NOT LOGGED IN, you can't send messages to sellers")
    print("Getting list of offers")

    array_offer_names = mainBrowser.find_elements_by_xpath(
        "//a[contains(@class, 'marginright5') and contains(@class, 'link') and contains(@class, 'linkWithHash') and contains(@class, 'detailsLink') and not(contains(@class, 'detailsLinkPromoted'))]")
    array_offer_prices = mainBrowser.find_elements_by_xpath(
        '//td[normalize-space(@class)="offer"]//p[@class="price"]/strong')
    for offerName, offerPrice in zip(array_offer_names, array_offer_prices):
        print("------------------------------")
        if checkIfFileContainsString(offerName.get_attribute('href')):
            print("One offer has been skipped!")
        else:
            print(offerName.text)
            print(offerPrice.text)
            if mode != "skipAsk":
                askUserDoesHeWant(offerName.get_attribute("href"), is_authenticated)
    mainBrowser.get(getNextPageUrl(is_authenticated))
    getListOffers(is_authenticated, mode)


def doAuth():
    # print("Please enter here your login and click enter")
    # login = input()
    # print("Please enter here your password and click enter")
    # password = input()
    print("Attempting to log in")
    mainBrowser.get("https://www.olx.pl/")
    moj_olx_button_url = mainBrowser.find_element_by_xpath("//*[@id=\"topLoginLink\"]").get_attribute('href')
    print("Logging using predefined login and password")
    mainBrowser.get(moj_olx_button_url)
    mainBrowser.find_element_by_xpath("//*[@id=\"userEmail\"]").send_keys(login)
    mainBrowser.find_element_by_xpath("//*[@id=\"userPass\"]").send_keys(password)
    mainBrowser.find_element_by_xpath("//*[@id=\"se_userLogin\"]").click()
    i = 0
    while mainBrowser.current_url != "https://www.olx.pl/mojolx/#login":
        i = i + 1
        time.sleep(1)
        print(".")
        if i > 15:
            print("Logging in is taking so much time, please fix your password in config")
            exit()
    print("Logged in!")
    print("------------------------------")
    mainTab('Logged in')


def settingsTab(is_authenticated):
    print("Settings tab here")
    print("------------------------------")
    print("1. Add new messages")
    print("2. Change login")
    print("3. Edit saved offers")
    print("4. Come back to main tab")
    user_key = readchar.readkey()
    if user_key == '1':
        print("1")
    elif user_key == '2':
        print("2")
    elif user_key == '3':
        print("3")
    elif user_key == '4':
        mainTab(is_authenticated)


def mainTab(is_authenticated):
    if os.path.isfile("offerDatabase.txt") == 0:
        print("offerDatabase.txt doesn't exist. Creating it")
        offer_database = open("offerDatabase.txt", "w")
        offer_database.close()
    if is_authenticated == 'Not logged in':
        print("------------------------------")
        print("Hello, program has been made by gbaranski")
        print("Its used to manage OLX.pl and make your life easier :)")
        print("------------------------------")
        print("What would you like to do today?")
    print("1. Auth me on OLX. NEEDED TO SEND MESSAGES! Currently: " + is_authenticated)
    print("2. Search for new offers using specified criteria")
    print("3. Search for new offers not using any criteria")
    print("4. Scan for offers(program won't ask you about anything, clear scanning)")
    print("5. Settings")
    user_key = readchar.readkey()
    if user_key == '1':
        doAuth()
    elif user_key == '2':
        print("2")
    elif user_key == '3':
        mainBrowser.get(searching_url)
        getListOffers(is_authenticated, 'nocriteria')
    elif user_key == '4':
        mainBrowser.get(searching_url)
        getListOffers(is_authenticated, 'skipAsk')
    elif user_key == '5':
        settingsTab(is_authenticated)
    elif user_key == readchar.key.CTRL_C:
        exit()
    else:
        print("Select proper key")
        mainTab(is_authenticated)


mainTab("Not logged in")
