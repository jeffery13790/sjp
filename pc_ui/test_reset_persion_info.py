from selenium.common.exceptions import NoSuchElementException
import re
import time
import pytest


def get_address():
    data = [("springfall", "18856012041", "虹梅路117号"), ("springfall_1", "18856012041", "虹梅路118号"),
            ("springfall_2", "18856012041", "虹梅路119号"), ("springfall_3", "18856012041", "虹梅路120号"),
            ("springfall_5", "18856012041", "虹梅路220号")]
    return data

def get_data():
    # import io
    # io.open()
    data = [("springfall", "profession"), ("springfall_1", "profession_1"), ("springfall_2", "profession_3"), ("springfall_3", "profession_4"), ("springfall_5", "profession_5")]
    return data
class TestClassReSetPersionInfo():


    @pytest.mark.parametrize('username, profession', get_data())
    def test_reset_persion_info(self, init_driver, username, profession):
        good = "明朝那些事"
        self.driver = init_driver
        #设置收藏商品个数
        num = 0

        #点击用户信息
        try:
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="box"]//p[@class="username-p"]').click()
        except:
            raise NoSuchElementException("没有找到用户信息元素")

        try:
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="information"]//input[@placeholder="请输入昵称"]').send_keys(username)
        except:
            raise NoSuchElementException("输入昵称的时候出错")


        try:
            sex = self.driver.find_element_by_xpath('//*[@id="information"]/div[2]/div[4]/div[2]/div/div[1]').text
            self.driver.find_element_by_xpath('//*[@id="information"]/div[2]/div[4]/div[2]/div/div[1]').click()
            if "男".__eq__(sex):
                self.driver.find_element_by_xpath('//*[@id="information"]//li[contains(text(), "女")]').click()
            else:
                self.driver.find_element_by_xpath('//*[@id="information"]//li[contains(text(), "男")]').click()
        except:
            raise NoSuchElementException("修改性别的时候出错")

        try:
            self.driver.find_element_by_xpath('//*[@id="information"]//input[@placeholder="请输入您的职业"]').clear()
            self.driver.find_element_by_xpath('//*[@id="information"]//input[@placeholder="请输入您的职业"]').send_keys(profession)
        except:
            raise NoSuchElementException("修改职业的时候出错")

        try:
            self.driver.find_element_by_xpath('//*[@id="information"]/div[2]/button').click()
        except:
            raise NoSuchElementException("保存更改信息按钮的时候错误")
        assert True
        # self.driver.close()

    def test_look_order(self, init_driver):
        self.driver = init_driver

        #点击用户信息
        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="box"]//p[@class="username-p"]').click()
        except:
            raise NoSuchElementException("没有找到用户信息元素")

        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="persone-center"]//a[contains(text(), "我的订单")]').click()
        except:
            raise NoSuchElementException("进入到我的订单界面")

        try:
            elements = self.driver.find_elements_by_xpath('//*[@id="person-order"]/div[1]/span')
            element_texts = []
            for element in elements:
                element_texts.append(element.text)

            assert "全部订单" in element_texts
            assert "待付款" in element_texts
            assert "待发货" in element_texts
            assert "已发货" in element_texts
            assert "待评价" in element_texts
        except:
            raise NoSuchElementException("没有进入到我的订单界面")
        # self.driver.close()

    def test_look_coupon(self, init_driver):
        self.driver = init_driver

        #点击用户信息
        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="box"]//p[@class="username-p"]').click()
        except:
            raise NoSuchElementException("没有找到用户信息元素")

        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="persone-center"]//a[contains(text(), "我的优惠券")]').click()
        except:
            raise NoSuchElementException("点击我的优惠券失败")

        try:
            elements = self.driver.find_elements_by_xpath('//*[@id="person-coupon"]/div[1]/div/span')
            element_texts = []
            for element in elements:
                element_texts.append(element.text)
            assert "未使用" in element_texts
            assert "已使用" in element_texts
            assert "已过期" in element_texts
        except:
            raise NoSuchElementException("点击我的优惠券,没有进入优惠券详细列表")

    @pytest.mark.parametrize('username, phone, address', get_address())
    def test_add_Address(self, init_driver, username, phone, address):
        self.driver = init_driver
        #定义收货地址数量
        num = 0
        #点击用户信息
        try:
            time.sleep(5)
            self.driver.find_element_by_xpath('//*[@id="box"]//p[@class="username-p"]').click()
        except:
            raise NoSuchElementException("没有找到用户信息元素")

        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="persone-center"]//a[contains(text(), "收货地址")]').click()
        except:
            raise NoSuchElementException("点击收货地址")

        #获取现有的收货地址数量
        try:
            time.sleep(2)
            addNum = self.driver.find_element_by_xpath('//*[@id="myAddress"]/div[1]/div[1]/span[1]/span[2]').text
            if addNum:
                num = re.findall('\d', addNum)
                if num:
                    num = int(num[0])
        except:
            raise NoSuchElementException("获取收货地址数量的时候出错")

        try:
            #点击添加收货地址
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="myAddress"]//span[contains(text(), "添加收货地址")]').click()
        except:
            raise NoSuchElementException("点击添加收货地址失败")

        try:
            time.sleep(2)
            #添加联系人信息
            self.driver.find_element_by_xpath('//input[@placeholder="收货人姓名"]').send_keys(username)
            time.sleep(0.5)
            #添加手机号码
            self.driver.find_element_by_xpath('//input[@placeholder="输入手机号"]').send_keys(phone)
            time.sleep(0.5)
            #选择省份
            self.driver.find_element_by_xpath('//span[contains(text(), "请选择省份")]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/form/div[3]/div/div/div[1]/div/div/div/div[2]/ul[2]/li[1]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('//span[contains(text(), "请选择城市")]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/form/div[3]/div/div/div[2]/div/div/div/div[2]/ul[2]/li[1]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('//span[contains(text(), "请选择城区")]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/form/div[3]/div/div/div[3]/div/div/div/div[2]/ul[2]/li[1]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('//input[@placeholder="详细地址、省、市区/街道、门牌号等"]').send_keys(address)
            time.sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[3]/div/button[1]').click()
            time.sleep(3)
        except:
            raise NoSuchElementException("添加地址信息的时候出错")

        #再次获取收获地址个数
        nex_num = 0
        try:
            time.sleep(2)
            next_addNum = self.driver.find_element_by_xpath('//*[@id="myAddress"]/div[1]/div[1]/span[1]/span[2]').text
            if next_addNum:
                nex_num = re.findall('\d', next_addNum)
                if nex_num:
                    nex_num = int(nex_num[0])
        except:
            raise NoSuchElementException("获取收货地址数量的时候出错")
        assert nex_num == num + 1


    def test_delete_Address(self, init_driver):
        self.driver = init_driver
        #定义收货地址数量
        num = 0
        #点击用户信息
        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="box"]//p[@class="username-p"]').click()
        except:
            raise NoSuchElementException("没有找到用户信息元素")

        try:
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="persone-center"]//a[contains(text(), "收货地址")]').click()
        except:
            raise NoSuchElementException("点击收货地址")

        #获取现有的收货地址数量
        try:
            time.sleep(2)
            addNum = self.driver.find_element_by_xpath('//*[@id="myAddress"]/div[1]/div[1]/span[1]/span[2]').text
            if addNum:
                num = re.findall('\d', addNum)
                if num:
                    num = int(num[0])
        except:
            raise NoSuchElementException("获取收货地址数量的时候出错")


        try:
            elements = self.driver.find_elements_by_xpath('//*[@id="myAddress"]//button[contains(text(), "删除")]')
            assert num == len(elements)
            if len(elements) <= 1:
                return
            else:
                for i in range(0, len(elements)):
                    if i < len(elements) - 1:
                        elements[len(elements) - 1 - i].click()
                        time.sleep(1)
                        self.driver.find_element_by_xpath(
                            '/html/body/div[4]//button[2]/span[contains(text(), "确定")]').click()

                nex_num = 0
                time.sleep(2)
                next_addNum = self.driver.find_element_by_xpath(
                    '//*[@id="myAddress"]/div[1]/div[1]/span[1]/span[2]').text
                if next_addNum:
                    nex_num = re.findall('\d', next_addNum)
                    if nex_num:
                        nex_num = int(nex_num[0])
                assert nex_num == 1
        except:
            raise NoSuchElementException("删除收货地址失败")


        #再次获取收获地址个数

