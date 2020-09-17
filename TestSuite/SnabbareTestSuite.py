import unittest
import os
import sys
import warnings
import requests
sys.path.append("..")  # Goes to the root Directory to find the main file, just purposes to run unittest through the command
import main
from TestSuite.AbstractTestMethods import AbstractTestMethods
from config import Environment

"""

    - Snabbare -- 

"""

# Class Setup
abstract = AbstractTestMethods()
environment = Environment('snabbare', 'https://www.snabbare.com/sv/', '', False)


class SnabbareTestSuite(unittest.TestCase):

    # Before Each TestCase
    def setUp(self):
        print('---------------------------------------')
        print('INF: Starting TestCase: ' + self._testMethodName)
        warnings.simplefilter('ignore', category=ResourceWarning)   # Imported because there is a bug in the selenium.

    # Checks so that the navbar display Spelpaus, Spelgränser, Självtest
    def test_navbar(self):

        # Load up
        selenium_session = main.WebDriverSession(environment)
        active_session = selenium_session.load_page()

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
        active_session = selenium_session.load_page()

        # Execution
        try:

            AbstractTestMethods.spel_inspektionen_logo_abstract(abstract, active_session)

        except Exception:
            raise Exception('Execution of ' + self._testMethodName + ' failed, please check error log')

        finally:
            active_session.quit()

    def test_locate_to_casino(self):

        # Load up
        selenium_session = main.WebDriverSession(environment)
        active_session = selenium_session.load_page()

        # Execution
        try:

            XpathToCasinoLink = '//*[@id="main-layout"]/div/div/div[3]/span[1]/a/div'
            AbstractTestMethods.navigate_casino_explore_abstract(abstract, active_session, XpathToCasinoLink, environment)

        except Exception:
            raise Exception('Execution of ' + self._testMethodName + ' failed, please check error log')

        finally:
            active_session.quit()

    def test_like_game_at_casino(self):

        # Load up
        selenium_session = main.WebDriverSession(environment)
        active_session = selenium_session.load_page()

        # Execution
        try:
            xpathToLikeButton = 'item__love u-flex u-relative false   '
            AbstractTestMethods.like_game_from_grid(abstract, active_session, environment, xpathToLikeButton)

        except Exception:
            raise Exception('Execution of ' + self._testMethodName + ' failed, please check error log')

        finally:
            active_session.quit()

    def test_cash_input_SEB(self):

        # Load up
        selenium_session = main.WebDriverSession(environment)
        active_session = selenium_session.load_page()

        # Execution
        try:

            AbstractTestMethods.add_cash_with_seb_digipass(abstract, active_session, environment)

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

        jsonObject = requests.get(environment.baseURL.split('sv')[0] + 'rest/state/casino/lovedAndRecentlyPlayed').json()
        self.assertEqual(True, 'SUCCESS' == jsonObject.get('status'))
        self.assertEqual(True, len(jsonObject.get('result').get('loved')) == 0)
        self.assertEqual(True, len(jsonObject.get('result').get('recent')) == 0)

