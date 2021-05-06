from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
import re
from selenium.webdriver.common.action_chains import ActionChains
import pytest


def get_address():  # '', '', '袁腾飞讲两宋风云', '不一样的卡梅拉14 我登上了逍遥岛'
    data = [
            ("springfall", "18856012041", "虹梅路117号", '明朝那些事'),
            ("springfall_1", "18856012041", "虹梅路118号", '金字塔原理'),
            ("springfall_2", "18856012041", "虹梅路119号", '袁腾飞讲两宋风云'),
            ("springfall_3", "18856012041", "虹梅路120号", '不一样的卡梅拉14 我登上了逍遥岛'),
            ("springfall_5", "18856012041", "虹梅路220号", '不一样的卡梅拉14 我登上了逍遥岛')
            ]
    return data
class TestClassShoppingOrder():

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
        if text.__contains__("无"):
            if len(price) == 2:
                return (float(price[0]), 0, float(price[1]))
        elif len(price) == 3:
            return (float(price[0]), float(price[1]), float(price[2]))
        else:
            return (float(0), float(0), float(0))


    def __init__(self):
        username = '18856012041'
        self.driver = Chrome()
        self.driver.implicitly_wait(20)
        self.driver.get(url=r'https://cs1.jsbooks.com.cn/user/login')
        self.driver.maximize_window()
        self.driver.find_element_by_xpath('//*[@id="login"]//input[@placeholder="请输入手机号"]').send_keys(username)
        self.driver.find_element_by_xpath('//*[@id="login"]//span/span/span').click()
        self.driver.find_element_by_xpath('//*[@id="login"]//input[@placeholder="请输入短信验证码"]').send_keys('123456')
        self.driver.find_element_by_xpath('//*[@id="login"]/div[2]/div/div/div[3]/label/span').click()
        self.driver.find_element_by_xpath('//*[@id="login"]/div[2]//button[@type="button"]').click()



    # 从购物车下单，如果没有商品则搜索商品然后再直接购买，如果没有收货地址，则添加地址然后再下单
    # @pytest.mark.parametrize('good_name', ['明朝那些事', '金字塔原理', '袁腾飞讲两宋风云', '不一样的卡梅拉14 我登上了逍遥岛'])
    @pytest.mark.parametrize('username, phone, address, good_name', get_address())
    def test_shopping_order_001(self, init_driver, username, phone, address, good_name):
    # def test_shopping_order_001(self):
    #     """
    #
    #     "springfall", "18856012041", "虹梅路117号",
    #     :param username:
    #     :param phone:
    #     :param address:
    #     :param good_name:
    #     :return:
    #     """
    #     username = "springfall"
    #     phone = "18856012041"
    #     address = "虹梅路117号"
    #     good_name = '明朝那些事'
    #     init_driver = self.driver
        time.sleep(2)
        #进入购物车，然后查看购物车和中是否有商品，如果有的话，直接下单，如果没有的话则搜索商品然后立即购买
        try:
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/span/span/a/div').click()
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="shopping"]/div[2]/div[1]/div[1]')
        except:
            raise NoSuchElementException("进入购物车失败")

        #获取购物车里的商品数量
        try:
            text = init_driver.find_element_by_xpath('//*[@id="shopping"]/div[2]/div[1]/div[1]').text
            good_num = self.get_num(text)
        except:
            raise NoSuchElementException("获取购物车中的商品数量出错")

        if not good_num:
            try:
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(good_name)
                time.sleep(0.5)
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(Keys.ENTER)
                time.sleep(5)
                init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[1]/span')
            except:
                raise NoSuchElementException("搜索商品出错")

            try:
                search_num = 0
                text = init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[1]/span').text
                search_num = self.get_num(text)
            except:
                raise NoSuchElementException("没有搜索到商品")

            try:
                init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[2]/a[1]').click()
                time.sleep(2)
            except:
                raise NoSuchElementException("进入到商品详情失败")

            #如果有优惠券则领取优惠券
            try:
                time.sleep(0.5)
                init_driver.find_element_by_xpath('//*[@id="receiveCoupons"]/div[2]')
                init_driver.find_element_by_xpath('//*[@id="receiveCoupons"]//div[contains(text(), "立即领取")]').click()
                time.sleep(0.5)
                #领取优惠券
                coupons = init_driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div')
                for coupon in coupons:
                    coupon.find_element_by_xpath('//span[contains(text(), "立即领取")]').click()
                time.sleep(0.5)
                #退出领取优惠券
                init_driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/a').click()
                time.sleep(0.5)
            except:
                if init_driver.find_elements_by_xpath('//*[@id="receiveCoupons"]//div[contains(text(), "立即领取")]'):
                    raise NoSuchElementException("没有优惠券可以领取")
                else:
                    pass


            try:
                time.sleep(2)
                init_driver.find_element_by_xpath('//*[@id="item-detail-show-w"]//div[contains(text(), "立即购买")]').click()
            except:
                raise NoSuchElementException("立即购买失败")

            #查看是否有收货地址，如果没有收货地址，则添加收货地址

            try:
                time.sleep(2)
                addrs_div = init_driver.find_elements_by_xpath('//*[@id="order"]/div[2]/div[1]/div')
                if len(addrs_div) > 2:
                    pass
                else:
                    init_driver.find_element_by_xpath('//*[@id="order"]//div[contains(text(), "新增收货地址")]').click()
                    time.sleep(0.2)
                                                     # /html/body/div[3]/div[2]/div/div/div[2]/div/form/div[1]/div/div/div/input
                    init_driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/form/div[1]/div/div/div/input').send_keys(username)
                    time.sleep(0.5)
                    init_driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/form/div[2]/div/div/div/input').send_keys(phone)
                    time.sleep(0.5)
                    init_driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/form/div[3]/div/div/div[1]/div/div/div/div[1]/div/span[contains(text(), "请选择省份")]').click()
                    time.sleep(0.5)
                    init_driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/form/div[3]/div/div/div[1]/div/div/div/div[2]/ul[2]/li[1]').click()
                    time.sleep(0.5)
                    init_driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/form/div[3]/div/div/div[2]/div/div/div/div[1]/div/span[contains(text(), "请选择城市")]').click()
                    time.sleep(0.5)
                    init_driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/form/div[3]/div/div/div[2]/div/div/div/div[2]/ul[2]/li[1]').click()
                    time.sleep(0.5)
                    init_driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/form/div[3]/div/div/div[3]/div/div/div/div[1]/div/span[contains(text(), "请选择城区")]').click()
                    time.sleep(0.5)
                    init_driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/form/div[3]/div/div/div[3]/div/div/div/div[2]/ul[2]/li[1]').click()
                    time.sleep(0.5)
                    init_driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/form/div[4]/div/div/div/input').send_keys(address)
                    time.sleep(0.5)
                    init_driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[3]/div/button[1]').click()
            except:
                raise NoSuchElementException("添加地址失败")

            try:
                time.sleep(2)
                mouse = init_driver.find_element_by_xpath('//*[@id="order"]/div[2]/div[1]/div[2]/div[1]/div[1]')
                ActionChains(init_driver).move_to_element(mouse).perform()
                mouse.find_element_by_xpath('//div[contains(text(), "默认地址")]').click()
                # init_driver.find_element_by_xpath('//*[@id="order"]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]').click()
            except:
                raise NoSuchElementException("选择地址失败")

            try:
                time.sleep(0.5)
                init_driver.find_element_by_xpath('//*[@id="order"]//div[contains(text(), "去支付")]').click()
                time.sleep(2)
            except:
                raise NoSuchElementException("去支付失败")

            try:
                time.sleep(2)
                init_driver.find_element_by_xpath('//*[@id="pay"]/div[3]/div/div[1]')
            except:
                raise NoSuchElementException("生成订单失败")
            assert True


    # 进入购物车，如果没有商品则搜索然后直接下单

    # @pytest.mark.parametrize('good_name', ['明朝那些事'])
    @pytest.mark.parametrize('good_name', ['明朝那些事', '金字塔原理', '袁腾飞讲两宋风云', '不一样的卡梅拉14 我登上了逍遥岛'])
    def test_shopping_order_002(self, init_driver, good_name):
    # def test_shopping_order_002(self):
    #     good_name = '明朝那些事'
    #     init_driver = self.driver
        time.sleep(2)
        #进入购物车，然后查看购物车和中是否有商品，如果有的话，直接下单，如果没有的话则搜索商品然后立即购买
        try:
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/span/span/a/div').click()
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="shopping"]/div[2]/div[1]/div[1]')
        except:
            raise NoSuchElementException("进入购物车失败")

        #获取购物车里的商品数量
        try:
            text = init_driver.find_element_by_xpath('//*[@id="shopping"]/div[2]/div[1]/div[1]').text
            good_num = self.get_num(text)
        except:
            raise NoSuchElementException("获取购物车中的商品数量出错")

        if good_num:

            try:
                selected = init_driver.find_element_by_xpath('//*[@id="shopping"]/div[3]/div/div[1]/label')
                if not selected.get_attribute('class').__contains__("ivu-checkbox-wrapper-checked"):
                    selected.click()
                time.sleep(2)
                init_driver.find_element_by_xpath('//*[@id="shopping"]/div[3]/div/div[2]').click()
                time.sleep(2)
                init_driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]').click()
                time.sleep(2)
            except:
                raise NoSuchElementException("删除商品失败")
        try:
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(good_name)
            time.sleep(0.5)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(Keys.ENTER)
            time.sleep(0.5)
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(Keys.ENTER)
            time.sleep(5)
            init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[1]/span')
        except:
            raise NoSuchElementException("搜索商品出错")

        try:
            search_num = 0
            text = init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[1]/span').text
            search_num = self.get_num(text)
        except:
            raise NoSuchElementException("没有搜索到商品")

        try:
            init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[2]/a[1]').click()
            time.sleep(2)
        except:
            raise NoSuchElementException("进入到商品详情失败")

        #如果有优惠券则领取优惠券
        try:
            time.sleep(0.5)
            init_driver.find_element_by_xpath('//*[@id="receiveCoupons"]/div[2]')
            init_driver.find_element_by_xpath('//*[@id="receiveCoupons"]//div[contains(text(), "立即领取")]').click()
        except:
            raise NoSuchElementException("进入优惠券领取界面失败")

        try:
            time.sleep(0.5)
            coupons = init_driver.find_elements_by_xpath('//div[@class="modelChange-content-item-action"]//span[contains(text(), "待领取")]')
            for coupon in coupons:
                coupon.click()
        except:
            raise NoSuchElementException("领取优惠券失败")

        #退出优惠券领取页面
        try:
            init_driver.find_element_by_xpath('//div[@class="ivu-modal-content"]/a[@class="ivu-modal-close"]').click()
            time.sleep(0.5)
        except:
            raise NoSuchElementException("退出优惠券领取页面失败")

        try:
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="item-detail-show-w"]//div[contains(text(), "立即购买")]').click()
        except:
            raise NoSuchElementException("立即购买失败")

        #选择收货地址
        try:
            time.sleep(2)                             #//*[@id="order"]/div[2]/div[1]/div[2]/div/div[1]
            mouse = init_driver.find_element_by_xpath('//div[@class="address-box-item-header"]')
            ActionChains(init_driver).move_to_element(mouse).perform()
            mouse.find_element_by_xpath('//div[contains(text(), "默认地址")]').click()
            # init_driver.find_element_by_xpath('//*[@id="order"]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]').click()
        except:
            raise NoSuchElementException("选择地址失败")

        try:
            time.sleep(0.5)
            init_driver.find_element_by_xpath('//*[@id="order"]//div[contains(text(), "去支付")]').click()
            time.sleep(2)
        except:
            raise NoSuchElementException("去支付失败")

        try:
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="pay"]/div[3]/div/div[1]')
        except:
            raise NoSuchElementException("生成订单失败")
        assert True

    #进入购物车，如果有商品则直接结账
    @pytest.mark.parametrize('good_name', ['明朝那些事', '金字塔原理', '袁腾飞讲两宋风云', '不一样的卡梅拉14 我登上了逍遥岛'])
    def test_shopping_order_003(self, init_driver, good_name):
    # def test_shopping_order_003(self):
    #     good_name = '明朝那些事'
    #     init_driver = self.driver
        time.sleep(2)
        #进入购物车，然后查看购物车和中是否有商品，如果有的话，直接下单，如果没有的话则搜索商品然后立即购买
        try:
            init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/span/span/a/div').click()
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="shopping"]/div[2]/div[1]/div[1]')
        except:
            raise NoSuchElementException("进入购物车失败")

        #获取购物车里的商品数量
        try:
            text = init_driver.find_element_by_xpath('//*[@id="shopping"]/div[2]/div[1]/div[1]').text
            good_num = self.get_num(text)
        except:
            raise NoSuchElementException("获取购物车中的商品数量出错")

        if not good_num:
            try:
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(good_name)
                time.sleep(0.5)
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                init_driver.find_element_by_xpath('//*[@id="search-wrapper"]/div/div[2]/div/div[1]/div[1]/input').send_keys(Keys.ENTER)
                time.sleep(5)
                init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[1]/span')
            except:
                raise NoSuchElementException("搜索商品出错")

            try:
                search_num = 0
                text = init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[1]/span').text
                search_num = self.get_num(text)
            except:
                raise NoSuchElementException("没有搜索到商品")

            try:
                init_driver.find_element_by_xpath('//*[@id="goodsListSearch"]/div[3]/div[2]/a[1]').click()
                time.sleep(2)
            except:
                raise NoSuchElementException("进入到商品详情失败")

            #如果有优惠券则领取优惠券
            try:
                time.sleep(0.5)
                init_driver.find_element_by_xpath('//*[@id="receiveCoupons"]/div[2]')
                init_driver.find_element_by_xpath('//*[@id="receiveCoupons"]//div[contains(text(), "立即领取")]').click()
            except:
                raise NoSuchElementException("进入优惠券领取界面失败")

            try:
                time.sleep(0.5)
                coupons = init_driver.find_elements_by_xpath('//div[@class="modelChange-content-item-action"]//span[contains(text(), "待领取")] | //div/span[contains(text(), "继续领取")]')
                if coupons:
                    for coupon in coupons:
                        coupon.click()
            except:
                raise NoSuchElementException("领取优惠券失败")

            #退出优惠券领取页面
            try:
                init_driver.find_element_by_xpath('//div[@class="ivu-modal-content"]//a[@class="ivu-modal-close"]').click()
                time.sleep(0.5)
            except:
                raise NoSuchElementException("退出优惠券领取页面失败")

            try:
                time.sleep(2)
                init_driver.find_element_by_xpath('//*[@id="item-detail-show-w"]//div[contains(text(), "加入购物车")]').click()
            except:
                raise NoSuchElementException("加入购物车失败")

            #进入到购物车
            try:
                time.sleep(3)
                init_driver.find_element_by_xpath('//span[@class="ivu-badge"]//span[contains(text(), "购物车")]').click()
                time.sleep(3)
                elements = init_driver.find_elements_by_xpath('//div[@class="info-box-header"]//div[contains(text(), "结算")]')
                if not elements:
                    raise NoSuchElementException("进入到购物车失败")
            except:
                raise NoSuchElementException('通过商品搜索进入到购物车失败')


        #查看是否已经全选，如果已经全选了则直接下单，如果没有全选择则全选然后下单
        try:
            time.sleep(0.5)
            ifChecked = init_driver.find_element_by_xpath('//*[@id="shopping"]/div[2]/div[2]/label').get_attribute('class')
            if not ifChecked.__contains__('ivu-checkbox-wrapper-checked'):
                init_driver.find_element_by_xpath('//*[@id="shopping"]/div[2]/div[2]/label').click()
        except:
            raise NoSuchElementException("全选商品失败")

        try:
            time.sleep(0.5)
            init_driver.find_element_by_xpath('//*[@id="shopping"]/div[3]/div/div[4]/div[3]').click()
        except:
            raise NoSuchElementException("点击结算失败")

        #获取运费
        try:
            time.sleep(2)
            text = init_driver.find_element_by_xpath('//*[@id="order"]/div[2]/div[2]/div[2]/div[1]').text
            carriage = self.get_price(text)
        except:
            raise NoSuchElementException("获取运费失败")

        #获取全部产品
        total_price = 0
        try:                                           #//*[@id="order"]/div[2]/div[2]/div[2]/div[2]/div[2]/div[4]
            goods = init_driver.find_elements_by_xpath('//*[@id="order"]/div[2]/div[2]/div[2]/div[2]/div')
            for good in goods:
                text = good.find_element_by_xpath('./div[4]').text
                if "总价" not in text:
                    total_price = total_price + self.get_price(text)
        except:
            raise NoSuchElementException("获取商品的价格失败")

        try:
            text = init_driver.find_element_by_xpath('//*[@id="order"]/div[2]/div[2]/div[2]/div[3]/p[1]').text
            real_text = init_driver.find_element_by_xpath('//*[@id="order"]/div[2]/div[2]/div[2]/div[3]/p[2]/span').text
            (all_price, reduced, carriage_all) = self.get_reduction(text)
            real_price = self.get_price(real_text)
            assert carriage == carriage_all
            assert all_price == total_price
        except:
            raise NoSuchElementException("校验金额失败")
        #校验实付金额是否正确
        try:
            text = init_driver.find_element_by_xpath('//*[@id="order"]//span[@class="order-foot-pay-text-amount"]').text
            real_total_price = self.get_price(text)
            assert real_total_price == real_price
        except:
            raise NoSuchElementException("校验实付金额失败")

        try:
            time.sleep(2)
            init_driver.find_element_by_xpath('//*[@id="order"]//div[@class="order-foot-pay-btn"]').click()
        except:
            raise NoSuchElementException("点击去支付失败")

        try:
            init_driver.find_element_by_xpath('//*[@id="pay"]/div[3]/div/div[1]')
        except:
            raise NoSuchElementException("下单失败")
        assert True

if __name__ == "__main__":
    testcase = TestClassShoppingOrder()
    testcase.test_shopping_order_001()
    testcase.test_shopping_order_002()
    testcase.test_shopping_order_003()