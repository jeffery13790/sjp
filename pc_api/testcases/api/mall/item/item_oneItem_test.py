# 对于接口/mall/item/oneItem  查询商品详情

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.login_test.login_test import TestCaseLogin as Login
import os
"""
loginStatus string (query) 判断是否登陆过，展示商品是否被收藏
qp-itemCode-eq string (query) 商品编码
qp-storeCode-eq string (query) 店铺Code
sorter-sales string (query)	销量排序
sso_sessionid string (header)  sessionid
x-tenant-id *  string (header) tenant Default value : 2

method: get
"""

class TestCaseOneItem(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "loginStatus-qp_itemCode_eq-qp_storeCode_eq-sorter_sales": "${parameterize(testcases/api/mall/item/item_oneItem.csv)}"
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("查询获取一个商品的详情")
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
            .export(*['sessionId', 'token'])
        ),
        Step(
            RunRequest("查询商品详情")
            .get("/mall/item/oneItem")
            .with_params(
                **{
                    "qp-storeCode-eq": "$qp_storeCode_eq",
                    "qp-itemCode-eq": "$qp_itemCode_eq",
                    "loginStatus": "$loginStatus",
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
