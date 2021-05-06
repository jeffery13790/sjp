import pytest
from selenium.common.exceptions import NoSuchElementException
import time
import re

# ('金字塔原理','',''),('','电视',''),('','','新华电商')
search_data=[('测试属性')]
add_data=[('我和你')]
change_data=[('自动化跑起来')]
# 属性管理
class TestAttributeManage():
    n = 0
    # 商品列表
    # @pytest.mark.skip
    @pytest.mark.parametrize('searchName',search_data)
    def test_search(self,init_driver,searchName ):
        driver = init_driver
        time.sleep(1)
        if TestAttributeManage.n ==0 :

        # 点击商品中心
            driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)
        # 点击属性管理
            title = driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[8]/a').click()
            if title:
                driver.find_element_by_xpath(
                    '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestAttributeManage.n+=1

        driver.find_element_by_id('qp-name-like').send_keys(searchName)

        driver.find_element_by_css_selector('button.ant-btn-two-chinese-chars:nth-child(1)').click()
        time.sleep(1)

        try:
            name_text=driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr/td[2]').text
        except:
            name_text=None


        if searchName in name_text :
            driver.find_element_by_css_selector('button.ant-btn:nth-child(2)').click()
            driver.find_element_by_css_selector('button.ant-btn-two-chinese-chars:nth-child(1)').click()
            assert True
        else:
            driver.find_element_by_css_selector('button.ant-btn:nth-child(2)').click()
            driver.find_element_by_css_selector('button.ant-btn-two-chinese-chars:nth-child(1)').click()
            assert False


    @pytest.mark.parametrize('addname',add_data)
    def test_add(self, init_driver, addname):
        driver = init_driver
        time.sleep(1)
        if TestAttributeManage.n == 0:
            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)
            # 点击属性管理
            driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[8]/a').click()

            time.sleep(1)
            TestAttributeManage.n += 1

        driver.find_element_by_xpath('//*[@class="antd-pro-components-show-table-index-tableListOperator"]/span/button').click()
        driver.find_element_by_id('name').send_keys(addname)
        time.sleep(1)
        # 创建第一个属性
        driver.find_element_by_xpath('//*[@class="ant-col ant-col-18 ant-form-item-control-wrapper"]/div/span/button').click()
        time.sleep(1)
        driver.find_element_by_id("value").send_keys('属性名称')
        time.sleep(1)
        # driver.find_element_by_css_selector('body > div:nth-child(8) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2)').click()
        driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()
        # 创建第二个属性
        time.sleep(1)
        driver.find_element_by_xpath('//*[@class="ant-col ant-col-18 ant-form-item-control-wrapper"]/div/span/button').click()
        time.sleep(1)
        driver.find_element_by_id("value").send_keys('需要删除的属性')
        # driver.find_element_by_css_selector('body > div:nth-child(8) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2)').click()
        driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()

        # 编辑第一个属性名称
        time.sleep(1)
        driver.find_element_by_xpath('//*[@class="ant-table-content"]//*[@class="ant-table-tbody"]/tr[1]/td[3]/button[1]').click()
        time.sleep(1)
        temp=driver.find_element_by_id("value")
        temp.clear()
        temp.send_keys("修改属性")
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@class="ant-table-content"]//*[@class="ant-table-tbody"]/tr[1]/td[3]/button[2]').click()
        time.sleep(1)
        driver.find_element_by_css_selector('button.ant-btn-sm:nth-child(2)').click()
        time.sleep(1)
        driver.find_element_by_css_selector('button.ant-btn-primary:nth-child(2)').click()
        time.sleep(1)
        name_text = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr/td[2]').text

        if addname in name_text :
            assert True
        else:
            assert False

    def test_view(self, init_driver):
        driver = init_driver
        time.sleep(1)
        if TestAttributeManage.n == 0:
            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)
            # 点击属性管理
            driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[8]/a').click()

            time.sleep(1)
            TestAttributeManage.n += 1
        # 点击查看详情
        driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr/td[6]/a[1]/span').click()
        time.sleep(1)

        try:
            close_button=driver.find_element_by_css_selector('.ant-modal-close-x')
            if close_button:
                close_button.click()
                assert True
            else:
                assert False
        except:
            raise print('未打开查看页面')

    @pytest.mark.parametrize('changeName',change_data)
    def test_edit(self, init_driver,changeName):
        driver = init_driver
        time.sleep(1)
        if TestAttributeManage.n == 0:
            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)
            # 点击属性管理
            driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[8]/a').click()

            time.sleep(1)
            TestAttributeManage.n += 1
        # 点击编辑
        driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr/td[6]/a[2]/span').click()
        time.sleep(1)

        attribute_name=driver.find_element_by_id('name')
        attribute_name.clear()
        attribute_name.send_keys(changeName)
        # 创建第二个属性
        time.sleep(1)
        driver.find_element_by_xpath(
            '//*[@class="ant-col ant-col-18 ant-form-item-control-wrapper"]/div/span/button').click()
        time.sleep(1)
        driver.find_element_by_id("value").send_keys('删除的属性')
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()

        # 编辑第一个属性名称
        time.sleep(1)
        driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[2]/button[1]').click()
        time.sleep(1)
        temp = driver.find_element_by_id("value")
        temp.clear()
        temp.send_keys("修改属性2")
        driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()
        time.sleep(1)
        # 删除一个属性
        driver.find_element_by_xpath(
            '//tbody[@class="ant-table-tbody"]/tr[1]/td[2]/button[2]').click()
        time.sleep(1)
        driver.find_element_by_css_selector('button.ant-btn-sm:nth-child(2)').click()
        time.sleep(1)
        driver.find_element_by_css_selector('button.ant-btn-primary:nth-child(2)').click()
        time.sleep(1)
        name_text = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr/td[2]').text

        if changeName in name_text :
            assert True
        else:
            assert False

    def test_delete(self, init_driver):
        driver = init_driver
        time.sleep(1)
        if TestAttributeManage.n == 0:
            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)
            # 点击属性管理
            driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[8]/a').click()

            time.sleep(1)
            TestAttributeManage.n += 1

        name_text1 = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr/td[2]').text

        # 点击删除
        driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr/td[6]/a[3]/span').click()
        time.sleep(1)
        driver.find_element_by_css_selector('button.ant-btn-primary:nth-child(2)').click()
        time.sleep(1)
        name_text2 = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr/td[2]').text

        if name_text1 != name_text2 :
            assert True
        else:
            assert False
