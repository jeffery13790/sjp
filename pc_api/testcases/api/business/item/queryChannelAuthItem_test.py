

"""
currentPage integer($int64) (query) 当前页数
pageSize integer($int64) (query) 每页记录数
qp-name-eq string (query)	 名称
qp-phone-eq string (query) 手机
qp-status-eq string (query) 账号状态：1-正常 11-停用
qp-username-eq string (query) 登录名
sorter string (query) 排序条件 desc-字段名或者asc-字段名
sso_sessionid string (header)	 sessionid
x-tenant-id * string (header) tenant Default value : 2
"""

from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase, Parameters
import pytest
from testcases.api.business.business_login_test import TestCaseBusinessLogin as Login


class TestCaseQueryChannelAuthItem(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "business_userName-business_password-business_verifyCode-business_regType": "${parameterize(common.csv)}",
            "qp_combination_eq-qp_ownerId_eq": "${parameterize(testcases/api/business/item/queryChannelAuthItem.csv)}",
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("登录business环境")
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
            RunTestCase("登录ops")
            .call(Login)
            .export(*["token", "sessionId",'accountCode'])
        ),
        Step(
            RunRequest("查询渠道授权商品 田磊")
            .get("/business/api/item/queryChannelAuthItem")
            .with_params(**{
                "qp-combination-eq": "$qp_combination_eq",
                "qp-ownerId-eq": "$qp_ownerId_eq",
            })
            .with_headers(
                **{
                    "business-code": "$accountCode",
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