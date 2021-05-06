# 对于接口/mall/category/queryCategoryTree   根据模板id查询类目树

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.api.mall.web_pcLogin_test import TestCaseWebPCLogin as Login
import ast

"""
status * string (query) 状态0启用1禁用

sso_sessionid string (header) sessionid
x-tenant-id * string (header) tenant Default value : 2
method: get
"""

class TestCaseCategoryQueryCategoryTree(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "status": "${parameterize(testcases/api/mall/category/category_queryCategoryTree.csv)}",
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("根据模板id查询类目录树")
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
            .export(*['sessionId', 'token'])
        ),
        Step(
            RunRequest("根据模板id查询类目录树")
            .get("/mall/category/queryCategoryTree")
            .with_params(
                **{
                    "status": "$status",
                }
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
