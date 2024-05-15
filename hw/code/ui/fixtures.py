import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ui.pages.auth_page import AuthPage
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.registration_page import RegistrationPage
from ui.pages.cabinet_page import CabinetPage
from ui.pages.center_commerce_page import CenterCommercePage
import os
from dotenv import load_dotenv


@pytest.fixture()
def driver(config):
    browser = config['browser']
    url = config['url']
    selenoid = config['selenoid']
    vnc = config['vnc']
    options = Options()
    if selenoid:
        capabilities = {
            'browserName': 'chrome',
            'version': '118.0',
        }
        if vnc:
            capabilities['enableVNC'] = True
        driver = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            options=options,
        )
    elif browser == 'chrome':
        driver = webdriver.Chrome()
    elif browser == 'firefox':
        driver = webdriver.Firefox()
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture(scope='session')
def credentials_without_cabinet():
    load_dotenv()
    return os.getenv('LOGIN_WITHOUT_CABINET'), os.getenv('PASSWORD_WITHOUT_CABINET')


@pytest.fixture(scope='session')
def credentials_with_cabinet():
    load_dotenv()
    return os.getenv('LOGIN'), os.getenv('PASSWORD')


@pytest.fixture
def auth_page(driver):
    return AuthPage(driver=driver)


@pytest.fixture
def cabinet_page(driver, credentials_with_cabinet, auth_page):
    driver.get(RegistrationPage.url)
    auth_page.login(*credentials_with_cabinet)
    return CabinetPage(driver=driver)


@pytest.fixture
def center_commerce_page(driver, cabinet_page):
    driver.get(CenterCommercePage.url)
    return CenterCommercePage(driver=driver)