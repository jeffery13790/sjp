# 对于接口/mall/item/selectActivityAndTicket  查询商品参与的活动和优惠券

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.login_test.login_test import TestCaseLogin as Login
import os
"""
qp-memberCardCode-eq string (query) 会员卡Code
qp-skuCode-in string (query) skuCodes,用逗号分隔
qp-storeCode-eq * string (query) 当前店铺
qp-userCode-eq string (query) 用户Code
sso_sessionid string (header) sessionid
x-tenant-id *  string (header) tenant Default value : 2

method: get
"""

class TestCaseItemSelectActivityAndTicket(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "qp_memberCardCode_eq-qp_skuCode_in-qp_storeCode_eq-qp_userCode_eq": "${parameterize(testcases/api/mall/item/item_selectActivityAndTicket.csv)}"
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("查询商品参与的活动和优惠券")
        .base_url("${get_base_url()}")
        .variables(**{
            "x_tenant_id": "2",     #tenant Default value : 2     必填选项  header部分
        })
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("登录")
            .with_variables(**{"x_tenant_id": "2",})
            .call(Login)
            .export(*['sessionId', 'token', 'accountCode', 'personId', "name", "nickname", "username", "phone",
                      "memberCode", "userCode", "account_id", "storeCode", "member_id"])
        ),
        Step(
            RunRequest("查询商品参与的活动和优惠券")
            .get("/mall/item/selectActivityAndTicket")
            .with_params(
                **{
                    "qp-skuCode-in": "$qp_skuCode_in",
                    "qp-storeCode-eq": "$qp_storeCode_eq",
                    "qp-memberCardCode-eq": "$qp_memberCardCode_eq",
                    "qp-userCode-eq": "$qp_userCode_eq",
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
