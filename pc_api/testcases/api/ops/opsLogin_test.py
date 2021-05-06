# NOTE: Generated By HttpRunner v3.1.4
# FROM: opsLogin.har


from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase, Parameters
import pytest
import ast


class TestCaseOpslogin(HttpRunner):
    @pytest.mark.parametrize(
        "param",
        Parameters({
            "userName-password-verifyCode1-regType": "${parameterize(common.csv)}",
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("登录ops环境")
        .base_url("${get_base_url()}")
        .variables(**{
            "x_tenant_id": "2",  # tenant Default value : 2     必填选项  header部分
            "x_app_id": "200",
        })
        .export(*["token", "sessionId"])
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("获取验证码")
            .get("/ops/api/web/getVerificationCode?")
            .with_headers(
                **{
                    "x-app-id": "200",
                    "x-tenant-id": "2",
                    "sso_sessionid": "",
                    "Token": "",
                }
            )
            .with_cookies(
                **{
                    "sessionId": "",
                    "token": "",
                }
            )
            .extract()
            .with_jmespath('body.data.verifyId', "verifyId")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("ops登录")
            .post("/ops/api/web/login")
            .with_headers(
                **{
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "",
                    "Token": "",
                }
            )
            .with_cookies(
                **{
                    "sessionId": "",
                    "token": "",
                }
            )
            .with_json(
                {
                    "userName": "$userName",
                    "password": "$password",
                    "verifyCode": "$verifyCode1",
                    "verifyId": "$verifyId",
                    "regType": "$regType",
                }
            )
            # .teardown_hook("${teardown_hook_sleep_N_secs($response, 7)}")
            .extract()
            .with_jmespath('body.data.token', "token")
            .with_jmespath('body.data.sessionId', "sessionId")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
    ]


if __name__ == "__main__":
    TestCaseOpslogin().test_start()