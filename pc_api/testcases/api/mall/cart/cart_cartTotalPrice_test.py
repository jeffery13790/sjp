# 对于接口/mall/cart/cartTotalPrice  计算购物车中选中商品的价格

from httprunner import HttpRunner, Config, Step, RunTestCase, RunRequest, Parameters
import pytest
from testcases.api.mall.cart.cart_save_test import TestCaseCartSave as CartSave

"""
reqDto  * 待计算的数据
{
  "buyerCode": "string",
  "calStep": 0,
  "cartLineReqDtos": [
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
  ],
  "cartType": 0,
  "channel": 0,
  "memberCardCode": "string",
  "orderAddressReqDto": {
    "cityName": "string",
    "consignee": "string",
    "detail": "string",
    "detailAddress": "string",
    "districtName": "string",
    "phone": "string",
    "phoneNumber": "string",
    "provinceName": "string",
    "receiver": "string",
    "zipcode": "string"
  },
  "orderLineList": [
    {
      "id": "string",
      "selectedGoodsTicket": 0
    }
  ],
  "orderSource": 0,
  "selectedGoodsTickets": [
    0
  ],
  "selectedOrderTicketIds": [
    0
  ],
  "sellerCode": "string",
  "storeCode": "string",
  "tradeType": 0
}

sso_sessionid string (header) sessionid
x-tenant-id * string (header) tenant Default value : 2

method: get
"""

class TestCaseCartTotalPrice(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "phoneNumber-verifyCode": "${parameterize(common.csv)}",
            "buyerCode-cartType-channelId-isChoice-itemCode-packingUnit-sellerCode-skuCode-skuQuantity-storeCode-qp_storeCode_eq-taxRate-taxRateCode-status_code-body_code-body_msg": "${parameterize(testcases/api/mall/cart/cart_save.csv)}",
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("计算购物车中选中商品的价格")
        .base_url("${get_base_url()}")
        .variables(**{
            "x_tenant_id": "2", #tenant Default value : 2     必填选项  header部分
        })
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("把商品加入购物车")
            .call(CartSave)
            .export(*['sessionId', 'token', "id", 'accountCode', 'personId', "name", "nickname", "username", "phone", "memberCode", "userCode", "account_id", "storeCode", "member_id"])
        ),
        Step(
            RunRequest("计算购物车中选中商品的价格")
            .post("/mall/cart/cartTotalPrice")
            .with_headers(
                **{
                    "x-tenant-id": "2",
                    "sso_sessionid": "$sessionId",
                }
            )
            .with_json(
                {
                    "orderLineList": [
                        {"id": "$id", "selectedGoodsTicket": 0}
                    ],
                    "buyerCode": "$buyerCode",
                    "cartType": 0,
                    "calStep": 1,
                    "channel": 1,
                    "memberCardCode": "$memberCode",
                    "orderSource": 1,
                    "selectedOrderTicketId": 0,
                    "sellerCode": "SJ001",
                    "storeCode": "$storeCode",
                    "tradeType": 8,
                    "selectedOrderTicketIds": [0],
                }
            )
                .validate()
                .assert_equal("status_code", 200)
                .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
                .assert_equal("body.code", "000000")
                .assert_equal("body.msg", "Success")
        ),
    ]
