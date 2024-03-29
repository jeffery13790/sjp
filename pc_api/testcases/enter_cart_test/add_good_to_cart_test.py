# NOTE: Generated By HttpRunner v3.1.4
# FROM: 通过搜索商品然后选择搜索到的商品列表中的第一个商品加入到购物车中
"""
@author :springfall

"""


from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase
from testcases.login_test.login_test import TestCaseLogin as Login
import pytest
from httprunner import Parameters
from datetime import datetime



class TestCaseAddGoodCart(HttpRunner):

    @pytest.mark.parametrize(
        'param',
        Parameters(
            {
                "phoneNumber-verifyCode": "${parameterize(common.csv)}",
                "good_name": "${get_good_name()}"
            }
        ),
    )
    def test_start(self, param):
        super().test_start(param)


    config = (
        Config("testcase description")
        .base_url("${get_base_url()}")
        .export(*['sessionId', 'token', 'accountCode', "memberCode", "userCode", "storeCode", "itemCode", "skuCode", "cart_good_id"])
        .verify(False)
    )
    teststeps = [
        Step(
            RunTestCase("登录")
            .call(Login)
            .export(*['sessionId', 'token', 'accountCode', 'personId', "name", "nickname", "username", "phone", "memberCode", "userCode", "account_id", "storeCode"])
        ),

        Step(
            RunRequest("/mall/search/queryItemList")
            .get("/mall/search/queryItemList")
            .with_params(
                **{
                    "pageSize": "16",
                    "keyWord": "$good_name",
                    "qp-status-eq": "1",
                    "qp-storeCode-eq": "$storeCode",
                }
            )
            .with_headers(
                **{
                    "x-tenant-id": "2",
                    "sso_sessionid": "$sessionId",
                }
            )
            .with_cookies(
                **{
                    "sessionId": "$sessionId",
                    "token": "$token",
                }
            )
            .extract()
            .with_jmespath('body.data.list[0].itemCode', "itemCode")
            .with_jmespath('body.data.list[0].skuCode', "skuCode")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),

        Step(
            RunRequest("/mall/cart/save")
            .post("/mall/cart/save")
            .with_headers(
                **{
                    "x-tenant-id": "2",
                    "sso_sessionid": "$sessionId",
                }
            )
            .with_cookies(
                **{
                    "sessionId": "$sessionId",
                    "token": "$token",
                }
            )
            .with_json(
                {
                    "buyerCode": "$accountCode",
                    "cartType": 0,
                    "channelId": 1,
                    "isChoice": 0,
                    "itemCode": "$itemCode",
                    "packingUnit": "册",
                    "sellerCode": "SJ001",
                    "skuCode": "$skuCode",
                    "skuQuantity": 1,
                    "storeCode": "$storeCode",
                    "qp-storeCode-eq": "$storeCode",
                    "taxRate": 0,
                    "taxRateCode": "",
                }
            )
            .extract()
            .with_jmespath('body.data.id', "cart_good_id")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/mall/cart/cartTotalNum")
            .get("/mall/cart/cartTotalNum")
            .with_params(
                **{
                    "cartType": "1",
                    "channel": "1",
                    "pageSize": "50",
                    "qp-buyerCode-eq": "$accountCode",
                    "qp-cartType-eq": "0",
                    "qp-channelId-eq": "1",
                    "qp-storeCode-eq": "$storeCode",
                }
            )
            .with_headers(
                **{
                    "x-tenant-id": "2",
                    "sso_sessionid": "$sessionId",
                }
            )
            .with_cookies(
                **{
                    "sessionId": "$sessionId",
                    "token": "$token",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),

    ]

