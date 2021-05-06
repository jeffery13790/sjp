# 对于接口/mall/search/queryItemList  查询商品信息

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.login_test.login_test import TestCaseLogin as Login

"""
currentPage integer($int64) (query)	当前页数
keyWord string (query)	关键字
pageSize integer($int64) (query) 每页记录数
qp-brandIds-in string (query) 品牌ID
qp-categoryIds-in string (query) 类目Id
qp-classIds-in string (query) 品类id
qp-itemCodes-in string (query)	商品code
qp-labelIds-in string (query) 标签ids
qp-salePrice-ge string (query) 价格大于等于
qp-salePrice-le string (query) 价格小于等于
qp-status-eq * string (query) 状态 0下架 1上架
qp-storeCode-eq * string (query) 店铺Code
sorter-complex string (query) 综合排序 desc 或者 asc
sorter-salePrice string (query) 价格排序 desc 或者 asc
sorter-sales string (query) 销量排序 desc 或者 asc
sso_sessionid string (header) sessionid
userCode string (query)	 用户code
x-tenant-id * string (header) tenant Default value : 2

method: get
"""

class TestCaseSearchQueryItemList(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "good_name": "${get_good_name()}"
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("查询商品信息接口")
        .base_url("${get_base_url()}")
        .variables(**{
            "currentPage": "1", #当前页
            "keyWord": "$good_name", #商品名称
            "pageSize": "16", #每页记录数
            "qp_status_eq": "1", #状态 0下架 1上架            此为必填项
            "x_tenant_id": "2", #tenant Default value : 2     必填选项  header部分
        })
        .export(*["itemCode", "categoryId", "classId", "skuCode"])
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("登录")
                # .with_variables(**{})
                .call(Login)
                .export(*['sessionId', 'token', 'accountCode', 'personId', "name", "nickname", "username", "phone",
                          "memberCode", "userCode", "account_id", "storeCode", "member_id"])
        ),
        Step(
            RunRequest("查询商品")
            .get("/mall/search/queryItemList")
            .with_params(
                **{
                    "pageSize": "$pageSize",
                    "keyWord": "$keyWord",
                    "qp-status-eq": "$qp_status_eq",
                    "qp-storeCode-eq": "$storeCode",
                }
            )
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
            .extract()
            .with_jmespath('body.data.list[0].itemCode', 'itemCode')
            .with_jmespath('body.data.list[0].categoryId', "categoryId")
            .with_jmespath('body.data.list[0].classId', "classId")
            .with_jmespath('body.data.list[0].skuCode', "skuCode")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
    ]
