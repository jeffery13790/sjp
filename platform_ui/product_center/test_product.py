import pytest
from selenium.common.exceptions import NoSuchElementException
import time
import re
from selenium.webdriver.common.keys import Keys
# ('金字塔原理','',''),('','电视',''),('','','新华电商')
productlist_data=[('金字塔原理','',''),('','电视',''),('','','新华电商')]
# 商品列表

class TestClassProduct():
    n = 0
    # 商品列表
    # @pytest.mark.skip
    @pytest.mark.parametrize('productname,productclass,productbrand',productlist_data)
    def test_procustlist(self,init_driver,productname,productclass,productbrand ):
        driver = init_driver
        time.sleep(1)
        if TestClassProduct.n ==0 :

        # 点击商品中心
            driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title=driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[1]/a')
            # 点击商品列表
            if title:
                driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassProduct.n+=1

        # 输入商品名称
        if productname :
            driver.find_element_by_xpath('//*[@id="qp-name-like"]').send_keys(productname)
            time.sleep(1)
        # 输入商品品类
        if productclass :
            driver.find_element_by_xpath('/html/body/div[1]/div/section/section/main/div/div[2]/div/div/div/div/div[3]/div[1]/div[2]/div/div/div[1]/form/div/div[2]/div/div[2]/div/span/div/div/div').click()
            time.sleep(1)
            driver.find_element_by_xpath(f'//li[text()="{productclass}"]').click()
            time.sleep(1)
        # 输入商品品牌
        if productbrand :
            driver.find_element_by_xpath('/html/body/div[1]/div/section/section/main/div/div[2]/div/div/div/div/div[3]/div[1]/div[2]/div/div/div[1]/form/div/div[3]/div/div[2]/div/span/div/div/div/div').click()
            driver.find_element_by_xpath(f'//li[text()="{productbrand}"]').click()
         # 点击搜索
        driver.find_element_by_xpath('/html/body/div[1]/div/section/section/main/div/div[2]/div/div/div/div/div[3]/div[1]/div[2]/div/div/div[1]/form/div/div[4]/span/button[1]').click()
        # driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/section/main/div/div[2]/div/div/div/div/div[3]/div[1]/div[2]/div/div/div[1]/form/div/div[4]/span/button[1]').click()
        time.sleep(1)
        #
        name_text=driver.find_element_by_xpath('//table[@class="ant-table-fixed"]/tbody/tr[1]/td[2]/a').text
        class_text=driver.find_element_by_xpath('//table[@class="ant-table-fixed"]/tbody/tr[1]/td[4]').text
        # with open('txt','a') as f:
        #     f.write(name_text+'\n')
        #     f.write(class_text +'\n')
        time.sleep(1)
        # name_text=driver.find_element_by_css_selector('tr.ant-table-row:nth-child(1) > td:nth-child(2) > a:nth-child(1)').text
        # class_text=driver.find_element_by_css_selector('tr.ant-table-row:nth-child(1) > td:nth-child(4)').text
        # '/html/body/div[1]/div/section/section/main/div/div[2]/div/div/div/div/div[3]/div[1]/div[2]/div/div/div[3]/div[2]/div/div/div/div/div/div/div/table/tbody/tr[1]/td[2]'
        if productname in name_text and productclass in class_text :
            driver.find_element_by_xpath('//div[@class="ant-row"]/div[4]/span/button[2]').click()
            time.sleep(1)
            assert True
        else:
            driver.find_element_by_xpath('//div[@class="ant-row"]/div[4]/span/button[2]').click()

            assert False

    # @pytest.mark.skip
    def test_view(self,init_driver):
        driver = init_driver
        time.sleep(1)

        # # 点击商品中心
        # driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
        # time.sleep(1)

        # 点击商品列表
        driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[1]/a').click()
        time.sleep(1)

        # 点击查看按钮
        driver.find_element_by_xpath('//table[@class="ant-table-fixed"]/tbody/tr[1]/td[7]/a/span').click()
        time.sleep(1)
        # 返回按钮
        flag=driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/section/main/div/div[1]/div/div[2]/span/button')

        if flag :
            assert True
        else:
            assert False


    def test_turnoff(self,init_driver):
        driver = init_driver
        time.sleep(1)

        # # 点击商品中心
        # driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
        # time.sleep(1)

        # 点击商品列表
        driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[1]/a').click()
        time.sleep(1)

        # 点击禁用按钮
        driver.find_element_by_xpath('//table[@class="ant-table-fixed"]/tbody/tr[1]/td[7]/span/a/span').click()
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div/div/div[2]/button[2]').click()
        time.sleep(1)

        text=driver.find_element_by_xpath('//table[@class="ant-table-fixed"]/tbody/tr[1]/td[6]/span').text

        if text =='禁用':
            driver.find_element_by_xpath('//table[@class="ant-table-fixed"]/tbody/tr[1]/td[7]/span/a/span').click()
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div/div/div[2]/button[2]').click()
            assert True
        else:
            assert False


