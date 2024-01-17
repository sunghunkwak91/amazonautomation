from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import locale

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options, executable_path="/Users/sunghunkwak/chromedriver.exe")

driver.get("https://www.amazon.com")

signIn = driver.find_element(By.ID, "nav-link-accountList")
signIn.click()

userID = driver.find_element(By.ID, "ap_email")
userID.send_keys("amazonAutomationTest@gmail.com")
userID.send_keys(Keys.RETURN)

userPassword = driver.find_element(By.ID, "ap_password")
userPassword.send_keys("09sjajs!")
userPassword.send_keys(Keys.RETURN)

try:
    searchBar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    searchBar.send_keys("macbook pro")
    searchBar.send_keys(Keys.RETURN)
except:
    driver.quit()

macbookList = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 's-result-item s-asin')]"))
)

macbookDict = {}
macbookPrice = []
macbookAsin = []


for list in macbookList:

    #getting Price from the macbookList
    whole_price = list.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
    fraction_price = list.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')

    if whole_price != [] and fraction_price != []:
        string_price = '.'.join([whole_price[0].text, fraction_price[0].text])
    else:
        string_price = 0

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    final_price = locale.atof(string_price)

    macbookPrice.append(final_price)

    #getting link
    itemLink = list.find_element(By.XPATH, './/a[contains(@class, "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")]')

    macbookDict[itemLink.get_attribute("href")] = final_price 


cheapestItemLink = min(macbookDict, key=macbookDict.get)
cheapestPrice = macbookDict[cheapestItemLink]

print("Cheapest Item's Link and Price: ", cheapestItemLink, ": ", cheapestPrice)

driver.get(f"{cheapestItemLink}")
driver.find_element(By.ID, "add-to-cart-button").click()

time.sleep(3)

noThanksBtn = driver.find_element(By.ID, "attachSiNoCoverage")
noThanksBtn.click()

time.sleep(3)

cartBtn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "attach-sidesheet-view-cart-button"))
)
cartBtn.click()






