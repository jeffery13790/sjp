from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import re
from selenium.webdriver import Chrome
import unittest
import pytest
class TestClassLogin():

    @pytest.mark.parametrize('good', ["明朝那些事", "红楼梦", "金字塔原理", "袁腾飞讲两宋风云", "不一样的卡梅拉14 我登上了逍遥岛"])
    def test_buy_goods(self, init_driver, good):

        #在搜索框中输入要搜索的商品
        try:
            time.sleep(0.4)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]//input[@placeholder="明朝那些事"]').send_keys(good)
            time.sleep(0.4)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]//input[@placeholder="明朝那些事"]').send_keys(Keys.ENTER)
        except:
            raise NoSuchElementException("商品搜索的时候出现了错误")
        #点击搜索按钮
        try:
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[2]').click()
        except:
            raise NoSuchElementException("点击搜索按钮的时候出错")
        #点击商品详情
        try:
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[2]/a[1]/div').click()
        except:
            raise NoSuchElementException("点击商品详情的时候出现了错误")
        #点击立即购买商品
        try:
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="item-detail-show-w"]//div[contains(text(), "立即购买")]').click()
        except:
            raise NoSuchElementException("立即购买商品的时候出现了错误")
        #点击去支付
        try:
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="order"]//div[contains(text(), "去支付")]').click()
        except:
            raise NoSuchElementException("去支付的时候出错了")
        time.sleep(5)
        assert True

    @pytest.mark.parametrize('good', ["明朝那些事", "红楼梦", "金字塔原理", "袁腾飞讲两宋风云", "不一样的卡梅拉14 我登上了逍遥岛"])  #
    def test_buy_goods_1(self, init_driver, good):
        #在搜索框中输入要搜索的商品
        try:
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]//input[@placeholder="明朝那些事"]').send_keys(good)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]//input[@placeholder="明朝那些事"]').send_keys(Keys.ENTER)
        except:
            raise NoSuchElementException("搜索商品出错")
        #点击搜索按钮
        try:
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[2]').click()
        except:
            raise NoSuchElementException("点击搜索的时候出错")
        #点击商品详情
        try:
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[2]/a[1]/div').click()
        except:
            raise NoSuchElementException("点击商品详情的时候错误")
        #点击立即购买商品
        try:
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="item-detail-show-w"]//div[contains(text(), "立即购买")]').click()
        except:
            raise NoSuchElementException("立即购买的时候出现了问题")
        #这里面有个判断是否设置默认地址，如果有地址则设置收货地址，如果没有收货地址则选择收货地址，或者添加收货地址
        try:
            time.sleep(0.5)
            init_driver.find_element_by_xpath('//*[@id="order"]//div[contains(text(), "默认地址")]').click()
        except:
            #如果没有的话，可以
            raise NoSuchElementException("设置默认地址失败")

        try:
            time.sleep(5)
            init_driver.find_element_by_xpath('//div[@class="order-foot-pay-btn" and contains(text(), "去支付")]').click()
        except:
            raise NoSuchElementException("点击去支付的时候出现了问题")
        try:
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="pay"]/div[3]/div/div[contains(text(), "选择以下方式付款")]')
            assert True
        except:
            assert False