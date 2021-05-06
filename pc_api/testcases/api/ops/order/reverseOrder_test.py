# NOTE: Generated By HttpRunner v3.1.4
# FROM: reverseOrder.har

"""
currentPage integer($int64) (query) 当前页数
pageSize integer($int64) (query) 每页记录数
qp-createTime-ge string (query) 开始时间
qp-createTime-le string (query) 结束时间
qp-orderNo-eq string (query) 订单编号
qp-phoneNumber-eq string (query) 手机号
qp-storeCode-in string (query) 店铺编码
sorter string (query) 排序条件 desc-字段名或者asc-字段名
sso_sessionid string (header) sessionid
x-tenant-id * string (header)	 tenant Default value : 2

"""


from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase, Parameters
import pytest
from testcases.api.ops.opsLogin_test import TestCaseOpslogin as Login


class TestCaseReverseorder(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "userName-password-verifyCode1-regType": "${parameterize(common.csv)}",
            "currentPage-pageSize-qp_createTime_ge-qp_createTime_le-qp_orderNo_eq-qp_phoneNumber_eq-qp_storeCode_in-sorter": "${parameterize(testcases/api/ops/order/reverseOrder.csv)}",
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
            RunTestCase("登录ops")
            .call(Login)
            .export(*["token", "sessionId"])
        ),
        Step(
            RunRequest("分页查逆向单，也就是列表")
            .get("/ops/api/reverseOrder/query?")
            .with_params(**{
                "currentPage": "$currentPage",
                "pageSize": "$pageSize",
                "qp-createTime-ge": "$qp_createTime_ge",
                "qp-createTime-le": "$qp_createTime_le",
                "qp-orderNo-eq": "$qp_orderNo_eq",
                "qp-phoneNumber-eq": "$qp_phoneNumber_eq",
                "qp-storeCode-in": "$qp_storeCode_in",
                "sorter": "$sorter"
            })
            .with_headers(
                **{
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "Token": "$token",
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


if __name__ == "__main__":
    TestCaseReverseorder().test_start()