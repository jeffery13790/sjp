
from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest



class TestCaseCustomerLogin(HttpRunner):

    config = (
        Config("运行平台登录")
        .base_url("${get_base_url()}")
        .variables(**{
            "userName": "opsAdmin",
            "password": "200622",
            "verifyCode": "1234",
            "regType": 4,
        })
        .export(*["customer_token", "customer_sessionId", "verifyId"])
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
                    # "sso_sessionid": "",
                    # "Token": "",
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
            RunRequest("用户登录")
            .post("/ops/api/web/login")
            .with_params(
                **{
                    "userName": "$userName",
                    "password": "$password",
                    "verifyCode": "$verifyCode",
                    "verifyId": "$verifyId",
                    "regType": "$regType",
                }
            )
            .with_headers(
                **{
                    "x-app-id": "200",
                    "x-tenant-id": "2",
                    "sso_sessionid": "",
                    "Token": "",

                }
            )
            .with_json(
                {
                    "userName": "$userName",
                    "password": "$password",
                    "verifyCode": "$verifyCode",
                    "verifyId": "$verifyId",
                    "regType": "$regType",
                }
            )
            .extract()
            .with_jmespath("body.data.token", "customer_token")
            .with_jmespath('body.data.sessionId', "customer_sessionId")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
    ]