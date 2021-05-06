# 对于接口/mall/cmsTemplate/getStoreCmsTemplateById  根据id号查询二级页面

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.login_test.login_test import TestCaseLogin as Login
import os
"""
id * integer($int64) (query) 二级页面主键
sso_sessionid string (header) sessionid
x-tenant-id * string (header) tenant Default value : 2

method: get
"""

class TestCaseCMSTemplateGetStoreTByID(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "id": "${parameterize(testcases/api/mall/cmsTemplate/cmsTemplate_getStoreCmsTemplateById.csv)}"
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
            RunRequest("根据id号查询二级页面")
            .get("/mall/cmsTemplate/getStoreCmsTemplateById")
            .with_params(
                **{
                    "id": "$id",
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
