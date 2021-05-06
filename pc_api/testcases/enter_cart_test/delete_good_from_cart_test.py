

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
from testcases.enter_cart_test.add_good_to_cart_test import TestCaseAddGoodCart as AddGoodCart
import pytest


class TestCaseDeleteGoodCart(HttpRunner):

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
        .export(*['sessionId', 'token', 'accountCode', "memberCode", "userCode", "storeCode", "itemCode", "skuCode"])
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("检索商品").with_variables(**{"good_name": "$good_name"}).call(AddGoodCart).export(*['sessionId', 'token', 'accountCode', "memberCode", "userCode", "storeCode", "itemCode", "skuCode", "cart_good_id"])
        ),
        Step(
            RunRequest("获取购物车商品数量")
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
        Step(
            RunRequest("/mall/cart/selectCartList")
            .get("/mall/cart/selectCartList")
            .with_params(
                **{
                    "cartType": "1",
                    "channel": "1",
                    "pageSize": "50",
                    "memberCode": "$memberCode",
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
        Step(
            RunRequest("/mall/cart/delete")
            .delete("/mall/cart/delete")
            .with_params(
                **{
                    "qp-buyerCode-eq": "$accountCode",
                    "qp-cartType-eq": "0",
                    "qp-channelId-eq": "1",
                    "qp-storeCode-eq": "$storeCode",
                    "qp-id-in": "$cart_good_id",
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
        Step(
            RunRequest("/mall/cart/cartTotalNum")
            .get("/mall/cart/cartTotalNum")
            .with_params(
                **{
                    "cartType": "1",
                    "channel": "1",
                    "pageSize": "50",
                    "qp-cartType-eq": "0",
                    "qp-channelId-eq": "1",
                    "qp-buyerCode-eq": "$accountCode",
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