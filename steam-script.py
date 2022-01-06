from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def getValorInString(string):
    value = ""
    add = False
    for i in range(len(string)):
        if string[i - 2] == "R" and string[i - 1] == "$" and string[i] == " ":
            add = True
        if (add == True) and (string[i].isnumeric() or string[i] == ","):
            value += string[i]

    return float(value.replace(",", "."))


entryUsername = str(input("Your login: "))
entryPassword = str(input("Your password: "))

#change the path for the location of chromedriver.exe in your chrome version
path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)

driver.get("https://steamcommunity.com/login/home/?goto=market%2F")

time.sleep(1.5)
username = driver.find_element_by_id("input_username")
username.send_keys(entryUsername)

password = driver.find_element_by_id("input_password")
password.send_keys(entryPassword)
password.send_keys(Keys.RETURN)

#sleep time to get the code in steam guard
time.sleep(10)

#can change the product, but by my research the trading cards are the best!
searchMarket = driver.find_element_by_id("findItemsSearchBox")
searchMarket.send_keys("Trading Card")
searchMarket.send_keys(Keys.RETURN)

#counting how many pages will traverse
numberOfPages = 0
while numberOfPages != 300:
    time.sleep(8)

    for i in range(10):
        searchAnnouncement = driver.find_element_by_id("result_" + str(i)).click()
        time.sleep(5)

        try:
            searchHigherValue = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "market_commodity_forsale"))
            )
        except:
            driver.quit()

        try:
            searchLowerValue = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "market_commodity_buyrequests"))
            )
        except:
            driver.quit()

        stringHigherValue = searchHigherValue.text
        stringLowerValue = searchLowerValue.text


        if (stringLowerValue == "There are no active buy orders for this item." or stringHigherValue == "There are no active listings for this item."):

            time.sleep(2)
            enter = driver.find_element_by_class_name("btn_green_white_innerfade").click()
            time.sleep(3)

            searchInputPrice = driver.find_element_by_id("market_buy_commodity_input_price")
            searchInputPrice.clear()
            searchInputPrice.send_keys(str(0.03))

            searchInputAmount = driver.find_element_by_id("market_buy_commodity_input_quantity")
            time.sleep(1)
            searchInputAmount.clear()
            searchInputAmount.send_keys("5")

            acceptBuyOrder = driver.find_element_by_id("market_buyorder_dialog_accept_ssa").click()
            buying = driver.find_element_by_id("market_buyorder_dialog_purchase").click()
            driver.back()
            time.sleep(2)

        else:
            higherValue = getValorInString(stringHigherValue)
            lowerValue = getValorInString(stringLowerValue)

            # the logic can change in what you analyze... so stay free to do it!
            if lowerValue > 0.45 * higherValue and lowerValue < 0.8 * higherValue and higherValue >= 0.25:

                    time.sleep(2)
                    enter = driver.find_element_by_class_name("btn_green_white_innerfade").click()
                    time.sleep(3)

                    searchInputPrice = driver.find_element_by_id("market_buy_commodity_input_price")
                    time.sleep(1)
                    searchInputPrice.clear()
                    searchInputPrice.send_keys(str(0.55 * higherValue))

                    searchInputAmount = driver.find_element_by_id("market_buy_commodity_input_quantity")
                    time.sleep(1)
                    searchInputAmount.clear()
                    searchInputAmount.send_keys("5")

                    acceptBuyOrder = driver.find_element_by_id("market_buyorder_dialog_accept_ssa").click()
                    buying = driver.find_element_by_id("market_buyorder_dialog_purchase").click()
                    driver.back()
                    time.sleep(2)

                #the logic can change in what you analyze... so stay free to do it!

            elif lowerValue < 0.45 * higherValue and higherValue > 0.15:

                    time.sleep(2)
                    enter = driver.find_element_by_class_name("btn_green_white_innerfade").click()
                    time.sleep(3)

                    searchInputPrice = driver.find_element_by_id("market_buy_commodity_input_price")
                    time.sleep(1)
                    searchInputPrice.clear()
                    searchInputPrice.send_keys(str(higherValue * 0.5))

                    searchInputAmount = driver.find_element_by_id("market_buy_commodity_input_quantity")
                    time.sleep(1)
                    searchInputAmount.clear()
                    searchInputAmount.send_keys("5")

                    acceptBuyOrder = driver.find_element_by_id("market_buyorder_dialog_accept_ssa").click()
                    buying = driver.find_element_by_id("market_buyorder_dialog_purchase").click()
                    driver.back()
                    time.sleep(2)

        driver.back()
        time.sleep(2)

    numberOfPages += 1
    searchNextPage = driver.find_element_by_id("searchResults_btn_next").click()

time.sleep(5)
driver.close()
