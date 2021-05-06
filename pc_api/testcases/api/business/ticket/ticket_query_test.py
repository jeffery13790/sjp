# NOTE: Generated By HttpRunner v3.1.4
# FROM: ticket_query.har

"""
currentPage integer($int64) (query)当前页数
pageSize integer($int64) (query) 每页记录数
qp-createTime-ge string (query) 大于创建时间
qp-createTime-le string (query) 小于创建时间
qp-createUserId-eq string (query)
qp-effectivetimeEnd-eq string (query)	有效结束时间
qp-effectivetimeStart-eq string (query) 有效开始时间
qp-ticketChannel-like string (query) 优惠券渠道
qp-ticketCode-eq string (query) 优惠券编码
qp-ticketName-eq string (query) 优惠券名称
qp-ticketStatus-eq string (query) 优惠券状态：0-未提交/1-待审核/2-审核通过/3-审核拒绝/4-活动中/5-已结束已过期/6-已关闭
qp-ticketType-eq string (query) 优惠券类型：1-抵现券/2-折扣券/3-单品优惠券
sorter string (query) 排序条件 desc-字段名或者asc-字段名
sso_sessionid string (header) sessionid
x-tenant-id * string (header) tenant Default value : 2

"""

from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase, Parameters
import pytest
from testcases.api.business.business_login_test import TestCaseBusinessLogin as Login


class TestCaseTicketQuery(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "business_userName-business_password-business_verifyCode-business_regType": "${parameterize(common.csv)}",
            "store_code-currentPage-pageSize-qp_createTime_ge-qp_createTime_le-qp_createUserId_eq-qp_effectivetimeStart_ge-qp_effectivetimeStart_le-qp_ticketChannel_like-qp_ticketCode_eq-qp_ticketName_eq-qp_ticketStatus_eq-qp_ticketType_eq-sorter": "${parameterize(testcases/api/business/ticket/ticket_query.csv)}"
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
            RunRequest("分页查询优惠券列表")
            .get("/business/api/ticket/query?")
            .with_params(**{
                # "qp-ticketName-like": "$qp_ticketName_eq",
                # "qp-ticketCode-eq": "$qp_ticketCode_eq",
                # "qp-createTime-ge": "$qp_createTime_ge",
                # "qp-createTime-le": "$qp_createTime_le",
                # "qp-effectivetimeStart-ge": "$qp_effectivetimeStart_ge",
                # "qp-effectivetimeStart-le": "$qp_effectivetimeStart_le",
                # "qp-ticketType-in": "$qp_ticketType_eq",
                # "qp-ticketStatus-in": "$qp_ticketStatus_eq",
                # "currentPage": "$currentPage",
                # "pageSize": "$pageSize",
                # "qp-createUserId-eq": "$qp_createUserId_eq",
                # "qp-ticketChannel-like": "$qp_ticketChannel_like",
                # "sorter": "$sorter"
            })
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
    TestCaseTicketQuery().test_start()