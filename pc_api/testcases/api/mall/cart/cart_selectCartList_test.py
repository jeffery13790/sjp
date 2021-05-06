# 对于接口/mall/cart/selectCartList  新版查询购物车，按照活动分组并排序-wxk，也就是列表(qp-参数支持的操作符号有: eq(=),ne(!=),gt(>),lt(<),ge(>=),le(<=),in,like,notLike,likeleft(左边LIKE '%xxx'),likeright(右边LIKE 'xx%'))

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.api.mall.web_pcLogin_test import TestCaseWebPCLogin as Login
import ast

"""
currentPage integer($int64) (query)	 当前页数
memberCode * string (query) 会员编码
pageSize * integer($int64) (query) 每页记录数
qp-buyerCode-eq * string (query) 买家code
qp-cartType-eq * string (query)	 购物车类型(默认0-普通)
qp-channelId-eq * string (query) 渠道id
qp-storeCode-eq * string (query) 店铺Code
sso_sessionid string (header) sessionid
x-tenant-id * string (header) tenant Default value : 2

method: get
"""

class TestCaseCartSelectCartList(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "memberCode-qp_buyerCode_eq-qp_storeCode_eq": "${parameterize(testcases/api/mall/cart/cart_selectCartList.csv)}",
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("新版查询购物车，按照活动分组并排序-wxk，也就是列表(qp-参数支持的操作符号有: eq(=),ne(!=),gt(>),lt(<),ge(>=),le(<=),in,like,notLike,likeleft(左边LIKE '%xxx'),likeright(右边LIKE 'xx%'))")
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
            .export(*['sessionId', 'token'])
        ),
        Step(
            RunRequest("/mall/cart/selectCartList")
            .get("/mall/cart/selectCartList")
            .with_params(
                **{
                    "cartType": "1",
                    "channel": "1",
                    "pageSize": "50",
                    "memberCode": "$memberCode",
                    "qp-buyerCode-eq": "$qp_buyerCode_eq",
                    "qp-cartType-eq": "0",
                    "qp-channelId-eq": "1",
                    "qp-storeCode-eq": "$qp_storeCode_eq",
                }
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
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
    ]
