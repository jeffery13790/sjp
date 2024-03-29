# NOTE: Generated By HttpRunner v3.1.4
# FROM: item_getItemList.har
"""
currentPage integer($int64) (query)	 当前页数
pageSize integer($int64) (query) 每页记录数
qp-brandId-in string (query) 品牌id
qp-businessCode-eq string (query) 商家编码
qp-categoryId-in string (query)	 类目id
qp-channelId-in string (query) 渠道id
qp-classId-in string (query) 品类id
qp-combination-eq string (query) 是否为组合商品:true or false
qp-createTime-eq string (query) 创建时间
qp-itemCode-eq string (query) 商品code
qp-name-like string (query) 商品名称
qp-ownerId-eq string (query) 	发布者id:0集团,1商家
qp-storeCode-eq * string (query)	店铺编码
sorter string (query) 排序条件 desc-字段名或者asc-字段名
sso_sessionid string (header) sessionid
x-tenant-id * string  (header) tenant Default value : 2

"""

from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase, Parameters
import pytest
from testcases.api.ops.opsLogin_test import TestCaseOpslogin as Login

class TestCaseItemGetitemlist(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "userName-password-verifyCode1-regType": "${parameterize(common.csv)}",
            "currentPage-pageSize-qp_brandId_in-qp_businessCode_eq-qp_categoryId_in-qp_channelId_in-qp_classId_in-qp_combination_eq-qp_createTime_eq-qp_itemCode_eq-qp_name_like-qp_ownerId_eq-qp_storeCode_eq-sorter": "${parameterize(testcases/api/ops/item/item_getItemList.csv)}",
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
            RunRequest("获取商品列表")
            .get("/ops/api/item/getItemList")
            .with_params(**{
                "currentPage": "$currentPage",
                "pageSize": "$pageSize",
                "qp-combination-eq": "$qp_combination_eq",
                "qp-ownerId-eq": "$qp_ownerId_eq",
                "qp-brandId-in": "$qp_brandId_in",
                "qp-businessCode-eq": "$qp_businessCode_eq",
                "qp-categoryId-in": "$qp_categoryId_in",
                "qp-channelId-in": "$qp_channelId_in",
                "qp-classId-in": "$qp_classId_in",
                "qp-createTime-eq": "$qp_createTime_eq",
                "qp-itemCode-eq": "$qp_itemCode_eq",
                "qp-name-like": "$qp_name_like",
                "qp-storeCode-eq": "$qp_storeCode_eq",
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
    TestCaseItemGetitemlist().test_start()
