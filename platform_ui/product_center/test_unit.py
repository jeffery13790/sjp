import pytest
from selenium.common.exceptions import NoSuchElementException
import time
import re

# ('金字塔原理','',''),('','电视',''),('','','新华电商')
search_data=[('件')]
add_data=[('我和你','15')]
change_data=[('自动化跑起来','1879')]
# 品类管理
class TestUnit():
    n = 0
    # 商品列表
    # @pytest.mark.skip
    @pytest.mark.parametrize('unitName',search_data)
    def test_search(self,init_driver,unitName ):
        driver = init_driver
        time.sleep(1)
        if TestUnit.n ==0 :

        # 点击商品中心
            driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title=driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[9]/a')
            # 点击属性管理
            if title:
                driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestUnit.n+=1
        # 输入查询单位名称
        driver.find_element_by_id('qp-name-like').send_keys(unitName)

        # 点击查询
        driver.find_element_by_css_selector('button.ant-btn-two-chinese-chars:nth-child(1)').click()
        time.sleep(1)
        name_text = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[3]').text

        if unitName in name_text:
            driver.find_element_by_css_selector('button.ant-btn:nth-child(2)').click()
            assert True
        else:
            driver.find_element_by_css_selector('button.ant-btn:nth-child(2)').click()
            assert False


    @pytest.mark.parametrize('addName,addCode',add_data)
    def test_add(self,init_driver,addName,addCode):
        driver = init_driver
        time.sleep(1)
        if TestUnit.n ==0 :

        # 点击商品中心
            driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title=driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[9]/a')
            # 点击属性管理
            if title:
                driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestUnit.n+=1

        driver.find_element_by_css_selector('.antd-pro-components-show-table-index-tableListOperator > span:nth-child(1) > button:nth-child(1)').click()
        time.sleep(1)

        driver.find_element_by_id('name').send_keys(addName)
        driver.find_element_by_id('packagingCode').send_keys(addCode)
        driver.find_element_by_css_selector('button.ant-btn-primary:nth-child(2)').click()
        time.sleep(1)

        name_text = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[3]').text
        code_text=driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[2]').text

        if addName == name_text and addCode == code_text :
            assert True
        else:
            assert False

    @pytest.mark.parametrize('changeName,changeCode', change_data)
    def test_edit(self, init_driver, changeName, changeCode):
        driver = init_driver
        time.sleep(1)
        if TestUnit.n == 0:

            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title = driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[9]/a')
            # 点击属性管理
            if title:
                driver.find_element_by_xpath(
                    '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestUnit.n += 1

        driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[4]/a[1]/span').click()
        time.sleep(1)

        temp=driver.find_element_by_id('name')
        temp.clear()
        temp.send_keys(changeName)

        temp=driver.find_element_by_id('packagingCode')
        temp.clear()
        temp.send_keys(changeCode)

        driver.find_element_by_css_selector('.ant-modal-footer > button:nth-child(2)').click()
        time.sleep(1)

        name_text = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[3]').text
        code_text = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[2]').text

        if changeName == name_text and changeCode == code_text:
            assert True
        else:
            assert False

    def test_delete(self, init_driver):
        driver = init_driver
        time.sleep(1)
        if TestUnit.n == 0:

            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title = driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[9]/a')
            # 点击属性管理
            if title:
                driver.find_element_by_xpath(
                    '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestUnit.n += 1

        name_text1 = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[3]').text
        driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[4]/a[2]/span').click()
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div/div/div[2]/button[2]').click()
        time.sleep(1)

        name_text2 = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[3]').text

        if name_text2 != name_text1:
            assert True
        else:
            assert False