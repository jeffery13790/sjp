# 对于接口/mall/cart/save  添加商品到购物车

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.login_test.login_test import TestCaseLogin as Login
import ast

"""
reqDto * 要保存的对象
{
  "buyerCode": "string",
  "cartType": 0,
  "channelId": 0,
  "classCode": "string",
  "isChoice": 0,
  "itemCode": "string",
  "packingUnit": "string",
  "sellerCode": "string",
  "skuCode": "string",
  "skuQuantity": 0,
  "storeCode": "string",
  "taxRate": "string",
  "taxRateCode": "string"
}

sso_sessionid string (header) sessionid
x-tenant-id * string (header) tenant Default value : 2

method: get
"""

class TestCaseCartSave(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "buyerCode-cartType-channelId-isChoice-itemCode-packingUnit-sellerCode-skuCode-skuQuantity-storeCode-qp_storeCode_eq-taxRate-taxRateCode-status_code-body_code-body_msg": "${parameterize(testcases/api/mall/cart/cart_save.csv)}"
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("添加商品到购物车")
        .base_url("${get_base_url()}")
        .variables(**{
            "x_tenant_id": "2", #tenant Default value : 2     必填选项  header部分
        })
        .export(*['sessionId', 'token'])
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("登录")
            .with_variables(**{
                "x_tenant_id": "3"
            })
            .call(Login)
            .export(*['sessionId', 'token', 'accountCode', 'personId', "name", "nickname", "username", "phone", "memberCode", "userCode", "account_id", "storeCode", "member_id"])
        ),
        Step(
            RunRequest("把商品添加到购物车")
            .post("/mall/cart/save")
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
            .with_json(
                {
                    "buyerCode": "$buyerCode",
                    "cartType": "$cartType",
                    "channelId": "$channelId",
                    "isChoice": "$isChoice",
                    "itemCode": "$itemCode",
                    "packingUnit": "$packingUnit",
                    "sellerCode": "$sellerCode",
                    "skuCode": "$skuCode",
                    "skuQuantity": "$skuQuantity",
                    "storeCode": "$storeCode",
                    "qp-storeCode-eq": "$qp_storeCode_eq",
                    "taxRate": "$taxRate",
                    "taxRateCode": "$taxRateCode",
                }
            )
            .extract()
            .with_jmespath('body.data.id', "id")
            .validate()
            .assert_equal("status_code", "${get_Status_code($status_code)}")
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "$body_code")
            .assert_equal("body.msg", "$body_msg")
        ),
        Step(
            RunRequest("/mall/cart/delete")
                .delete("/mall/cart/delete")
                .with_params(
                **{
                    "qp-buyerCode-eq": "$buyerCode",
                    "qp-cartType-eq": "0",
                    "qp-channelId-eq": "1",
                    "qp-id-in": "$id",
                    "qp-storeCode-eq": "$$qp_storeCode_eq",
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
