import unittest
import os
import sys
import warnings
import requests
import config
import time
from random import randrange
import json
from config import Environment


class AbstractTestMethods(unittest.TestCase):

    def navbar_abstract(self, driver_object):

        # xpath's to <a> elements
        navbar_objects = {
            'spelpaus': '//*[@id="regulations-header"]/span[1]/a',
            'spelgranser': '//*[@id="regulations-header"]/span[2]/a',
            'sjalvtest': '//*[@id="regulations-header"]/span[3]/a',
        }

        # Method to check if <a> elements is displayed
        def check_if_displayed():

            print('EXE: Checking for navbar elements appearance...')

            for (x, y) in navbar_objects.items():
                try:
                    self.assertEqual(True, driver_object.find_element_by_xpath(y).is_displayed())
                    print('EXE: Element found: ' + str(x))

                except Exception:
                    raise Exception('Element: ' + str(x) + 'Could not be found')

        # link's to <a> elements
        navbar_link_objects = {
            'spelpaus': 'https://www.spelpaus.se/?scos=true',
            'spelgranser': str(driver_object.current_url) + '/account/my-limits',
            'sjalvtest': 'https://stodlinjen.se/#!/spelberoende-test-pgsi'
        }

        # Method to check if <a> elements have correct link and if link is working
        def check_if_broken_link():

            print('EXE: Controlling navbar-links pointers')

            for (x, y) in navbar_objects.items():
                try:
                    url = driver_object.find_element_by_xpath(y).get_attribute('href')

                    if navbar_link_objects.get(str(x)) == url:
                        responseCode = requests.get(url).status_code
                        if responseCode >= 400:
                            self.assertEqual.fail('Link to element %s is not a valid page')
                        print('INF: Pointer ' + x + ' CORRECT')
                    else:
                        self.fail('The element: ' + str(x) + ' is pointing towards wrong page. \n Expected: ' + str(
                            navbar_link_objects.get(str(x))) + ' , Actual: ' + str(url))

                except Exception:
                    raise

        # Running above methods
        check_if_displayed()
        check_if_broken_link()

    def spel_inspektionen_logo_abstract(self, driver_object, Environment):
        print('EXE: Controlling spel_inspektionen-logo')
        driver_object.execute_script("document.getElementsByClassName('licenses-logos__spelinspektionen u-dib')[0].scrollIntoView();")
        time.sleep(2)

        if Environment.mobileMode:
            inspektionLogoXpath = '//*[@id="app"]/div/div/div[1]/div/footer/section/div[3]/div[2]/a/div/span'
        else:
            inspektionLogoXpath = '//*[@id="app"]/div/div/div[1]/div/footer/div/div[3]/div[1]/a/div/span'

        self.assertEqual(True, driver_object.find_element_by_xpath(inspektionLogoXpath).is_displayed())

    def navigate_casino_explore_abstract(self, driver_object, xpath, Environment):
        print('EXE: Controlling navigation towards the casino path')
        driver_object.find_element_by_xpath(xpath).click()

        # Checks so that the page loads correctly
        while driver_object.execute_script("return document.readyState") != "complete":
            timeout = time.process_time()

            if timeout > 10:
                raise TimeoutError('Timeout on loading the page: ' + str(driver_object.current_url))

        time.sleep(2)
        active_url = str(driver_object.current_url)
        urlBool = active_url == (Environment.casino)
        self.assertEqual(True, urlBool)

    def like_game_from_grid(self, driver_object, Environment, className):

        driver_object.get(Environment.casino)

        # Checks so that the page loads correctly
        while driver_object.execute_script("return document.readyState") != "complete":
            timeout = time.process_time()

            if timeout > 10:
                raise TimeoutError('Timeout on loading the page: ' + str(driver_object.current_url))

        time.sleep(3)
        driver_object.execute_script("return document.getElementsByTagName('figure')[2].getElementsByClassName(arguments[0])[0]", className).click()

        jsonObject = requests.get(str(Environment.verify).split('sv')[0] + 'player/status').json()
        self.assertEqual(True, ("SUCCESS" == jsonObject.get('status')))
        self.assertEqual(True, ("false" == jsonObject.get('result').get('map').get('authenticated')))
        self.assertEqual(True, ("Sessionen har upphört" == jsonObject.get('result').get('map').get('message')))

        # document.getElementsByTagName('figure')[1].lastElementChild.getElementsByTagName('button')[0]

    def add_cash_with_seb_digipass(self, driver_object, Environment):

        print('EXE: Navigating to the casino page')
        driver_object.get(Environment.casino)
        time.sleep(2)

        print('EXE: Controlling the insert to play functionality')

        # element selectors
        xpathToButton = '//*[@id="header-bigger"]/div/div/div/button'
        inputFieldID = 'amount'
        css = '#deposit-flow > div.payment__content-wrapper.amount__content-wrapper.u-relative > form > div.button-wrapper__SimpleButtonWrapper-sc-19e2gxb-0.button-wrapper__ButtonWrapper-sc-19e2gxb-1.kfxYMT.hheKJu.u-bg-trans > button'
        SEBPayment = '//*[@id="core_order_holder"]/div[1]/div[2]/a[5]/span'
        xpathRadioDigiPass = '//*[@id="core_order_holder"]/div[1]/div[5]/div[2]/label[2]'
        xpathinputDigiPass = '//*[@id="core_order_holder"]/div[1]/div[4]/div[2]/div[3]/input'

        xpathFortsattButton = '//*[@id="core_order_holder"]/div[2]/a'

        xpathCoreHolder = '//*[@id="core_order_holder"]/div[1]'
        xpathControlCodeOne = '//*[@id="core_order_holder"]/div[1]/div[2]'
        xpathControlCodeTwo = '//*[@id="core_order_holder"]/div[1]/div[3]'

        xpathControlCodeValidateField = '//*[@id="core_order_holder"]/div[1]/div[4]/div[2]/div[3]/input'

        # Other elements
        value = 100
        personID = 192311229252

        #Xpaths
        SattInOchSpelaButtonMobile = '//*[@id="app"]/div/div/div[1]/div/div[5]/div/div/div/button'
        SattInOchSpelaButtonDesktop = '//*[@id="header-bigger"]/div/div/div/button'

        # Pressing the button | sätt in och spela
        print("EXE: Pressing the 'Sätt in och spela button'")
        if Environment.mobileMode:
            driver_object.execute_script('arguments[0].click();', driver_object.find_element_by_xpath(SattInOchSpelaButtonMobile))
        else:
            driver_object.execute_script('arguments[0].click();', driver_object.find_element_by_xpath(SattInOchSpelaButtonDesktop))

        # Inserting a value to the input field
        print('EXE: Inserting a value of: ' + str(value))
        time.sleep(2)   # Must be added because else it won't find the form element
        driver_object.find_elements_by_id(inputFieldID)[0].send_keys(value)

        # Pressing the button | Sätt in
        time.sleep(1)
        driver_object.find_element_by_css_selector(css).click()
        time.sleep(1)

        # Press the div | Trustly
        print('EXE: Selecting Trustly as payment method')
        driver_object.find_element_by_class_name('grid-u-sm-1').click()
        time.sleep(5)

        # Switching to the iframe to be able to fetch data from external site
        print('EXE: Getting external bank system')
        driver_object.switch_to.frame(driver_object.execute_script("return document.getElementById('paymentIframe')"))
        driver_object.find_element_by_xpath(SEBPayment).click()
        time.sleep(5)

        # Selecting DigiPass as authorization method
        print('EXE: Selecting DigiPass as authorization method')
        driver_object.find_element_by_xpath(xpathRadioDigiPass).click()
        time.sleep(2)

        # Entering personalID into the input field
        print('EXE: Inserting personal ID: ' + str(personID))
        driver_object.find_element_by_xpath(xpathinputDigiPass).send_keys(personID)
        driver_object.find_element_by_xpath(xpathFortsattButton).click()
        time.sleep(10)
        self.assertEqual(True, driver_object.find_element_by_xpath(xpathCoreHolder).is_displayed())
        self.assertEqual(True, driver_object.find_element_by_xpath(xpathControlCodeOne).is_displayed())
        self.assertEqual(True, driver_object.find_element_by_xpath(xpathControlCodeTwo).is_displayed())

        driver_object.find_element_by_xpath(xpathControlCodeValidateField).send_keys(1337)
        driver_object.save_screenshot('LatestRunPayWithSEB.png')

