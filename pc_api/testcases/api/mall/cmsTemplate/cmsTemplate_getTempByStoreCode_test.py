# 对于接口/mall/cmsTemplate/getTemplateByStoreCode  查询店铺首页

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.login_test.login_test import TestCaseLogin as Login
import os
"""
qp-bg-eq * string (query) 业务 1商城 2助学读物
qp-memberCardCode-eq string (query) 会员编码
qp-platform-eq * string (query) 状态 1移动端 2pc端
qp-storeCode-eq * string (query) 店铺code
qp-userCode-eq string (query) 账户编码
sso_sessionid string (header) sessionid
x-tenant-id *  string (header) tenant Default value : 2

method: get
"""

class TestCaseCMSTGetTByStoreCode(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "qp_bg_eq-qp_platform_eq-qp_storeCode_eq": "${parameterize(testcases/api/mall/cmsTemplate/cmsTemplate_getTempByStoreCode.csv)}",
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("查询商品信息接口")
        .base_url("${get_base_url()}")
        .variables(**{
            "x_tenant_id": "2",     #tenant Default value : 2     必填选项  header部分
        })
        .export(*["itemCode", "categoryId", "classId", "skuCode"])
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("登录")
            .call(Login)
            .export(*['sessionId', 'token', 'accountCode', 'personId', "name", "nickname", "username", "phone",
                      "memberCode", "userCode", "account_id", "storeCode", "member_id"])
        ),
        Step(
            RunRequest("查询店铺首页")
            .get("/mall/cmsTemplate/getTemplateByStoreCode")
            .with_params(
                **{
                    "qp-storeCode-eq": "$storeCode",
                    "qp-bg-eq": "1",
                    "qp-platform-eq": "2",
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
