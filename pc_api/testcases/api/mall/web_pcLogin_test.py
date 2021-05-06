# 对于接口/mall/web/pcLogin  登录

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
"""
phoneNumber * string (query) 手机号
verifyCode * string (query) 验证码的值
x-tenant-id * string (header) tenant Default value : 2

method: get
"""

class TestCaseWebPCLogin(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(testcases/api/mall/web_pcLogin.csv)}"
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("登录")
        .base_url("${get_base_url()}")
        .variables(**{
            "x_tenant_id": "2",     #tenant Default value : 2     必填选项  header部分
        })
        .verify(False)
        .export(*["sessionId", "token"])
    )

    teststeps = [
        Step(
            RunRequest("登录")
            .get("/mall/web/pcLogin")
            .with_params(**{"phoneNumber": "$phoneNumber", "verifyCode": "$verifyCode"})
            .with_headers(
                **{
                    "sso_sessionid": "undefined",
                    "x-tenant-id": "$x_tenant_id",
                }
            )
            .extract()
            .with_jmespath('body.data.sessionId', 'sessionId')
            .with_jmespath('body.data.token', 'token')
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
    ]
