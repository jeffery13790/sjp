# 对于接口/mall/homeTemplate/getItemPagerByYourLike  猜你喜欢

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.login_test.login_test import TestCaseLogin as Login
import os
"""
currentPage integer($int64) (query)	 当前页数
pageSize integer($int64) (query) 每页记录数
qp-storeCode-eq * string (query)  storeCode
userCode string (query) 用户code
sso_sessionid string (header) sessionid
x-tenant-id * string (header)	tenant Default value : 2

method: get
"""

class TestCaseHomeTGetPageByYourLike(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "currentPage-pageSize-qp_storeCode_eq-userCode": "${parameterize(testcases/api/mall/homeTemplate/homeT_getPageByYourLike.csv)}"
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("查询获取一个商品的详情")
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
            RunRequest("猜你喜欢")
            .get("/mall/homeTemplate/getItemPagerByYourLike")
            .with_params(**{"qp-storeCode-eq": "$qp_storeCode_eq", "pageSize": "12", "userCode": "$userCode"})
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
