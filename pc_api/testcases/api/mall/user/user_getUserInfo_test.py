# 对于接口/mall/user/getUserInfo   获取用户个人信息

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.api.mall.web_pcLogin_test import TestCaseWebPCLogin as Login
import ast

"""
sessionId * string (query) 登录返回sessionId

sso_sessionid string (header) sessionid
x-tenant-id * string (header) tenant Default value : 2

method: get
"""

class TestCaseUserGetUserInfo(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("获取个人信息")
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
            RunRequest("获取用户的个人信息")
            .get("/mall/user/getUserInfo")
            .with_params(
                **{"sessionId": "$sessionId"}
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
            .extract()
            .with_jmespath('body.data.accountResDto.accountCode', "accountCode")
            .with_jmespath('body.data.accountResDto.personId', "personId")
            .with_jmespath('body.data.accountResDto.name', "name")
            .with_jmespath('body.data.accountResDto.nickname', "nickname")
            .with_jmespath('body.data.accountResDto.username', "username")
            .with_jmespath('body.data.accountResDto.phone', "phone")
            .with_jmespath('body.data.memberCardResDto.memberCode', "memberCode")
            .with_jmespath('body.data.memberCardResDto.userId', "userId")
            .with_jmespath('body.data.personResDto.userCode', "userCode")
            .with_jmespath('body.data.accountResDto.id', "account_id")
            .with_jmespath('body.data.memberCardResDto.id', "member_id")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
    ]
