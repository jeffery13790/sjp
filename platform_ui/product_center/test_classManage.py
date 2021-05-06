import pytest
from selenium.common.exceptions import NoSuchElementException
import time
import re

# ('金字塔原理','',''),('','电视',''),('','','新华电商')
search_data=[('电视')]
add_data=[('我和你','15')]
change_data=[('自动化跑起来','1879')]
# 品类管理
class TestClassManage():
    n = 0
    # 商品列表
    # @pytest.mark.skip
    @pytest.mark.parametrize('className',search_data)
    def test_search(self,init_driver,className ):
        driver = init_driver
        time.sleep(1)
        if TestClassManage.n ==0 :

        # 点击商品中心
            driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title=driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[7]/a')
            # 点击品类管理
            if title:
                driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassManage.n+=1
        # 输入品类名称
        driver.find_element_by_id('qp-name-like').send_keys(className)
        time.sleep(1)
        driver.find_element_by_css_selector('button.ant-btn-two-chinese-chars:nth-child(1)').click()
        time.sleep(1)
        # 获取搜索列表第一行的品类名称
        name_text = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[2]').text

        if className in name_text :
            driver.find_element_by_css_selector('button.ant-btn:nth-child(2)').click()
            driver.find_element_by_css_selector('button.ant-btn-two-chinese-chars:nth-child(1)').click()

            assert True
        else:
            assert False


    @pytest.mark.parametrize('addName,addCode',add_data)
    def test_add(self,init_driver,addName,addCode):
        driver = init_driver
        time.sleep(1)
        if TestClassManage.n ==0 :

        # 点击商品中心
            driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title=driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[7]/a')
            # 点击品类管理
            if title:
                driver.find_element_by_xpath('//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassManage.n+=1
        # 点击新增按钮
        driver.find_element_by_css_selector('.antd-pro-components-show-table-index-tableListOperator > span:nth-child(1) > button:nth-child(1)').click()
        time.sleep(1)

        driver.find_element_by_id('name').send_keys(addName)
        driver.find_element_by_id('taxRateCode').send_keys(addCode)
        time.sleep(1)
        # 新增品类税率
        driver.find_element_by_css_selector('.ant-btn-dashed').click()
        time.sleep(1)
        driver.find_element_by_css_selector('.ant-calendar-picker-input').click()
        time.sleep(1)
        driver.find_element_by_css_selector('.ant-calendar-today-btn').click()
        time.sleep(1)

        # 在新增一个后删除
        driver.find_element_by_css_selector('.ant-btn-dashed').click()
        driver.find_element_by_css_selector('tr.editable-row:nth-child(2) > td:nth-child(3) > span:nth-child(1) > a:nth-child(1)').click()
        time.sleep(1)
        driver.find_element_by_css_selector('button.ant-btn-sm:nth-child(2)').click()
        # 点击保存
        driver.find_element_by_css_selector('button.ant-btn-primary:nth-child(2)').click()
        time.sleep(1)

        name_text = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[2]').text

        if addName in name_text :
            assert True
        else:
            assert False

    @pytest.mark.parametrize('changeName,changeCode', change_data)
    def test_change(self, init_driver, changeName, changeCode):
        driver = init_driver
        time.sleep(1)
        if TestClassManage.n == 0:

            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title = driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[7]/a')
            # 点击品类管理
            if title:
                driver.find_element_by_xpath(
                    '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassManage.n += 1
        # 点击编辑
        driver.find_element_by_css_selector('tr.ant-table-row:nth-child(1) > td:nth-child(4) > a:nth-child(1) > span:nth-child(1)').click()
        time.sleep(1)
        # 修改数据
        name = driver.find_element_by_id('name')
        name.clear()
        name.send_keys(changeName)
        code = driver.find_element_by_id('taxRateCode')
        code.clear()
        code.send_keys(changeName)
        time.sleep(1)
        # 修改商品税率
        driver.find_element_by_css_selector('.ant-calendar-picker-input').click()
        time.sleep(1)
        driver.find_element_by_css_selector('.ant-calendar-today-btn').click()
        time.sleep(1)
        driver.find_element_by_css_selector('button.ant-btn-primary:nth-child(2)').click()

        time.sleep(1)
        name_text = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[2]').text

        if changeName in name_text:
            assert True
        else:
            assert False

    # @pytest.mark.parametrize('changeName,changeCode', change_data)
    def test_connect_attribute(self,init_driver):
        driver = init_driver
        time.sleep(1)
        if TestClassManage.n == 0:

            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title = driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[7]/a')
            # 点击品类管理
            if title:
                driver.find_element_by_xpath(
                    '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassManage.n += 1

        # 点击关联属性
        driver.find_element_by_css_selector('tr.ant-table-row:nth-child(1) > td:nth-child(4) > a:nth-child(5)').click()
        time.sleep(1)
        # 输入属性名称并查询
        driver.find_element_by_xpath('//*[@class="ant-modal-root"]//input[@id="qp-name-like"]').send_keys('作者')
        driver.find_element_by_xpath('//*[@class="ant-modal-root"]//button[@class="ant-btn ant-btn-primary ant-btn-two-chinese-chars"]').click()
        time.sleep(1)

        name_text =driver.find_element_by_xpath('//*[@class="ant-modal-root"]//tbody[@class="ant-table-tbody"]/tr[1]/td[2]').text

        if name_text == '作者':
            flag=True
        else:
            flag=False

        # 勾选第一栏
        driver.find_element_by_xpath('//*[@class="ant-modal-root"]//input[@class="ant-checkbox-input"]').click()
        # 点击确认
        driver.find_element_by_css_selector('.ant-modal-footer > button:nth-child(2)').click()
        # 点击属性管理
        driver.find_element_by_css_selector('tr.ant-table-row:nth-child(1) > td:nth-child(4) > a:nth-child(7)').click()
        time.sleep(1)

        name_text =driver.find_element_by_xpath('//*[@class="ant-modal-root"]//tbody[@class="ant-table-tbody"]/tr[1]/td[2]').text

        if name_text == '作者'and flag:
            driver.find_element_by_css_selector('.anticon-close').click()
            assert True
        else:
            driver.find_element_by_css_selector('.anticon-close').click()
            assert False

    def test_delete(self, init_driver):
        driver = init_driver
        time.sleep(1)
        if TestClassManage.n == 0:

            # 点击商品中心
            driver.find_element_by_xpath(
                '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
            time.sleep(1)

            title = driver.find_element_by_xpath('//*[@id="/commodity$Menu"]/li[7]/a')
            # 点击品类管理
            if title:
                driver.find_element_by_xpath(
                    '//*[@id="root-slave"]/div/section/aside/div/ul/li[2]/div[1]/span/span').click()
                title.click()
            time.sleep(1)
            TestClassManage.n += 1

        class_name_text = driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[2]').text

        # 点击属性管理
        driver.find_element_by_css_selector('tr.ant-table-row:nth-child(1) > td:nth-child(4) > a:nth-child(7)').click()
        time.sleep(1)
        # 获取第一行的属性名称
        attribute_name_text = driver.find_element_by_xpath(
            '//*[@class="ant-modal-root"]//tbody[@class="ant-table-tbody"]/tr[1]/td[2]').text

        # 点击列表第一行的删除关联属性按钮
        driver.find_element_by_xpath('//*[@class="ant-modal-root"]//tbody[@class="ant-table-tbody"]/tr[1]/td[5]/a').click()
        time.sleep(1)
        # 确认删除
        driver.find_element_by_css_selector('button.ant-btn-primary:nth-child(2)').click()
        time.sleep(1)

        try:
            changed_attribute_name_text=driver.find_element_by_xpath(
                '//*[@class="ant-modal-root"]//tbody[@class="ant-table-tbody"]/tr[1]/td[2]').text

        except :
            changed_attribute_name_text = '没有数据'


        if attribute_name_text == changed_attribute_name_text :
            flag1 = False
        else:
            flag1 = True
        time.sleep(1)
        # 退出属性管理页面
        driver.find_element_by_css_selector('.anticon-close').click()
        time.sleep(1)
        # 点击删除品类按钮
        driver.find_element_by_css_selector('tr.ant-table-row:nth-child(1) > td:nth-child(4) > a:nth-child(3) > span:nth-child(1)').click()
        time.sleep(1)
        driver.find_element_by_css_selector('button.ant-btn-primary:nth-child(2)').click()
        time.sleep(1)

        change_class_name_text=driver.find_element_by_xpath('//tbody[@class="ant-table-tbody"]/tr[1]/td[2]').text

        if class_name_text == change_class_name_text :
            flag2 = False
        else:
            flag2 = True

        if flag1 and flag2 :
            assert True
        else:
            assert False