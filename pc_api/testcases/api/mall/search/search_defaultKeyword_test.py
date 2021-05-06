# 对于接口/mall/search/defaultKeyword   默认搜索词检索商品

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.api.mall.web_pcLogin_test import TestCaseWebPCLogin as Login
import ast

"""
qp-storeCode-eq string (query) storeCode
sso_sessionid string (header) sessionid
x-tenant-id * string (header) tenant Default value : 2

method: get
"""

class TestCaseSearchDefaultkeyWord(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "qp_storeCode_eq": "${parameterize(testcases/api/mall/search/search_defaultKeyword.csv)}",
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("获取默认搜索词")
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
            RunRequest("默认搜索词")
            .get("/mall/search/defaultKeyword")
            .with_params(
                **{"qp-storeCode-eq": "$qp_storeCode_eq"}
            )
            .with_headers(
                **{
                    "x-tenant-id": "2",
                    "sso_sessionid": "$sessionId",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
    ]
