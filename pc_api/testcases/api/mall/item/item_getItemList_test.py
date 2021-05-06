# 对于接口/mall/item/getItemList  查询商品列表

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.login_test.login_test import TestCaseLogin as Login
import os
"""
byClassIds string (query) 查推荐区分参数
currentPage integer($int64) (query) 当前页数
frontCategoryId integer($int64) (query) 前端类目Id
mustNot string (query) 需要过滤的商品编码
pageSize integer($int64) (query) 每页记录数
qp-classIds-in string (query) 品类名称
qp-status-eq string (query) 上下架。0下架 1上架
qp-storeCode-eq string (query)	 店铺Code
sorter-complex string (query) 综合排序
sorter-salePrice string (query) 价格排序
sorter-sales string (query) 销量排序 asc 或者 desc
sso_sessionid string (header) sessionid
x-tenant-id * string (header) tenant Default value : 2

method: get
"""

class TestCaseItemGetItemList(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "byClassIds-currentPage-frontCategoryId-mustNot-pageSize-qp_status_eq-qp_storeCode_eq-sorter_complex-sorter_salePrice-sorter_sales": "${parameterize(testcases/api/mall/item/item_getItemList.csv)}",
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("查询商品列表")
        .base_url("${get_base_url()}")
        # .variables(**{
        #     "byClassIds": "$byClassIds",  # string (query) 查推荐区分参数
        #     "currentPage": "$currentPage",  # integer($int64) (query) 当前页数
        #     "frontCategoryId": "$frontCategoryId",  # integer($int64) (query) 前端类目Id
        #     "mustNot": "$mustNot",  # string (query) 需要过滤的商品编码
        #     "pageSize": "$pageSize",  # integer($int64) (query) 每页记录数
        #     # "qp_classIds_in": "$qp_classIds_in",  #string (query) 品类名称
        #     "qp_status_eq": "$qp_status_eq",  # string (query) 上下架。0下架 1上架
        #     "qp_storeCode_eq": "$qp_storeCode_eq",  # string (query)	 店铺Code
        #     "sorter_complex": "$sorter_complex",  # string (query) 综合排序
        #     "sorter_salePrice": "$sorter_salePrice",  # string (query) 价格排序
        #     "sorter_sales": "$sorter_sales",  # string (query) 销量排序 asc 或者 desc
        #
        #     "x_tenant_id": "2",     #tenant Default value : 2     必填选项  header部分
        # })
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("登录")
            .call(Login)
            .export(*['sessionId', 'token', 'accountCode', 'personId', "name", "nickname", "username", "phone",
                      "memberCode", "userCode", "account_id", "storeCode", "member_id"])
        ),
        Step(
            RunRequest("查询商品列表")
            .get("/mall/item/getItemList")
            .with_params(
                **{
                    "qp-status-eq": "$qp_status_eq",
                    "qp-storeCode-eq": "$qp_storeCode_eq",
                    "frontCategoryId": "$frontCategoryId",
                    "totalCount": "0",
                    "currentPage": "1",
                    "pageSize": "16",
                    "sorter-complex": "$sorter_complex",
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
