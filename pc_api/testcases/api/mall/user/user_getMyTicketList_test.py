# 对于接口/mall/user/getMyTicketList  获取我的优惠券

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.login_test.login_test import TestCaseLogin as Login
import ast

"""
accountCode *string (query) 用户code
memberCardCode * string (query)	 会员code
storeCode * string (query) 当前店铺code

sso_sessionid string (header) sessionid
x-tenant-id * string (header) tenant Default value : 2

method: get
"""

class TestCaseUserGetTicketList(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "accountCode-memberCardCode-storeCode": "${parameterize(testcases/api/mall/user/user_getMyTicketList.csv)}",

        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("获取我的优惠券")
        .base_url("${get_base_url()}")
        .variables(**{
            "x_tenant_id": "2", #tenant Default value : 2     必填选项  header部分
        })
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("把商品加入购物车")
            .call(Login)
            .export(*['sessionId', 'token',])
        ),
        Step(
            RunRequest("获取我的优惠券")
            .get("/mall/user/getMyTicketList")
            .with_params(
                **{
                    "accountCode": "$accountCode",
                    "memberCardCode": "$memberCardCode",
                    "storeCode": "$storeCode",
                }
            )
            .with_headers(
                **{
                    "x-tenant-id": "$x_tenant_id",
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
