# 对于接口/mall/item/getCommentList 商品评价列表

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.api.mall.web_pcLogin_test import TestCaseWebPCLogin as Login
import ast

"""
currentPage  integer($int64) (query) 当前页数
pageSize integer($int64) (query) 每页记录数
qp-customerId-eq string (query) 会员编号
qp-skuCode-eq string (query) sku编号
sorter string (query) 排序条件 desc-字段名或者asc-字段名

sso_sessionid string (header) sessionid
x-tenant-id * string (header) tenant Default value : 2

method: get
"""

class TestCaseITemGetCommentList(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "qp_customerId_eq-qp_skuCode_eq-sorter": "${parameterize(testcases/api/mall/item/item_getCommentList.csv)}",
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("商品评价列表")
        .base_url("${get_base_url()}")
        .variables(**{
            "x_tenant_id": "2", #tenant Default value : 2     必填选项  header部分
        })
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("登录")
            .call(Login)
            .export(*['sessionId', 'token',])
        ),
        Step(
            RunRequest("获取商品评价")
            .get("/mall/item/getCommentList")
            .with_params(
                **{
                    "qp-customerId-eq": "$qp_customerId_eq",
                    "qp-skuCode-eq": "$qp_skuCode_eq",
                    "pageSize": "10",
                    "currentPage": "1"
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
