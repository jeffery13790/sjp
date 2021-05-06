import pytest
from selenium.common.exceptions import NoSuchElementException
import time
import re

from selenium.webdriver.common.keys import Keys
# ('XHSKU82','','',''),('','我不知道我是谁','',''),('','','漫画',''),('','','','新华电商')
sku_data=[('XHSKU82','','',''),('','我不知道我是谁','',''),('','','漫画',''),('','','','新华电商')]

# sku管理
class TestClassSku():
    n=0
    # 商品列表
    # @pytest.mark.skip
    @pytest.mark.parametrize('skuName,productName,skuClass,skuBrand',sku_data)
    def test_sku(self,init_driver,skuName,productName,skuClass,skuBrand ):
        driver = init_driver
        time.sleep(1)
        if TestClassSku.n == 0 :
            # 点击商品中心
            driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title=driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[3]/a')
            # 点击sku
            if title:
                driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassSku.n +=1

        # 输入sku编码
        if skuName :
            driver.find_element_by_xpath('//*[@id="qp-skuCode-like"]').send_keys(skuName)
            time.sleep(1)

        # 输入商品名称
        if productName:
            driver.find_element_by_xpath('//*[@id="qp-name-like"]').send_keys(productName)
            time.sleep(1)

        # 输入sku品类
        if skuClass :
            # driver.find_element_by_xpath('//*[@id="classIdsQueryIn"]/div/div/div').click()
            # time.sleep(1)
            driver.find_element_by_xpath('//input[@id="classIdsQueryIn"]').send_keys(skuClass)
            time.sleep(1)
            driver.find_element_by_xpath(f'//li[text()="{skuClass}"]').click()
            time.sleep(1)

        # 输入商品品牌
        if skuBrand :
            driver.find_element_by_xpath('//input[@id="brandIdsQueryIn"]').send_keys(skuBrand)
            driver.find_element_by_xpath(f'//li[text()="{skuBrand}"]').click()
            time.sleep(1)

         # 点击搜索
        driver.find_element_by_xpath('/html/body/div[1]/div/section/section/main/div/div[2]/div/div/div/div/div[3]/div[1]/div[2]/div/div/div[1]/form/div/div[5]/span/button[1]').click()
        time.sleep(1)
        #获取搜索出来第一行的信息
        sku_text=driver.find_element_by_xpath('//table[@class="ant-table-fixed"]/tbody/tr[1]/td[2]').text
        name_text=driver.find_element_by_xpath('//table[@class="ant-table-fixed"]/tbody/tr[1]/td[3]/span').text
        class_text=driver.find_element_by_xpath('//table[@class="ant-table-fixed"]/tbody/tr[1]/td[4]').text
        # with open('txt','a') as f:
        #     f.write(name_text+'\n')
        #     f.write(class_text +'\n')
        #     f.write(sku_text + '\n')
        time.sleep(1)
        if productName in name_text and skuClass in class_text and skuName in sku_text :
            driver.find_element_by_xpath('//*[@class="ant-row"]/div[5]/span/button[2]').click()
            time.sleep(1)
            assert True
        else:
            driver.find_element_by_xpath('//div[@class="ant-row"]/div[5]/span/button[2]').click()
            assert False







    # @pytest.mark.skip
    def test_view(self,init_driver):
        driver = init_driver

        if TestClassSku.n == 0 :
            # 点击商品中心
            driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)


            title=driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[3]/a')
            # 点击商品列表
            if title:
                driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassSku.n +=1


        # 点击查看按钮
        driver.find_element_by_xpath('//table[@class="ant-table-fixed"]/tbody/tr[1]/td[6]/a[1]/span').click()

        time.sleep(1)

        # 定位返回按钮
        try:
            flag = driver.find_element_by_css_selector('.ant-modal-footer > button:nth-child(1)')

            if flag :
                flag.click()

                assert True
            else:
                assert False
        except:
            raise print('查看的返回按钮定位错误')





    # @pytest.mark.skip
    def test_tag(self,init_driver):
        driver = init_driver

        if TestClassSku.n == 0 :
            # 点击商品中心
            driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)


            title=driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[3]/a')
            # 点击商品列表
            if title:
                driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassSku.n +=1

        # 点击标签管理
        driver.find_element_by_xpath('//table[@class="ant-table-fixed"]/tbody/tr[1]/td[6]/a[2]').click()
        time.sleep(1)

        # handles = driver.window_handles
        # driver.switch_to.window(handles[-1])

        try:
            # 确定按钮
            flag = driver.find_element_by_css_selector('button.ant-btn-primary:nth-child(2)')
            if  flag :
                flag.click()
                assert True
            else:
                assert False
        except:
            raise print('标签管理确认按钮没定位')
            # assert False


