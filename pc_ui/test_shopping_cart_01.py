from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys
import re
from decimal import Decimal
import copy
import pytest

class TestClassShoppingCart_01():

    def get_num(self, text):
        num_data = re.findall('\d', text)
        if num_data:
            return int(num_data[0])
        else:
            return 0

    def get_price(self, text):
        price = re.findall('\d+\.?\d+', text)
        if price:
            return float(price[0])
        else:
            return 0.00

    def get_reduction(self, text):
        price = re.findall('\d+\.?\d+', text)
        if len(price) == 2:
            return (float(price[0]), float(price[1]))
        else:
            return (0,0)


    @pytest.mark.parametrize('good_name', ['明朝那些事', '金字塔原理', '袁腾飞讲两宋风云', '不一样的卡梅拉14 我登上了逍遥岛'])
    def test_shopping_cart_003(self, init_driver, good_name):
        num = 0
        goods = []
        try:
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]//span[contains(text(), "购物车")]').click()
        except:
            raise NoSuchElementException("进入到购物车出错了")

        try:
            time.sleep(2)
            text = init_driver.find_element_by_xpath('//*[@id="shopping"]//div[contains(text(), "全部商品")]').text
            num = self.get_num(text)
        except:
            raise NoSuchElementException("获取商品的个数错误")

        # 如果没有商品的话则进行查找商品软后加入到购物车
        if not num:
            try:
                init_driver.find_element_by_xpath(
                    '//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(good_name)
                time.sleep(0.5)
                init_driver.find_element_by_xpath(
                    '//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[2]').click()
                time.sleep(5)
            except:
                raise NoSuchElementException("搜索商品出问题了")

            try:
                time.sleep(4)
                text = init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[1]/span').text
                time.sleep(2)
                good_num_seach = self.get_num(text)
                if good_num_seach:
                    raise NoSuchElementException("没有搜索到商品，请换一个商品再次操作")
                time.sleep(2)
                init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[2]/a[1]').click()

            except:
                raise NoSuchElementException("进入到商品详情的时候出错了")

            try:
                time.sleep(2)
                init_driver.find_element_by_xpath(
                    '//*[@id="item-detail-show-w"]//div[contains(text(), "加入购物车")]').click()

            except:
                raise NoSuchElementException("加入购物车失败")

            # 进入购物车
            try:
                time.sleep(1)
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/span/span').click()

            except:
                raise NoSuchElementException("进入购物车失败")

        try:
            time.sleep(5)
            temp = init_driver.find_element_by_xpath('//*[@id="shopping"]//div[contains(text(), "全部商品")]').text
            num = self.get_num(temp)
            if not num:
                raise NoSuchElementException("商品加入购物车失败")
        except:
            raise NoSuchElementException("获取商品数量出错")

        try:
            status = init_driver.find_element_by_xpath('//*[@id="shopping"]/div[3]/div/div[1]/label').get_attribute(
                'class')
            if not status.__contains__("ivu-checkbox-wrapper-checked"):
                init_driver.find_element_by_xpath('//*[@id="shopping"]/div[3]/div/div[1]/label').click()

        except:
            raise NoSuchElementException("全选商品出错")

        goods_list = init_driver.find_elements_by_xpath('//*[@id="shopping"]/div[2]/div[3]/div')
        good = {}
        for good_datil in goods_list:
            good_name = good_datil.find_element_by_xpath('./div/div[2]/div[2]/p').text
            good_num = good_datil.find_element_by_xpath('./div/div[2]/div[4]/div/div[2]/input').get_attribute('value')
            good_price = self.get_price(good_datil.find_element_by_xpath('./div/div[2]/div[3]/div[2]').text)
            good_all_price = self.get_price(good_datil.find_element_by_xpath('./div/div[2]/div[5]').text)

            assert good_all_price == int(good_num) * good_price
            try:
                huodongleixing = good_datil.find_element_by_xpath('./div[2]/div[1]').text
                if "满减" in huodongleixing:
                    activeName = "reduction"
                    active = self.get_reduction(good_datil.find_element_by_xpath('./div[2]/div[2]').text)

                elif "限时特价" in huodongleixing:
                    activeName = "specialOffer"
                    active = self.get_price(good_datil.find_element_by_xpath('./div[3]/div[1]/div/div/div[2]').text)
                elif "限时折扣" in huodongleixing:
                    activeName = "discount"
                    active = self.get_price(good_datil.find_element_by_xpath('./div[3]/div[1]/div/div/div[2]').text)
            except:
                activeName = "standard"
                active = "standard"
                pass
            good = {"name" : good_name, 'price' : good_price, "all_price" : good_all_price, "good_num" : int(good_num), "activeName" : activeName, "active_value": active}
            goods.append(good)
        datas = copy.deepcopy(goods)
        total_price = 0
        try:
            total_price = float(
                init_driver.find_element_by_xpath('//*[@id="shopping"]/div[3]/div/div[4]/div[2]/span').text)
        except:
            raise NoSuchElementException("获取总价格失败")


        total = 0
        for good in datas:
            if "reduction".__eq__(good.get('activeName', " ")):
                price = good.get('all_price', 0)
                temp1 = good.get("active_value")[0]
                temp2 = good.get("active_value")[1]
                while price > temp1:
                    price = price - temp2
                total = Decimal(total) + Decimal(price)
            elif "specialOffer".__eq__(good.get("activeName", " ")):
                total = Decimal(total) + Decimal(good.get('active_value', 0)) * Decimal(int(good.get("good_num", 0)))
            elif "discount".__eq__(good.get("activeName", " ")):
                total = Decimal(total) + Decimal(good.get("all_price", 0)) * Decimal(good.get("active_value", 0)) * Decimal(0.1)
            else:
                total = Decimal(total) + Decimal(good.get('all_price', 0))
        assert total.quantize(Decimal('0.00')).__str__() == Decimal(total_price).quantize(Decimal('0.00')).__str__()

