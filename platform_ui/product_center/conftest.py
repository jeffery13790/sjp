import time

import pytest
from selenium.webdriver import Chrome


@pytest.fixture(scope='session', autouse=True)
def init_driver():
    username = 'opsAdmin'
    # 测试环境平台端
    url = r'https://cs1.jsbooks.com.cn/customer/#/customer/user/login'
    password = "200622"


    #云环境
    # url = r'http://www.jssz365.com/user/login'
    # password = '200605'

    driver = Chrome()
    driver.implicitly_wait(10)
    driver.get(url=url)
    driver.maximize_window()
    driver.find_element_by_id('userName').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('verifyCode').send_keys('1234')
    driver.find_element_by_class_name('ant-btn').click()
    time.sleep(1)
    driver.find_element_by_class_name('ant-btn').click()
    # driver.execute_script()
    # driver.find_element_by_xpath().__setattr__()
    # driver.find_element_by_css_selector()
    time.sleep(1)
    yield driver
    driver.quit()

# if __name__ == '__main__':
#     # s= '2018-05-20 08:30:00'
#     # newtime = s.split(' ')
#     # n=newtime[0].split('-')
#     # print(n)
#     # if n[1].startswith('0'):
#     #     n[1]=n[1].replace('0','')
#     # if n[2].startswith('0'):
#     #     n[2]=n[2].replace('0','')
#     # t=f'{n[0]}年{n[1]}月{n[2]}日'
#     # print(t)
#     a = '2017-10-18 22:17:46'
#     b = '2017-10-19 22:17:40'
#     print(a > b)

