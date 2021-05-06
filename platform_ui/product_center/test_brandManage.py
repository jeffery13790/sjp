import pytest
from selenium.common.exceptions import NoSuchElementException
import time
import re
import os
from selenium.webdriver.common.keys import Keys
# ('XHSKU82','','',''),('','我不知道我是谁','',''),('','','漫画',''),('','','','新华电商')
tag_data=[('新华','我不知道','platform_ui/product_center/picture/fish.png')]
tag_change_data=[('修改名称','platform_ui/product_center/picture/girl.jpg')]
# 品牌管理
class TestClassBrand():
    n=0
    # 商品列表
    # @pytest.mark.skip
    @pytest.mark.parametrize('brandName,addBrandName,picture',tag_data)
    def test_sku(self,init_driver,brandName,addBrandName,picture):
        driver = init_driver
        time.sleep(1)

        if TestClassBrand.n == 0 :
            # 点击商品中心
            driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title = driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[4]/a')
            # 点击品类管理
            if title:
                driver.find_element_by_xpath(
                    '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()

            time.sleep(1)
            TestClassBrand.n +=1

        # 品牌名称
        driver.find_element_by_xpath('//*[@id="qp-name-like"]').send_keys(brandName)
        time.sleep(1)
        # 点击查询
        driver.find_element_by_xpath('//form[@class="ant-form ant-form-inline"]/div[1]/div[2]/span/button[1]')
        time.sleep(1)

        name_text = driver.find_element_by_xpath('//table/tbody/tr[1]/td[2]').text

        if brandName in name_text :
            driver.find_element_by_xpath('//form[@class="ant-form ant-form-inline"]/div[1]/div[2]/span/button[2]')
            assert True



    @pytest.mark.parametrize('brandName,addBrandName,picture',tag_data)
    def test_add_brand(self,init_driver,brandName,addBrandName,picture):
        driver = init_driver
        picture_path=os.path.join(os.getcwd(),picture)

        if TestClassBrand.n == 0 :
            # 点击商品中心
            driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            # 点击品牌管理
            driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[4]/a').click()
            time.sleep(1)
            TestClassBrand.n +=1


        driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/section/main/div/div[2]/div/div/div/div[3]/div[2]/span/button').click()
        time.sleep(1)

        # 输入品牌名称
        driver.find_element_by_xpath('//*[@id="name"]').send_keys(addBrandName)
        time.sleep(1)

        #上传图片
        driver.find_element_by_xpath('//*[@id="logoUrl"]').send_keys(picture_path)
        time.sleep(1)

        # 点击确定
        driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div[3]/button[2]').click()
        time.sleep(1)

        name_text = driver.find_element_by_xpath('//table/tbody/tr[1]/td[2]').text

        if brandName in name_text:
            driver.find_element_by_xpath('//form[@class="ant-form ant-form-inline"]/div[1]/div[2]/span/button[2]')
            assert True

    # @pytest.mark.skip
    @pytest.mark.parametrize('changeName,changePicture', tag_change_data)
    def test_change_info(self,init_driver,changeName,changePicture):
        driver = init_driver
        picture_path = os.path.join(os.getcwd(), changePicture)

        if TestClassBrand.n == 0:
            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            # 点击品牌管理
            driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[4]/a').click()
            time.sleep(1)
            TestClassBrand.n += 1


        driver.find_element_by_xpath('//table/tbody/tr[1]/td[6]/a[1]/span').click()

        # 输入品牌名称
        driver.find_element_by_xpath('//*[@id="name"]').send_keys(changeName)
        time.sleep(1)

        # 上传图片
        driver.find_element_by_xpath('//input[@id="logoUrl"]').send_keys(picture_path)
        time.sleep(1)

        # 点击确认
        driver.find_element_by_css_selector('button.ant-btn-primary:nth-child(2)').click()
        # driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div[3]/button[2]').click()
        time.sleep(1)

        name_text = driver.find_element_by_xpath('//table/tbody/tr[1]/td[2]').text

        if changeName in name_text:
            driver.find_element_by_xpath('//form[@class="ant-form ant-form-inline"]/div[1]/div[2]/span/button[2]')
            assert True

    # @pytest.mark.skip
    def test_delete(self,init_driver):

        driver = init_driver

        if TestClassBrand.n == 0:
            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            # 点击品牌管理
            driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[4]/a').click()
            time.sleep(1)
            TestClassBrand.n += 1

        name_text = driver.find_element_by_xpath('//table/tbody/tr[1]/td[2]').text


        # 点击删除
        driver.find_element_by_xpath('//table/tbody/tr[1]/td[6]/a[2]/span').click()
        time.sleep(1)

        driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div/div/div[2]/button[2]').click()
        time.sleep(1)

        changed_name_text=driver.find_element_by_xpath('//table/tbody/tr[1]/td[2]').text

        if name_text != changed_name_text:
            assert True
        else:
            assert False