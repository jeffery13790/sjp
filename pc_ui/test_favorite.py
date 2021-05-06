from selenium.common.exceptions import NoSuchElementException
import time
import re
from selenium.webdriver.common.keys import Keys

import pytest

class TestClassFavorite():

    # 如果没有收藏的话，添加收藏
    def test_add_favorite(self, init_driver):

        # 定义收货地址数量
        num = 0
        # 点击用户信息
        try:
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="box"]//p[@class="username-p"]').click()
        except:
            raise NoSuchElementException("没有找到用户信息元素")

        try:
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="persone-center"]//a[contains(text(), "个人收藏")]').click()
        except:
            raise NoSuchElementException("点击收货地址")

        # 获取收藏数据的数量
        try:
            time.sleep(2)
            addNum = init_driver.find_element_by_xpath('//*[@id="my-favorite"]//span[contains(text(), "共收藏了")]').text
            if addNum:
                num = re.findall('\d', addNum)
                if num:
                    num = int(num[0])
        except:
            raise NoSuchElementException("获取收货地址数量的时候出错")

        #添加收藏
        try:
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]//input[@placeholder="明朝那些事"]').send_keys("红楼梦")
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]//input[@placeholder="明朝那些事"]').send_keys(Keys.ENTER)
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]//span[contains(text(), "搜索")]').click()
            time.sleep(2)
        except:
            raise NoSuchElementException("商品搜索的时候出错")

        #获取搜索出来的数据条数
        good_num = 0
        try:
            text = init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]//div[contains(text(), "共计")]').text
            temp = re.findall('\d',text)
            if temp:
                good_num = int(temp[0])
        except:
            raise NoSuchElementException("添加商品收藏的时候出错")

        if good_num == 0:
            raise NoSuchElementException("搜索的商品不存在，请换个商品重新搜索")
        else:
            try:

            # 点击商品，进入商品详情，稍后会进入点击收藏
                init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[2]/a[1]').click()
                time.sleep(3)
                init_driver.find_element_by_xpath('//*[@id="item-detail-show-w"]//div[contains(text(), "加入收藏")]').click()
                time.sleep(3)
            except:
                raise NoSuchElementException("该商品已经收藏了，请换一个商品再添加搜藏")

            try:
                init_driver.find_element_by_xpath('//*[@id="item-detail-show-w"]//div[contains(text(), "取消收藏")]')
                time.sleep(2)
            except:
                raise NoSuchElementException("搜藏失败")
        try:
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="box"]//a[contains(text(), "收藏夹")]').click()
        except:
            raise NoSuchElementException("收藏夹出现了问题")


        now_num = 0
        try:
            time.sleep(1)
            addNum = init_driver.find_element_by_xpath('//*[@id="my-favorite"]//span[contains(text(), "共收藏了")]').text
            if addNum:
                temp = re.findall('\d', addNum)
                if temp:
                    now_num = int(temp[0])
        except:
            raise NoSuchElementException("获取收货地址数量的时候出错")

        assert now_num >= num



     # 验证个人收藏
    def test_check_favorite_num(self, init_driver):
        init_driver = init_driver
        # 定义收货地址数量
        num = 0
        # 点击用户信息
        try:
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="box"]//p[@class="username-p"]').click()
        except:
            raise NoSuchElementException("没有找到用户信息元素")

        try:
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="persone-center"]//a[contains(text(), "个人收藏")]').click()
        except:
            raise NoSuchElementException("点击个人收藏")

        # 获取现有的收货地址数量
        try:
            time.sleep(2)
            addNum = init_driver.find_element_by_xpath('//*[@id="my-favorite"]//span[contains(text(), "共收藏了")]').text
            if addNum:
                num = re.findall('\d', addNum)
                if num:
                    num = int(num[0])
        except:
            raise NoSuchElementException("获取收货地址数量的时候出错")

        #获取收藏的商品列表
        try:
            time.sleep(2)
            goods = init_driver.find_elements_by_xpath('//*[@id="my-favorite"]/div[2]/div')
            assert num == len(goods)
        except:
            raise NoSuchElementException("在获取收藏列表的时候出错")



    # 当有收藏的商品的时候，取消收藏
    def test_cancel_favorite(self, init_driver):
        # 收藏的商品数量
        num = 0
        # 点击用户信息
        try:
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="box"]//a[contains(text(), "收藏夹")]').click()
        except:
            raise NoSuchElementException("没有找到用户信息元素")

        # 获取收藏数据的数量
        try:
            time.sleep(9)
            addNum = init_driver.find_element_by_xpath('//*[@id="my-favorite"]//span[contains(text(), "共收藏了")]').text
            if addNum:
                num = re.findall('\d', addNum)
                if num:
                    num = int(num[0])
        except:
            raise NoSuchElementException("获取收货地址数量的时候出错")

        if num == 0:
            raise NoSuchElementException("没有收藏产品")
        else:
            try:
                time.sleep(1)
                init_driver.find_element_by_xpath('//*[@id="my-favorite"]//span[contains(text(), "批量管理")]').click()
            except:
                raise NoSuchElementException("点击批量管理的时候出错了")

            try:
                time.sleep(2)
                init_driver.find_element_by_xpath('//*[@id="my-favorite"]/div[1]//label//input[@type="checkbox"]').click()
                time.sleep(2)
                init_driver.find_element_by_xpath('//*[@id="my-favorite"]//span[contains(text(), "取消收藏")]').click()
            except:
                raise NoSuchElementException("取消收藏失败")

            try:
                time.sleep(2)
                addNum = init_driver.find_element_by_xpath(
                    '//*[@id="my-favorite"]//span[contains(text(), "共收藏了")]').text
                if addNum:
                    temp = re.findall('\d', addNum)
                    if temp:
                        now_num = int(temp[0])
            except:
                raise NoSuchElementException("获取收货地址数量的时候出错")

            assert now_num == 0
