# NOTE: Generated By HttpRunner v3.1.4
# FROM: sendGood.har


from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase, Parameters
import pytest
from testcases.order_test.create_to_send_order_test import TestCaseCreateCancelObligationOrder as ObligationOrder
from testcases.login_test.customer_login_test import TestCaseCustomerLogin as CustomerLogin



class TestCaseSendgood(HttpRunner):

    @pytest.mark.parametrize(
        "param",
        Parameters({
            "good_name": "${get_good_name()}"
        })
    )
    def test_start(self, param) -> "HttpRunner":
        super().test_start(param)

    config = (
        Config("testcase description")
        .variables(**{
            "logisticsNo": "1111111111",
        })
        .base_url("${get_base_url()}")
        .export(*['sessionId', 'token', 'accountCode', 'personId',  "memberCode", 'orderNo', "storeCode", "member_id", "nickname"])
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("生成待发货订单")
            .with_variables(**{
                "phoneNumber": "18856012041",
                "verifyCode": "123456"
            })
            .call(ObligationOrder)
            .export(*['sessionId', 'token', 'accountCode', 'personId',  "memberCode", 'orderNo', "storeCode", "member_id", "nickname"])
        ),
        Step(
            RunTestCase("运营平台登录")
            .with_variables(**{
                "userName": "opsAdmin",
                "password": "200622",
                "verifyCode": "1234",
                "regType": 4,
            })
            .call(CustomerLogin)
            .export(*["customer_token", "customer_sessionId"])
        ),

        Step(
            RunRequest("/ops/api/order/query")
            .get("/ops/api/order/query")
            .with_params(**{"currentPage": "1", "pageSize": "10"})
            .with_headers(
                **{
                    "x-tenant-id": "2",
                    "sso_sessionid": "$customer_sessionId",
                    "Token": "$customer_token",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/order/selectOrderLineByOwner")
            .get("/ops/api/order/selectOrderLineByOwner")
            .with_params(**{"orderNo": "$orderNo", "ownerId": "0"})
            .with_headers(
                **{
                    "x-app-id": "200",
                    "x-tenant-id": "2",
                    "sso_sessionid": "$customer_sessionId",
                    "Token": "$customer_token",
                }
            )
            .extract()
            .with_jmespath('body.data.list[0].recordCode', "recordCode")
            .with_jmespath('body.data.list[0].skuCode', "skuCode")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/logisticsCompany/getCompanyListNoPage")
            .get(
                "/ops/api/logisticsCompany/getCompanyListNoPage?"
            )
            .with_headers(
                **{
                    "x-app-id": "200",
                    "x-tenant-id": "2",
                    "sso_sessionid": "$customer_sessionId",
                    "Token": "$customer_token",
                }
            )
            .extract()
            .with_jmespath('body.data[0].logisticsCompanyName', "logisticsCompanyName")
            .with_jmespath('body.data[0].logisticsCompanyCode', "logisticsCompanyCode")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/RwResultRecord/addBySend")
            .post("/ops/api/RwResultRecord/addBySend")
            .with_headers(
                **{
                    "x-app-id": "200",
                    "x-tenant-id": "2",
                    "sso_sessionid": "$customer_sessionId",
                    "Token": "$customer_token",
                }
            )
            .with_json(
                {
                    "logisticsCompanyCode": "$logisticsCompanyCode",
                    "logisticsCompanyName": "$logisticsCompanyName",
                    "logisticsNo": "$logisticsNo",
                    "recordCode": "$recordCode",
                    "orderNo": "$orderNo",
                    "skuList": [{"skuCode": "$skuCode", "skuQuantity": 1}],
                    "isSplit": False,
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/order/query")
            .get("/ops/api/order/query?")
            .with_headers(
                **{
                    "x-app-id": "200",
                    "x-tenant-id": "2",
                    "sso_sessionid": "$customer_sessionId",
                    "Token": "$customer_token",
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
    TestCaseSendgood().test_start()
