from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
import re
from decimal import Decimal
import pytest
class TestClassShoppingCart():

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


    #网购物车中添加产品, 购物车中没有商品，重新添加商品
    @pytest.mark.parametrize('good', ["明朝那些事", "红楼梦", "金字塔原理", "袁腾飞讲两宋风云", "不一样的卡梅拉14 我登上了逍遥岛"])
    def test_shopping_cart_001(self, init_driver, good):
        num = 0
        #点击购物车，从主页进入到购物车查看购物车里的商品
        try:
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]//span[contains(text(), "购物车")]').click()
        except:
            raise NoSuchElementException("进入到购物车出错了")

        try:
            time.sleep(5)
            text = init_driver.find_element_by_xpath('//*[@id="shopping"]//div[contains(text(), "全部商品")]').text
            num = self.get_num(text)
        except:
            raise NoSuchElementException("获取商品的个数错误")

        #如果购物车中有商品的话，则删除全部的商品然后再添加，
        if num:
            try:
                time.sleep(5)
                status = init_driver.find_element_by_xpath('//*[@id="shopping"]/div[3]/div/div[1]/label').get_attribute(
                    'class')
                if not status.__contains__("ivu-checkbox-wrapper-checked"):
                    init_driver.find_element_by_xpath('//*[@id="shopping"]/div[3]/div/div[1]/label').click()
            except:
                raise NoSuchElementException("全选商品出错")

            try:
                time.sleep(5)
                init_driver.find_element_by_xpath('//*[@id="shopping"]/div[3]/div/div[2]').click()
                time.sleep(4)
                init_driver.find_element_by_xpath('//button[2]/span[contains(text(), "确定")]').click()
                time.sleep(2)
            except:
                raise NoSuchElementException("购物车中的商品全部清空失败")

        try:
            time.sleep(2)
            text = init_driver.find_element_by_xpath('//*[@id="shopping"]//div[contains(text(), "全部商品")]').text
            num = self.get_num(text)
        except:
            raise NoSuchElementException("获取商品的个数错误")
        if num > 0 :
            raise NoSuchElementException("删除商品出错")

        # 如果没有商品的话则进行查找商品软后加入到购物车
        try:
            time.sleep(1)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(good)
            time.sleep(1)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(Keys.ENTER)
            time.sleep(1)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[2]').click()
        except:
            raise NoSuchElementException("搜索商品出问题了")

        try:
            time.sleep(5)
            text = init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[1]').text
            if not self.get_num(text):
                raise NoSuchElementException("没有搜索到商品，请换一个商品再次操作")
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[2]/a[1]').click()
        except:
            raise NoSuchElementException("进入到商品详情的时候出错了")

        try:
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="item-detail-show-w"]//div[contains(text(), "加入购物车")]').click()
        except:
            raise NoSuchElementException("加入购物车失败")

        #进入购物车
        try:
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/span/span').click()
            time.sleep(5)
        except:
            raise NoSuchElementException("进入购物车失败")
        time.sleep(5)
        temp = init_driver.find_element_by_xpath('//*[@id="shopping"]//div[contains(text(), "全部商品")]').text
        now_num = self.get_num(temp)
        if not now_num:
            raise NoSuchElementException("加入购物车失败")
        assert num + 1 == now_num


    #网购物车中添加产品, 购物车中没有商品，重新添加商品, 全选商品，判断全选的商品师傅和全部商品数量一致
    @pytest.mark.parametrize('good', ["明朝那些事", "红楼梦", "金字塔原理", "袁腾飞讲两宋风云", "不一样的卡梅拉14 我登上了逍遥岛"])
    def test_shopping_cart_002(self, init_driver, good):
        # try:
        #商品个数
        num = 0
        #点击购物车，从主页进入到购物车查看购物车里的商品
        try:
            time.sleep(0.5)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/span/span/a/div').click()
        except:
            raise NoSuchElementException("进入到购物车出错了")

        try:
            time.sleep(2)
            text = init_driver.find_element_by_xpath('//*[@id="shopping"]//div[contains(text(), "全部商品")]').text
            num = self.get_num(text)
        except:
            raise NoSuchElementException("获取商品的个数错误")

        #如果没有商品的话则进行查找商品软后加入到购物车
        if not num:
            try:
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(good)
                time.sleep(0.5)
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[2]').click()
            except:
                raise NoSuchElementException("搜索商品出问题了")

            try:
                text = init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[1]/span').text
                if not self.get_num(text):
                    raise NoSuchElementException("没有搜索到商品，请换一个商品再次操作")
                time.sleep(0.5)
                init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[2]/a[1]').click()
            except:
                raise NoSuchElementException("进入到商品详情的时候出错了")

            try:
                time.sleep(2)
                init_driver.find_element_by_xpath('//*[@id="item-detail-show-w"]//div[contains(text(), "加入购物车")]').click()
            except:
                raise NoSuchElementException("加入购物车失败")

            #进入购物车
            try:
                time.sleep(1)
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/span/span').click()
            except:
                raise NoSuchElementException("进入购物车失败")

        try:
            temp = init_driver.find_element_by_xpath('//*[@id="shopping"]//div[contains(text(), "全部商品")]').text
            num = self.get_num(temp)
            if not num:
                raise NoSuchElementException("商品加入购物车失败")
        except:
            raise NoSuchElementException("获取商品数量出错")

        try:
            status = init_driver.find_element_by_xpath('//*[@id="shopping"]/div[3]/div/div[1]/label').get_attribute('class')
            if status.__contains__("ivu-checkbox-wrapper-checked"):
                init_driver.find_element_by_xpath('//*[@id="shopping"]/div[3]/div/div[1]/label').click()
        except:
            raise NoSuchElementException("全选商品出错")

        try:
            goods_list = init_driver.find_elements_by_xpath('//*[@id="shopping"]/div[2]/div[3]/div')
            assert num == len(goods_list)
        except:
            raise NoSuchElementException("获取商品列表失败")
        # finally:
        #     init_driver.quit()




    # 把购物车中的商品删除，如果没有的话直接退出
    @pytest.mark.parametrize('good', ["明朝那些事", "红楼梦", "金字塔原理", "袁腾飞讲两宋风云", "不一样的卡梅拉14 我登上了逍遥岛"])
    def test_shopping_cart_004(self, init_driver, good):
        # 商品个数
        num = 0
        goods = []
        # 点击购物车，从主页进入到购物车查看购物车里的商品
        try:
            time.sleep(1)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/span/span/a/div').click()
        except:
            raise NoSuchElementException("进入到购物车出错了")

        try:
            time.sleep(5)
            text = init_driver.find_element_by_xpath('//*[@id="shopping"]//div[contains(text(), "全部商品")]').text
            num = self.get_num(text)
        except:
            raise NoSuchElementException("获取商品的个数错误")
        if not num:#说明购物车中没有商品，添加商品到购物车
            try:
                time.sleep(4)
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(good)
                time.sleep(2)
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(Keys.ENTER)
                time.sleep(2)
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(Keys.ENTER)
                time.sleep(5)
            except:
                raise NoSuchElementException("搜索商品失败")
            #查看是否搜索到了商品
            try:
                time.sleep(5)
                text = init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[1]').text
                if not self.get_num(text):
                    raise NoSuchElementException("没有搜索到商品，换一个商品继续搜索")
            except:
                raise NoSuchElementException("没有搜索到商品，换个商品继续搜索")
            try:
                time.sleep(2)
                init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[2]/a[1]').click()
                time.sleep(6)
                init_driver.find_element_by_xpath('//*[@id="item-detail-show-w"]//div[contains(text(),"加入购物车")]')
            except:
                raise NoSuchElementException("进入商品详情失败")
            try:
                time.sleep(4)
                init_driver.find_element_by_xpath('//*[@id="item-detail-show-w"]//div[contains(text(),"加入购物车")]').click()
                time.sleep(1)
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/span/span/a/div').click()
                time.sleep(2)
                init_driver.find_element_by_xpath('//*[@id="shopping"]/div[2]/div[1]/div[1]')
            except:
                raise NoSuchElementException("商品加入到购物车失败")
            try:
                time.sleep(2)
                text = init_driver.find_element_by_xpath('//*[@id="shopping"]/div[2]/div[1]/div[1]').text
                if not self.get_num(text):
                    raise NoSuchElementException("加入购物车失败")
            except:
                raise NoSuchElementException("加入购物车失败")

        try:
            time.sleep(3)
            text = init_driver.find_element_by_xpath('//*[@id="shopping"]/div[2]/div[2]/label')
            if not text.get_attribute('class').__contains__("ivu-checkbox-wrapper-checked"):
                text.click()
        except:
            raise NoSuchElementException("点击全选失败")
        try:
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="shopping"]/div[3]/div/div[2]').click()
            time.sleep(3)
            init_driver.find_element_by_xpath('//button/span[contains(text(), "确定")]').click()
            time.sleep(2)
        except:
            raise NoSuchElementException("删除商品失败")
        try:
            time.sleep(2)
            text = init_driver.find_element_by_xpath('//*[@id="shopping"]//div[contains(text(), "全部商品")]').text
            num = self.get_num(text)
        except:
            raise NoSuchElementException("获取商品的个数错误")
        assert num == 0