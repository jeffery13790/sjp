# NOTE: Generated By HttpRunner v3.1.4
# FROM: ticket_query.har

"""
currentPage integer($int64) (query) 当前页数
pageSize integer($int64) (query)	 每页记录数
qp-createTime-ge string (query) 大于创建时间
qp-createTime-le string (query) 小于创建时间
qp-createUserId-eq string (query)
qp-effectivetimeEnd-eq   string (query) 有效结束时间
qp-effectivetimeStart-eq string (query) 有效开始时间
qp-ticketChannel-like string (query) 优惠券渠道
qp-ticketCode-eq string (query) 优惠券编码
qp-ticketName-eq string (query)	 优惠券名称
qp-ticketStatus-eq string (query) 优惠券状态：0-未提交/1-待审核/2-审核通过/3-审核拒绝/4-活动中/5-已结束已过期/6-已关闭
qp-ticketType-eq string (query) 优惠券类型：1-抵现券/2-折扣券/3-单品优惠券
sorter  string (query) 排序条件 desc-字段名或者asc-字段名
sso_sessionid string (header) sessionid
x-tenant-id * string (header) tenant Default value : 2
"""

from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase, Parameters
import pytest
from testcases.api.ops.opsLogin_test import TestCaseOpslogin as Login



class TestCaseTicketQuery(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "userName-password-verifyCode1-regType": "${parameterize(common.csv)}",
            "currentPage-pageSize-qp_barCode_eq-qp_brandId_in-qp_categoryId_in-qp_classId_in-qp_combination_eq-qp_labelIds_like-qp_name_like-qp_ownerId_eq-qp_skuCode_eq-qp_storeCode_eq-skuNameOrCode-sorter": "${parameterize(testcases/api/ops/item/getSkuList.csv)}",
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
            RunTestCase("登录")
            .call(Login)
            .export(*["sessionId", "token"])
        ),
        Step(
            RunRequest("分页查询优惠券列表")
            .get("/ops/api/ticket/query?")
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
    TestCaseTicketQuery().test_start()
