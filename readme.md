## Comeon Testing Project
> Just a asignment project to test towards the comeon sites Hajper.com and Snabbare.com

### Prerequistes:
To able to run this project you need to have Python installed and preferably docker. Docker is for the headless selenium grid but the
project can be runned on the non-headless webdriver.

### Usage:
To use this project you can either execute the test as non-headless tests or headless tests.

#### Execution in non-headless:
When executing the test within the non-headless webdriver a chromedriver is needed, it already exist one in the project at: ../Webdrivers/chrome_driver_85.exe
If this webdriver wouldn't work you can install a new one and replace this webdriver. Download page for chrome driver: https://chromedriver.chromium.org/downloads

When the driver has been setup, some changes has to be made towards the files within the project:

> Go to HajperTestSuite and SnabbareTestSuite and change the function name and add a '2' to the function name:
```
FROM: active_session = selenium_session.load_page()
TO: active_session = selenium_session.load_page2()
```
If the chrome driver is working, you can go to the section 'Actual Execution of Tests' to see how the execution proccess are.

#### Execution in headless:

When executing the test within the headless webdriver docker is needed. Docker helps to host a selenium/standalone-chrome node to able to perform the test on your local machines kernal. To Execute test towards this node a docker images has to be setup.

Docker commands that has to be executed in the cmd:
```
docker pull selenium/hub 
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:3.141.59-20200826
```
When running the second command it should download the image, and host it and the environment should be setup, these are my current images pulled from the docker hub if it would appear that the server wont start, try downloading these images and see if it fixes it.

```
REPOSITORY                   TAG                 IMAGE ID            CREATED             SIZE
selenium/standalone-opera    3.141.59-20200826   e45a417f24a5        3 weeks ago         972MB
selenium/standalone-chrome   3.141.59-20200826   94750fa10f22        3 weeks ago         918MB
selenium/standalone-chrome   latest              94750fa10f22        3 weeks ago         918MB
selenium/node-chrome         latest              6df82e991002        3 weeks ago         918MB
selenium/hub                 latest              dffdad82155b        3 weeks ago         263MB
```

#### Actual Execution of Tests:
When executing the actual tests, it can be done either within an IDE or in the cmd:

*Note: Remember to path to correct directory or else the python interpreter wont find the tests.

```
 cd ../ComeonTestSuite/TestSuite
```

When the correct path is set, the test can be executed by two ways:
```
python -m unittest HajperTestSuite
python -m unittest SnabbareTestSuite

OR with xml reports

python -m xmlrunner HajpareTestSuite.py
python -m xmlrunner SnabbareTestSuite.py
```

*Note: If a test passes it prints ('.') and ('E') if it fails by default at the end of every test.

#### Modification to the tests

##### Change to non-headless webdriver method:
As explained in the non-headless webdriver you can change the method of either headless or non headless within the methods.

##### Enable mobile mode:
To Enable mobile mode:
> Go to HajperTestSuite and SnabbareTestSuite and at the very top of the file change the Environment variable to True:
```
FROM:  environment = Environment('hajper', 'https://www.hajper.com/sv/', '', False)
TO:    environment = Environment('hajper', 'https://www.hajper.com/sv/', '', True)
```

##### Disclaimers:
Test passes almost everytime, some problems can appear when the loading takes to long. Mostly of all these things can be fixed, but the date and time the project had to be delivered it went with a simple solution.


