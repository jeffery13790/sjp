# NOTE: Generated By HttpRunner v3.1.4
# FROM: business_login.har


from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase, Parameters
import pytest


class TestCaseBusinessLogin(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "business_userName-business_password-business_verifyCode-business_regType": "${parameterize(common.csv)}",
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("计算购物车中选中商品的价格")
        .base_url("${get_base_url()}")
        .variables(**{
            "x_app_id": "201",
            "x_tenant_id": "2",  # tenant Default value : 2     必填选项  header部分
        })
        .export(*["sessionId", "token", "employeeName", "employeeId", "accountName", "accountId", "accountCode"])
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("获取验证码")
            .get("/business/api/web/getVerificationCode?")
            .with_headers(
                **{
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "",
                    "store-code": "",
                    "business-code": "",
                    "token": "",
                }
            )
            .extract()
            .with_jmespath("body.data.verifyId", "verifyId")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("商家后台登录")
            .post("/business/api/web/login")
            .with_params(
                **{
                    "userName": "$business_userName",
                    "password": "$business_password",
                    "verifyCode": "$business_verifyCode",
                    "regType": "$business_regType",
                    "verifyId": "$verifyId",
                }
            )
            .with_headers(
                **{
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "",
                    "store-code": "",
                    "business-code": "",
                    "token": "",
                }
            )
            .with_json(
                {
                    "userName": "$business_userName",
                    "password": "$business_password",
                    "verifyCode": "$business_verifyCode",
                    "regType": "$business_regType",
                    "verifyId": "$verifyId",
                }
            )
            .extract()
            .with_jmespath("body.data.personDetailResDto.accountCode", "accountCode")
            .with_jmespath('body.data.personDetailResDto.accountId', "accountId")
            .with_jmespath('body.data.personDetailResDto.accountName', "accountName")
            .with_jmespath('body.data.personDetailResDto.employeeId', "employeeId")
            .with_jmespath('body.data.personDetailResDto.employeeName', "employeeName")
            .with_jmespath('body.data.sessionId', "sessionId")
            .with_jmespath('body.data.token', "token")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
    ]


if __name__ == "__main__":
    TestCaseBusinessLogin().test_start()
