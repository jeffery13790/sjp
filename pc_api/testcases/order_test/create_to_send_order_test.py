# NOTE: Generated By HttpRunner v3.1.4
# FROM: 生成一个待付款订单
"""
@author :springfall

"""


from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.buy_good_test.search_buy_test import TestCaseBuyFromSearch as BuyGood

class TestCaseCreateCancelObligationOrder(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "good_name": "${get_good_name()}"
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("登录操作 ")
        .base_url("${get_base_url()}")
        .verify(False)
        .export(*['sessionId', 'token', 'orderNo', "member_id", "nickname"])
    )
    teststeps = [
        Step(
            RunTestCase("检索商品下单")
            .with_variables(**{"good_name": "$good_name"})
            .call(BuyGood)
            .export(*['sessionId', 'token', 'orderNo', "member_id", "nickname"])
        ),
        Step(
            RunRequest("事件模式设置订单支付状态")
            .put("${get_trade_url()}/trade/order/triggerOrder")
            .with_params(**{
                "event": "20",
                "orderNo": "$orderNo",
            })
            .with_headers(**{
                "x-tenant-id": "2",
                "sso_sessionid": "$sessionId",
            })
            .with_cookies(**{
                "sessionId": "$sessionId",
                "token": "$token",
            })
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        #申请售后  reverseOrderCause  分页查询售后原因列表

    ]