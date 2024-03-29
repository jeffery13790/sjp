# NOTE: Generated By HttpRunner v3.1.4
# FROM: cmsTemplatePage_queryTemplateById.har

"""
sso_sessionid string (header) sessionid
templateId * integer($int64) (query) templateId
x-tenant-id * string (header)	tenant Default value : 2
"""

from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase, Parameters
import pytest
from testcases.api.business.business_login_test import TestCaseBusinessLogin as Login


class TestCaseCmstemplatepageQuerytemplatebyid(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "business_userName-business_password-business_verifyCode-business_regType": "${parameterize(common.csv)}",
            "store_code-templateId": "${parameterize(testcases/api/business/cmsTemplate/cmsTemplatePage_queryTemplateById.csv)}"
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("计算购物车中选中商品的价格")
        .base_url("${get_base_url()}")
        .variables(**{
            "x_tenant_id": "2",  # tenant Default value : 2     必填选项  header部分
        })
        .export(*["sessionId", "token", "employeeName", "employeeId", "accountName", "accountId", "accountCode"])
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("商家后台登录")
            .call(Login)
            .export(*["sessionId", "token", "employeeName", "employeeId", "accountName", "accountId", "accountCode"])
        ),
        Step(
            RunRequest("查询页面基础数据")
            .get("/business/api/cmsTemplatePage/queryTemplateById")
            .with_params(**{"templateId": "741364749471719424"})
            .with_headers(
                **{
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "store-code": "$store_code",
                    "business-code": "$accountCode",
                    "token": "$token",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
            .assert_equal("body.traceId", "")
        ),
    ]


if __name__ == "__main__":
    TestCaseCmstemplatepageQuerytemplatebyid().test_start()
