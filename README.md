# ComeonTestSuite
>Test assignment to perform web flows and UI interactions on Hajper.com and Snabbare.com

[![Python Version][python-version]][npm-url]
[![NPM Version][npm-image]][npm-url]

### Workflow Image:
![MindMap](https://github.com/Vodrech/ComeonWebTesting/blob/master/MindMap.png?raw=true)

### Usage:
When using this project it can be used with 2 different settings. Within selenium you can either create a headless or non-headless browser when you
perform your tests. The default for this project is an headless browser and needs to be setup before actually running. If the non-headless browser is wanted just
follow the instructions under the ### non-headless browser testing:

### Headless browser:

#### Prerequisites: 
Because this project are using docker and its containers, its useful to already have docker installed, if docker isn't installed on your computer you can go to:
https://docs.docker.com/docker-for-windows/install/

Check that docker exist on your computer:
```
docker --version
```

docker command to run the chrome node/standalone server:
```
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:3.141.59-20200826
```
To check that its running:

```
docker ps
```

#### Executing Headless browser tests:
When the server/node is up and running you can simply just execute the test within the cmd, but remember to locate to the correct directory or the
python interpreter won't able to find the tests.
```
cd C:/Users/.../ComeonTestSuite/TestSuite
```
To run the tests through cmd:
```
python -m unittest HajperTestSuite
python -m unittest SnabbareTestSuite
```
After each test either a ('.') or a ('E') are displayed to show if the test ERROR or PASS.
E = ERROR
. = PASS

#### Executing Non-Headless browser tests:
Non Headless browser tests can be executed the same way as headless browser tests, the only difference is that no server/node are needed and
can be executed directly.
> Note: Only if the correct webdriver are placed in the Webdriver folder.

##### Changes that has to be made:
The changes that has to be made before the execution are:

Editing the HajperTestSuite and SnabbareTestSuite function usage on every test:

active_session = selenium_session.load_page()

TO

active_session = selenium_session.load_page2()


<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/badge/version-v1.0-brightgreen
[npm-url]: https://npmjs.org/package/datadog-metrics
[python-version]: https://img.shields.io/badge/python-%2B3.7-blue
