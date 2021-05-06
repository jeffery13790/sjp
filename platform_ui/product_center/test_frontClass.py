import pytest
from selenium.common.exceptions import NoSuchElementException
import time
import re
from selenium.webdriver.common.keys import Keys
# ('金字塔原理','',''),('','电视',''),('','','新华电商')
front_data=[('','2020-07-28 00:00:00','2020-07-30 23:59:59')]
add_data=[('金字塔','1234')]
change_data=[('金字塔','1234')]
# 前台类目
class TestClassFrontClass():
    n = 0
    # 商品列表
    # @pytest.mark.skip
    @pytest.mark.parametrize('searchName,startTime,endTime',front_data)
    def test_search(self,init_driver,searchName,startTime,endTime ):
        driver = init_driver
        time.sleep(1)
        if TestClassFrontClass.n ==0 :


        # 点击商品中心
            driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title=driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[5]/a')
            # 点击前台类目
            if title:
                driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassFrontClass.n+=1

        # 时间格式转换
        # 转换成xxxx年x月x日的形式
        temp = startTime.split(' ')[0].split('-')
        if temp[1].startswith('0'):
            temp[1] = temp[1].replace('0', '')
        if temp[2].startswith('0'):
            temp[2] = temp[2].replace('0', '')
        searchStartTime = f'{temp[0]}年{temp[1]}月{temp[2]}日'


        temp1 = endTime.split(' ')[0].split('-')
        if temp1[1].startswith('0'):
            temp1[1] = temp1[1].replace('0', '')
        if temp1[2].startswith('0'):
            temp1[2] = temp1[2].replace('0', '')
        searchEndTime = f'{temp1[0]}年{temp1[1]}月{temp1[2]}日'

        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="qp-name-like"]').send_keys(searchName)

        driver.find_element_by_xpath('//*[@id="createTimeRange"]/span/input[1]').click()

        time.sleep(1)
        # driver.find_element_by_xpath('//td[@tittle="2020年7月29日"]/div').click()
        # 输入日期
        driver.find_element_by_xpath(f'//td[@title="{searchStartTime}"]/div').click()
        driver.find_element_by_xpath(f'//td[@title="{searchEndTime}"]/div').click()
        driver.find_element_by_xpath('//div/a[@class="ant-calendar-ok-btn" and @role="button"]').click()

        time.sleep(1)

        driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/section/main/div/div[2]/div/div/div/div[3]/div[1]/form/div/div[3]/span/button[1]').click()

        time.sleep(1)

        name_text = driver.find_element_by_xpath('//table/tbody/tr[1]/td[1]/span').text
        create_time=driver.find_element_by_xpath('//table/tbody/tr[1]/td[3]/span').text


        if searchName in name_text and create_time >= startTime  and  create_time <= endTime :
            assert True
        else:
            assert False


    # @pytest.mark.skip
    @pytest.mark.parametrize('addName,addInfo',add_data)
    def test_add_front(self,init_driver,addName,addInfo):
        driver = init_driver
        time.sleep(1)
        if TestClassFrontClass.n == 0:

            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title = driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[5]/a')
            # 点击前台类目
            if title:
                driver.find_element_by_xpath(
                    '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassFrontClass.n += 1

        # 点击新增按钮
        driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/section/main/div/div[2]/div/div/div/div[3]/div[2]/button').click()
        # 填写新增信息
        driver.find_element_by_xpath('//*[@id="name"]').send_keys(addName)
        driver.find_element_by_xpath('//*[@id="detail"]').send_keys(addInfo)
        time.sleep(1)
        driver.find_element_by_css_selector('button.ant-btn-primary:nth-child(2)').click()

        time.sleep(1
                   )
        name_text = driver.find_element_by_xpath('//table/tbody/tr[1]/td[1]/span').text
        info_text = driver.find_element_by_xpath('//table/tbody/tr[1]/td[2]/span').text
        # with open('platform_ui/product_center/txt','a') as f:
        #     f.write(name_text+'\n')
        #     f.write(info_text+'\n')
        #     f.write(addInfo+'\n')
        #     f.write(addName+'\n')

        if addName == name_text and addInfo == info_text :
            assert True
        else:
            assert False


    @pytest.mark.parametrize('changename,changeinfo', add_data)
    def test_change_front(self,init_driver,changename,changeinfo):
        driver = init_driver
        time.sleep(1)
        if TestClassFrontClass.n == 0:

            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title = driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[5]/a')
            # 点击前台类目
            if title:
                driver.find_element_by_xpath(
                    '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassFrontClass.n += 1
        # 点击编辑
        driver.find_element_by_xpath('//table/tbody/tr[1]/td[5]/a[1]/span').click()
        time.sleep(1)
        name = driver.find_element_by_id('name')
        name.clear()
        name.send_keys(changename)

        detail=driver.find_element_by_id('detail')
        detail.clear()
        detail.send_keys(changeinfo)

        time.sleep(1)
        driver.find_element_by_css_selector('button.ant-btn-primary:nth-child(2)').click()

        time.sleep(1)

        name_text = driver.find_element_by_xpath('//table/tbody/tr[1]/td[1]/span').text
        info_text = driver.find_element_by_xpath('//table/tbody/tr[1]/td[2]/span').text

        # with open('txt', 'a') as f:
        #     f.write(name_text + '\n')
        #     f.write(info_text + '\n')

        time.sleep(1)

        if changename == name_text and changeinfo == info_text:
            assert True
        else:
            assert False

    def test_open(self, init_driver, ):
        driver = init_driver
        time.sleep(1)
        if TestClassFrontClass.n == 0:

            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title = driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[5]/a')
            # 点击前台类目
            if title:
                driver.find_element_by_xpath(
                    '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassFrontClass.n += 1

        driver.find_element_by_xpath('//table/tbody/tr[1]/td[5]/span/a').click()
        time.sleep(1)

        driver.find_element_by_css_selector('button.ant-btn-sm:nth-child(1)').click()

        assert True

    def test_copy(self, init_driver, ):
        driver = init_driver
        time.sleep(1)
        if TestClassFrontClass.n == 0:

            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title = driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[5]/a')
            # 点击前台类目
            if title:
                driver.find_element_by_xpath(
                    '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassFrontClass.n += 1

        driver.find_element_by_xpath('//table/tbody/tr[1]/td[5]/a[2]').click()
        time.sleep(1)

        driver.find_element_by_css_selector('.ant-modal-footer > button:nth-child(1)').click()
