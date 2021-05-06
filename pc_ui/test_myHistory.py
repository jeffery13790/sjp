from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
import time
import re
from selenium.webdriver.common.keys import Keys
import io
import pytest
import random


class TestClassMyHistory():

    # 个人轨迹>> 这里面有个坑，没有考虑到足迹特别多的时候会导致分页的情况
    def test_delete_favorite(self, init_driver):
        # self.driver = init_driver
        # 定义收货地址数量
        num = 0
        # 点击用户信息
        try:
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="box"]//p[@class="username-p"]').click()
        except:
            raise NoSuchElementException("没有找到用户信息元素")

        #点击浏览足迹，然后进入到足迹信息中
        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="persone-center"]//a[contains(text(), "浏览足迹")]').click()
        except:
            raise NoSuchElementException("进入浏览足迹失败")

        # 获取现有浏览足迹的个数
        try:
            time.sleep(2)
            historys = self.driver.find_elements_by_xpath('//*[@id="myHistory"]/div[2]/ul/li/div[3]/div/div')
            num = len(historys)
        except:
            num = 0

        if num == 0:
            raise NoSuchElementException("没有浏览轨迹")
        else:
            try:
                historys = self.driver.find_elements_by_xpath('//*[@id="myHistory"]/div[2]/ul/li/div[3]/div/div')
                historys_num = len(historys)
                #删除该浏览足迹
                self.driver.find_element_by_xpath('//*[@id="myHistory"]/div[2]/ul/li/div[3]/div/div[1]/div[1]/i').click()
                now_historys = self.driver.find_elements_by_xpath('//*[@id="myHistory"]/div[2]/ul/li/div[3]/div/div')
                assert historys_num - 1 == len(now_historys)
                # self.driver.close()
            except:
                raise NoSuchElementException("没有获取到当前页面浏览足迹的元素")

    # 个人轨迹>> 这里面有个坑，没有考虑到足迹特别多的时候会导致分页的情况
    # @pytest.fixture()
    @pytest.mark.parametrize('good', ["明朝那些事", "红楼梦", "金字塔原理", "袁腾飞讲两宋风云", "不一样的卡梅拉14 我登上了逍遥岛"])
    def test_check_favorite_num(self, init_driver, good):
        self.driver = init_driver
        # 定义收货地址数量
        num = 0
        # 点击用户信息
        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="box"]//p[@class="username-p"]').click()
        except:
            raise NoSuchElementException("没有找到用户信息元素")

        #点击浏览足迹，然后进入到足迹信息中
        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="persone-center"]//a[contains(text(), "浏览足迹")]').click()
        except:
            raise NoSuchElementException("进入浏览足迹失败")

        # 获取现有浏览足迹的个数
        try:
            time.sleep(2)
            historys = self.driver.find_elements_by_xpath('//*[@id="myHistory"]/div[2]/ul/li/div[3]/div/div')
            num = len(historys)
        except:
            num = 0

        #再次浏览商品，搜索商品
        try:
            time.sleep(0.5)
            self.driver.find_element_by_xpath('//*[@id="search-wrapper"]//input[@placeholder="明朝那些事"]').send_keys(good)
            time.sleep(0.5)
            self.driver.find_element_by_xpath('//*[@id="search-wrapper"]//input[@placeholder="明朝那些事"]').send_keys(Keys.ENTER)
            time.sleep(0.5)
            self.driver.find_element_by_xpath('//*[@id="search-wrapper"]//span[contains(text(), "搜索")]').click()
        except:
            raise NoSuchElementException("搜索商品出错")

        try:
            time.sleep(0.5)
            self.driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[2]/a[1]').click()
        except:
            raise NoSuchElementException("进入商品详情的时候出错，请确认是否有商品被搜索出来")

        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="box"]//p[@class="username-p"]').click()
        except:
            raise NoSuchElementException("没有找到用户信息元素")

        #点击浏览足迹，然后进入到足迹信息中
        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="persone-center"]//a[contains(text(), "浏览足迹")]').click()
        except:
            raise NoSuchElementException("进入浏览足迹失败")

        try:
            time.sleep(2)
            historys = self.driver.find_elements_by_xpath('//*[@id="myHistory"]/div[2]/ul/li/div[3]/div/div')
            now_num = len(historys)
        except:
            raise NoSuchElementException("浏览的足迹没有保存到足迹中")

        assert now_num >= num



    # 个人轨迹>> 通过足迹进入到商品详情里面去
    def test_delete_favorite(self, init_driver):
        self.driver = init_driver
        # 定义收货地址数量
        num = 0
        # 点击用户信息
        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="box"]//p[@class="username-p"]').click()
        except:
            raise NoSuchElementException("没有找到用户信息元素")

        #点击浏览足迹，然后进入到足迹信息中
        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="persone-center"]//a[contains(text(), "浏览足迹")]').click()
        except:
            raise NoSuchElementException("进入浏览足迹失败")

        # 获取现有浏览足迹的个数
        try:
            time.sleep(2)
            historys = self.driver.find_elements_by_xpath('//*[@id="myHistory"]/div[2]/ul/li/div[3]/div/div')
            num = len(historys)
            historys[random.randint(1, num-1)].click()
        except:
            raise NoSuchElementException("没有找到用户信息")

        try:
            self.driver.find_element_by_xpath('//*[@id="item-detail-show-w"]//div[contains(text(), "收藏")]')
            self.driver.find_element_by_xpath('//*[@id="recommended-products"]//div[contains(text(), "推荐商品")]')
            assert True
        except:
            raise NoSuchElementException("没有成功的从足迹中进入到商品详情中来")
