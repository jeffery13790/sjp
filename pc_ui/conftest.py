import pytest
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException


@pytest.fixture(scope='session', autouse=True)
def init_driver():
    try:
        username = '18856012041'
        driver = Chrome()
        driver.implicitly_wait(20)
        driver.get(url=r'https://cs1.jsbooks.com.cn/user/login')
        driver.maximize_window()
        driver.find_element_by_xpath('//*[@id="login"]//input[@placeholder="请输入手机号"]').send_keys(username)
        driver.find_element_by_xpath('//*[@id="login"]//span/span/span').click()
        driver.find_element_by_xpath('//*[@id="login"]//input[@placeholder="请输入短信验证码"]').send_keys('123456')
        driver.find_element_by_xpath('//*[@id="login"]/div[2]/div/div/div[3]/label/span').click()
        driver.find_element_by_xpath('//*[@id="login"]/div[2]//button[@type="button"]').click()
        yield driver
        driver.quit()
    except:
        raise NoSuchElementException("登录客户端失败")