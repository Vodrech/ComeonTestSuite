from selenium import webdriver
import config
import time
import requests
from config import Environment


"""

    @ PageFetcher 
        - Checks so no authorization or connection problems are towards the requested web page.
        
    
    
"""


class PageFetcher:

    # Initialization
    def __init__(self, web_page, headers):
        self.web_page = str(web_page)
        self.headers = headers

    # Main Method for Object | Fetches an url and checks if it returns successfully ( status.code = 200 )
    def validate_connection(self):

        for x in range(5):
            page = requests.get(self.web_page + self.headers)  # Fetching the url that was requested
            if page.status_code == 200:
                print("EXE: Page Returned StatusCode = " + str(page.status_code))
                return 1

            else:

                if x == 5:
                    print("EXE: Page Returned StatusCode = " + str(page.status_code))
                    return 0

                continue


class WebDriverSession:

    def __init__(self, Environment):
        self.environment = Environment

    # Headless testing
    def load_page(self):

        # Creates the PageFetcher Object
        page = PageFetcher(self.environment.baseURL, self.environment.headers)
        connection = page.validate_connection()

        # Checks if the page returns a valid request ( 200 )
        if connection == 1:

            # driver = webdriver.Chrome(self.web_driver)
            driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=webdriver.DesiredCapabilities.CHROME)
            print("EXE: Running on: " + str(driver.desired_capabilities.get('browserName')) + " with the SessionID: " + str(driver.session_id))
            driver.get(self.environment.baseURL)
            print("EXE: Driver getting webpage: " + str(self.environment.baseURL))

            # Waits for the page to load, Timeouts if the loading takes more than 10 seconds
            while driver.execute_script("return document.readyState") != "complete":
                timeout = time.process_time()

                if timeout >= 10:
                    raise requests.exceptions.HTTPError("Webdriver Timeout, driver took to long to load page!")

            return driver

        else:
            raise requests.exceptions.RequestException("Page: " + str(self.environment.baseURL) + " could not be loaded, please check connection, authorization etc")

    # For visual testing
    def load_page2(self):

        # Creates the PageFetcher Object
        page = PageFetcher(self.environment.baseURL, self.environment.headers)
        connection = page.validate_connection()

        # Checks if the page returns a valid request ( 200 )
        if connection == 1:

            # driver = webdriver.Chrome(self.web_driver)
            driver = webdriver.Chrome('../WebDrivers/chrome_driver_85.exe')
            print("EXE: Running on: " + str(
                driver.desired_capabilities.get('browserName')) + " with the SessionID: " + str(driver.session_id))
            driver.get(self.environment.baseURL)
            print("EXE: Driver getting webpage: " + str(self.environment.baseURL))

            # Waits for the page to load, Timeouts if the loading takes more than 10 seconds
            while driver.execute_script("return document.readyState") != "complete":
                timeout = time.process_time()

                if timeout >= 10:
                    raise requests.exceptions.HTTPError("Webdriver Timeout, driver took to long to load page!")

            return driver

        else:
            raise requests.exceptions.RequestException("Page: " + str(
                self.environment.baseURL) + " could not be loaded, please check connection, authorization etc")
