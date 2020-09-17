import unittest
import os
import sys
import warnings
import requests
sys.path.append("..")  # Goes to the root Directory to find the main file, just purposes to run unittest through the command
import main
from TestSuite.AbstractTestMethods import AbstractTestMethods
from config import Environment
import time
import xmlrunner


# Class Setup
abstract = AbstractTestMethods()
environment = Environment('hajper', 'https://www.hajper.com/sv/', '', False)


class HajperTestSuite(unittest.TestCase):


    # Before Each TestCase
    def setUp(self):
        print('\n---------------------------------------')
        print('INF: Starting TestCase: ' + self._testMethodName)
        warnings.simplefilter('ignore', category=ResourceWarning)   # Imported because there is a bug in the selenium.

    # Checks so that the navbar display Spelpaus, Spelgränser, Självtest
    def test_navbar(self):

        # Load up
        selenium_session = main.WebDriverSession(environment)
        active_session = selenium_session.load_page(environment.mobileMode)

        # Execution
        try:

            AbstractTestMethods.navbar_abstract(abstract, active_session)

        except Exception:
            raise Exception('Execution of ' + self._testMethodName + ' failed, please check error log')

        finally:
            active_session.quit()

    def test_spel_inspektionen_logo(self):

        # Load up
        selenium_session = main.WebDriverSession(environment)
        active_session = selenium_session.load_page(environment.mobileMode)

        # Execution
        try:

            AbstractTestMethods.spel_inspektionen_logo_abstract(abstract, active_session, environment)

        except Exception:
            raise Exception('Execution of ' + self._testMethodName + ' failed, please check error log')

        finally:
            active_session.quit()

    def test_locate_to_casino(self):

        # Load up
        selenium_session = main.WebDriverSession(environment)
        active_session = selenium_session.load_page2(environment.mobileMode)

        # Execution
        try:

            XpathToCasinoLink = '//*[@id="main-layout"]/div/div/div[3]/span[1]/a'
            AbstractTestMethods.navigate_casino_explore_abstract(abstract, active_session, XpathToCasinoLink, environment)

        except Exception:
            raise Exception('Execution of ' + self._testMethodName + ' failed, please check error log')

        finally:
            active_session.quit()

    def test_like_game_at_casino(self):

        # Load up
        selenium_session = main.WebDriverSession(environment)
        active_session = selenium_session.load_page(environment.mobileMode)

        # Execution
        try:
            xpathTolikeButton = 'item__love u-flex u-relative false   '
            AbstractTestMethods.like_game_from_grid(abstract, active_session, environment, xpathTolikeButton)

        except Exception:
            raise Exception('Execution of ' + self._testMethodName + ' failed, please check error log')

        finally:
            active_session.quit()

    def test_cash_input_SEB(self):

        # Load up
        selenium_session = main.WebDriverSession(environment)
        active_session = selenium_session.load_page(environment.mobileMode)

        # Execution
        try:

            AbstractTestMethods.add_cash_with_seb_digipass(abstract, active_session, environment)

        except Exception:
            raise Exception('Execution of ' + self._testMethodName + ' failed, please check error log')

        finally:
            active_session.quit()

    def test_spin_therespinners(self):

        # Load up
        selenium_session = main.WebDriverSession(environment)
        active_session = selenium_session.load_page2(environment.mobileMode)
        active_session.get(environment.casino)

        # Navigation Variables
        xpathIFrame = '//*[@id="iframe-game"]'
        xpathGameCanvas = '//*[@id="webgl"]'
        xpathGameBet = '//*[@id="BetAmountValue"]'
        xpathGameBalance = '//*[@id="BalanceValue"]'
        xpathPlaceBet = '//*[@id="PlaceBetBtn"]'

        try:
            # Execution
            print('EXE: Navigation to the game the respinners')
            time.sleep(5)
            listOfItems = active_session.execute_script("return document.getElementsByTagName('figure')")
            counter = 0
            for x in listOfItems:
                checkingName = x.text

                if str(checkingName).__contains__('The Respinners'):
                    # Scrolling to the object
                    if environment.mobileMode:
                        active_session.execute_script("return document.getElementsByTagName('figure')[arguments[0]].scrollIntoView()", counter)
                    else:
                        active_session.execute_script("return document.getElementsByTagName('figure')[arguments[0]].scrollIntoView(alignToTop=false)",counter)

                    # Clicks on the button
                    element = active_session.execute_script("return document.getElementsByTagName('figure')[arguments[0]].getElementsByClassName('dots-container u-absolute u-pos-tr0 u-cursor-hand')[0]", counter)
                    element.click()
                    boolVal = True
                else:
                    counter+=1
                    continue

            if boolVal != True:
                raise Exception('The Respinners could not be found!')

            active_session.find_element_by_xpath('//*[@id="main-layout"]/nav/div/button[3]').click()
            time.sleep(2)
            # Switching to the iframe to be able to fetch data from external site
            print('EXE: Getting the iframe for the game')
            active_session.switch_to.frame(active_session.find_element_by_xpath(xpathIFrame))

            # Game Interaction
            time.sleep(10)
            print('EXE: Starting the game')
            active_session.find_element_by_xpath(xpathGameCanvas).click()
            time.sleep(5)

            bettingAmount = active_session.find_element_by_xpath(xpathGameBet).text
            balanceAmount = active_session.find_element_by_xpath(xpathGameBalance).text

            print('EXE: Betting: ' + str(bettingAmount) + ' with a balance of: ' + str(balanceAmount))

            # Calculating ( Balance - Bet )
            if float(active_session.find_element_by_xpath(xpathGameBet).text.split('€')[0].split(',')[0]) <= 0:
                bettingAmountAsFloat = float('0.' + active_session.find_element_by_xpath(xpathGameBet).text.split('€')[0].split(',')[1])
            else:
                bettingAmountAsFloat = float(active_session.find_element_by_xpath(xpathGameBet).text.split('€')[0].split(',')[0])

            balanceAsFloat = float(active_session.find_element_by_xpath(xpathGameBalance).text.split('€')[0].split(',')[0].split('.')[0] +
            active_session.find_element_by_xpath(xpathGameBalance).text.split('€')[0].split(',')[0].split('.')[1])
            time.sleep(5)
            active_session.find_element_by_xpath(xpathPlaceBet).click()

            calculateFloat = balanceAsFloat - bettingAmountAsFloat
            afterBalanceFloat = float(
                active_session.find_element_by_xpath(xpathGameBalance).text.split('€')[0].split(',')[0].split('.')[0] +
                active_session.find_element_by_xpath(xpathGameBalance).text.split('€')[0].split(',')[0].split('.')[1])

            # Checking so that the bet actually calculated correctly
            self.assertEqual(True, calculateFloat == afterBalanceFloat)

            time.sleep(4)
            active_session.save_screenshot('LatestRunSpinTheSpinners.png')

        except Exception:
            raise Exception('Execution of ' + self._testMethodName + ' failed, please check error log')

        finally:
            active_session.quit()

    def test_API_player_status(self):

        jsonObject = requests.get(environment.baseURL.split('sv')[0] + 'player/status').json()
        self.assertEqual(True, ("SUCCESS" == jsonObject.get('status')))
        self.assertEqual(True, ("false" == jsonObject.get('result').get('map').get('authenticated')))
        self.assertEqual(True, ("Sessionen har upphört" == jsonObject.get('result').get('map').get('message')))

    def test_API_loved_games_authentication(self):

        jsonObject = requests.get(
            environment.baseURL.split('sv')[0] + 'rest/state/casino/lovedAndRecentlyPlayed').json()
        self.assertEqual(True, 'SUCCESS' == jsonObject.get('status'))
        self.assertEqual(True, len(jsonObject.get('result').get('loved')) == 0)
        self.assertEqual(True, len(jsonObject.get('result').get('recent')) == 0)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='./test-reports'))
