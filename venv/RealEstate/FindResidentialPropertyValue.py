""""    This program uses an electoral roll list I've found on LINZ, and runs randomised addresses
        through qv.co.nz to get the price of the house
        I ignore non-residential properties, and output this data in a format to use
        in RealEstatePrediction"""

def openFile():
    file = open("LINZ data.csv", "r+")
    return file

def readLine(file):
    lineData = file.readline()
    elements = lineData.split(',')
    address = elements[5]
    lattitude = elements[15]
    longitude = elements[16]
    longitude = longitude.replace("\n", "")
    return address, lattitude, longitude

# I didn't originally use headless browsers, as I had to do some troubleshooting
#   But headless browsers for this kind of operation is quicker
def openBrowser(headlessBrowsing):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.

    if headlessBrowsing:
        #driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
        driver = webdriver.Chrome(chrome_options=options)
    else:
        driver = webdriver.Chrome()
    return driver

# Puts data into a category according to price
def getPriceCategory(price):
    if price < 300000:
        return 1
    if price < 600000:
        return 2
    if price < 900000:
        return 3
    if price < 1200000:
        return 4
    if price < 1500000:
        return 5
    else:
        return 6

def createSearch(driver, address):
    # from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    driver.get("https://www.qv.co.nz/")
    assert "QV.co.nz" in driver.title
    # driver.implicitly_wait(10)

    try:
        element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID  , "search"))
            )
    except:
        return -1

    elem = driver.find_element_by_name("searchTerm")
    elem.clear()
    elem.send_keys(address)
    elem.send_keys(Keys.RETURN)

    return 1

# I have created my own wait for an element, as found problems using the library
#   [It just wasn't waiting)
def myWaitForElement (driver, cssSelectorName, numTries):
    loopContinue = True
    loopCount =0
    while ((loopContinue==True) and (loopCount<numTries)):
        loopContinue=False
        loopCount=loopCount+1
        import time
        time.sleep(0.5)
        try:
            elem = driver.find_element_by_css_selector(cssSelectorName)
        except:
            loopContinue=True

        # If an alert has been raised, there's no property there, so shortcut this ...
        try:
            elem = driver.find_element_by_css_selector(".alert")
            if "There are no properties which match your search" in elem.text:
                return True
        except:
            time.sleep(0.5)
    return loopContinue

def findValueFromWebPage (driver):
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # Wait for the elements .capitalVal and .buildingTypeVal
    if (myWaitForElement(driver, ".capitalVal", 40)) or (myWaitForElement(driver, ".buildingTypeVal", 20)):
        return -1

    # Find the value
    # Strip out $ and ,
    elem = driver.find_element_by_css_selector(".capitalVal")
    value = elem.text
    value = value.replace("$", "")
    value = value.replace(",", "")

    # If it's not residential, we don't want the data
    elem = driver.find_element_by_css_selector(".buildingTypeVal")
    type = elem.text
    if "Residential" not in type:
        return -1

    # Turn the text string into an integer, and return
    # Have occasionally had issues here
    try:
        returnValue = int(value)
    except:
        return -1
    return returnValue


# =====================
# MAIN BODY STARTS HERE
# =====================

readFile = openFile()

# I am expecting to have to run this file several times, hence will discard some lines before
#   starting to process data
startProcessingFromLine = 1367
currentLine = 1

while currentLine < startProcessingFromLine:
    lineData = readLine(readFile)
    currentLine = currentLine + 1



# Open browser ready for searching
driver = openBrowser(True)

# Now process the rest
# I didn't expect to be able to run all these, but thought it good to see how well it would go
while currentLine < 50000:

    lineData = readLine(readFile)
    lattitude = lineData[1]
    longitude = lineData[2]
    address =  lineData[0]

    if createSearch(driver, address) != 0:
        value = findValueFromWebPage(driver)
        if value > 0:
            category = getPriceCategory(value)
            printLine = str(currentLine) + "|" + lattitude + "|" + longitude  + "|" + str(category)  + "|" + str(value)  + "|" + address + "\n"

            # Open file to write to
            writeFile = open("Property Data For ML", "a")
            writeFile.write(printLine)
            writeFile.close()
            print(printLine)

    currentLine = currentLine + 1

readFile.close()
