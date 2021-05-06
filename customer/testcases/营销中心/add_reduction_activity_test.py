from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase
import pytest
from httprunner import Parameters
import datetime
import uuid


class TestCaseAddReductionActivity(HttpRunner):

    @pytest.mark.parametrize(
        'param',
        Parameters(
            {
                "x_app_id": ["200"],
                "x_tenant_id": ["2"],
                "password": ["200622"],
                "regType": [4],
                "userName": ["opsAdmin"],
                "verifyCode": ["1234"],
                "storeCode": ["STORE000086"],
                "activityName": ["api接口测试{}".format(uuid.uuid4().__str__().replace('-', '')[0:5])],
                "ticketDesc": ["api接口自动化测试新增库存策略，优惠券说明api，优惠券说明api接口自动化测试新增优惠券，优惠券说明api接口自动化测试新增优惠券，优惠券说明api接口自动化测试新增优惠券，优惠券说明api接口自动化测试新增优惠券，优惠券说明a"],
                "activityStart": ["{}T10:06:41.507Z".format((datetime.datetime.utcnow() - datetime.timedelta(days=-1)).strftime('%Y-%m-%d'))],
                "activiyEnd": ["{}T23:59:59.000Z".format((datetime.datetime.utcnow() - datetime.timedelta(days=-30)).strftime('%Y-%m-%d'))],
                "file_path": ['./image/reduction.jpg']
            }
        ),
    )
    def test_start(self, param):
        super().test_start(param)

    config = (
        Config("库存分配策略新增，删除")
        .base_url("${get_base_url()}")
        .verify(False)
        .export(*["token", "verifyId", "sessionId"])
    )

    teststeps = [
        Step(
            RunRequest("/ops/api/web/getVerificationCode")
            .get("/ops/api/web/getVerificationCode?")
            .with_headers(
                **{
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
                    "Token": "",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .extract()
            .with_jmespath("body.data.verifyId", "verifyId")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/web/login")
            .post("/ops/api/web/login")
            .with_headers(
                **{
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
                    "Token": "",
                    "Content-Type": "application/json; charset=utf-8",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .with_json(
                {
                    "userName": "$userName",
                    "password": "$password",
                    "verifyCode": "$verifyCode",
                    "verifyId": "$verifyId",
                    "regType": "$regType",
                }
            )
            .extract()
            .with_jmespath("body.data.token", "token")
            .with_jmespath("body.data.sessionId", "sessionId")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/activity/query")
            .get("/ops/api/activity/query?")
            .with_headers(
                **{
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                    "Token": "$token",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/brand/getBrandList")
            .get("/ops/api/brand/getBrandList")
            .with_params(**{"currentPage": "1", "pageSize": "10"})
            .with_headers(
                **{
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                    "Token": "$token",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuList")
            .get("/ops/api/sku/getSkuList")
            .with_params(**{"currentPage": "1", "pageSize": "10"})
            .with_headers(
                **{
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                    "Token": "$token",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .extract()
            .with_jmespath('body.data.list[0].itemCode', 'itemCode')
            .with_jmespath('body.data.list[0].itemName', 'itemName')
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/activity/addActivity")
            .post("/ops/api/activity/addActivity")
            .with_headers(
                **{
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                    "Token": "$token",
                    "Content-Type": "application/json; charset=utf-8",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .with_json(
                {
                    "activityName": "$activityName",
                    "activityDescription": "",
                    "activityStart": "$activityStart",
                    "activiyEnd": "$activiyEnd",
                    "activityStatus": 0,
                    "activityLevel": 0,
                    "templateName": "满减",
                    "templateCode": "FullReduction",
                    "activityType": "2",
                    "activityOwnerCode": 0,
                }
            )
            .extract()
            .with_jmespath('body.data.activityNo', 'activityNo')
            .with_jmespath('body.data.id', 'activity_id')
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/store/query")
            .get("/ops/api/store/query")
            .with_params(**{"currentPage": "1", "pageSize": "10"})
            .with_headers(
                **{
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                    "Token": "$token",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/activityStore/addBatch")
            .post("/ops/api/activityStore/addBatch")
            .with_headers(
                **{
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                    "Token": "$token",
                    "Content-Type": "application/json; charset=utf-8",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .with_json(
                [
                    {
                        "activityNo": "$activityNo",
                        "storeCode": "$storeCode",
                        "channel": "1",
                    }
                ]
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
            .assert_equal("body.data", None)
        ),
        Step(
            RunRequest("/ops/api/activity/editStatus")
            .patch("/ops/api/activity/editStatus")
            .with_headers(
                **{
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                    "Token": "$token",
                    "Content-Type": "application/json; charset=utf-8",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .with_json(
                {
                    "id": "$activity_id",
                    "activityNo": "$activityNo",
                    "templateName": "满减",
                    "templateCode": "FullReduction",
                    "activityName": "$activityName",
                    "activityStart": "$activityStart",
                    "activiyEnd": "$activiyEnd",
                    "activityType": 2,
                    "activityDescription": "",
                    "activityUrl": None,
                    "extData": None,
                    "activityChannel": "1",
                    "remarks": None,
                    "createUserId": "1",
                    "activityStatus": 0,
                    "activityParameters": '{"configurations":{"CHANNEL_RULE":{"values":[{"enable":true,"name":"电商","type":[{"enable":false,"name":"全部店铺","value":"1"},{"enable":true,"name":"部分店铺","value":"2"}],"value":"1"}],"name":"活动平台","id":"","desc":"活动平台","group":"group"},"PROMOTION_RULE":{"values":[{"range":"1000","value":"1"}],"name":"满减活动","id":"overoff","desc":"满减活动，满range元减value","group":"group"},"USER_RULE":{"values":[{"enable":true,"name":"黄金会员","value":"LV4"},{"enable":false,"name":"白银会员","value":"LV3"},{"enable":false,"name":"青铜会员","value":"LV2"},{"enable":false,"name":"铂金会员","value":"LV5"},{"enable":false,"name":"普通会员","value":"LV1"}],"name":"会员等级","id":"","desc":"活动会员等级","group":"group"},"USE_RANGE_TYPE":{"values":[{"enable":false,"name":"全部商品","value":"all"},{"enable":false,"name":"部分商品","value":"part"}],"name":"商品范围","id":"USE_RANGE_TYPE","desc":"商品范围","group":"radio"},"singlevalue":"configurationItemValue","OVERLYING_RULE":{"values":[{"enable":true,"name":"单品活动","value":"1"},{"enable":false,"name":"订单活动","value":"2"},{"enable":true,"name":"单品优惠券","value":"3"},{"enable":true,"name":"订单优惠券","value":"4"}],"name":"叠加规则","id":"","desc":"叠加规则","group":"group"}}}',
                    "activityOwnerCode": "0",
                    "activityLevel": 0,
                    "rejectOpinion": None,
                    "ticketRule": None,
                    "modifyUserId": "1",
                    "couponRange": None,
                    "activityPriority": 1898,
                    "subscript": None,
                    "activityRange": None,
                    "platformId": "0",
                    "tickets": None,
                    "createUserName": "运营平台管理员",
                    "modifyUserName": "运营平台管理员",
                    "createTime": "$activityStart",
                    "modifyTime": "$activiyEnd",
                    "goingCount": None,
                    "pendingCount": None,
                    "itemCode": None,
                    "skuCode": None,
                    "receive": False,
                    "ticketType": None,
                    "ticketId": None,
                    "ticketCode": None,
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuList")
            .get("/ops/api/sku/getSkuList")
            .with_params(**{"activityNo": "$activityNo", "activityRange": "2"})
            .with_headers(
                **{
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                    "Token": "$token",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/upload")
            .with_variables(
                **{
                    "file_path": "$file_path",
                    "m_encoder": "${multipart_encoder(file=$file_path)}",
                }
            )
            .post("/ops/api/upload")
            .with_headers(
                **{
                    "Connection": "keep-alive",
                    "x-tenant-id": "$x_tenant_id",
                    "X-Requested-With": "XMLHttpRequest",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                    "Token": "$token",
                    "Content-Type": "${multipart_content_type($m_encoder)}",
                    "Accept": "*/*",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .with_data("$m_encoder")
            .extract()
            .with_jmespath('body.data', 'subscript')
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/activityItem/addBatch")
            .post("/ops/api/activityItem/addBatch")
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                    "Token": "$token",
                    "Content-Type": "application/json; charset=utf-8",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .with_json(
                [
                    {
                        "activityNo": "$activityNo",
                        "stock": "",
                        "remarks": "",
                        "proPrice": "",
                        "itemCode": "$itemCode",
                        "itemName": "$itemName",
                        "skuCode": "XHSKU111466",
                    }
                ]
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
            .assert_equal("body.data", None)
        ),
        Step(
            RunRequest("/ops/api/activity/editStatus")
            .patch("/ops/api/activity/editStatus")
            .with_headers(
                **{
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                    "Token": "$token",
                    "Content-Type": "application/json; charset=utf-8",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .with_json(
                {
                    "id": "$activity_id",
                    "activityNo": "$activityNo",
                    "templateName": "满减",
                    "templateCode": "FullReduction",
                    "activityName": "$activityName",
                    "activityStart": "$activityStart",
                    "activiyEnd": "$activiyEnd",
                    "activityType": 2,
                    "activityDescription": "",
                    "activityUrl": None,
                    "extData": None,
                    "activityChannel": "1",
                    "remarks": None,
                    "createUserId": "1",
                    "activityStatus": 0,
                    "activityParameters": '{"configurations":{"CHANNEL_RULE":{"values":[{"enable":true,"name":"电商","type":[{"enable":false,"name":"全部店铺","value":"1"},{"enable":true,"name":"部分店铺","value":"2"}],"value":"1"}],"name":"活动平台","id":"","desc":"活动平台","group":"group"},"PROMOTION_RULE":{"values":[{"range":"1000","value":"1"}],"name":"满减活动","id":"overoff","desc":"满减活动，满range元减value","group":"group"},"USER_RULE":{"values":[{"enable":true,"name":"黄金会员","value":"LV4"},{"enable":false,"name":"白银会员","value":"LV3"},{"enable":false,"name":"青铜会员","value":"LV2"},{"enable":false,"name":"铂金会员","value":"LV5"},{"enable":false,"name":"普通会员","value":"LV1"}],"name":"会员等级","id":"","desc":"活动会员等级","group":"group"},"USE_RANGE_TYPE":{"values":[{"enable":false,"name":"全部商品","value":"all"},{"enable":true,"name":"部分商品","value":"part"}],"name":"商品范围","id":"USE_RANGE_TYPE","desc":"商品范围","group":"radio"},"singlevalue":"configurationItemValue","OVERLYING_RULE":{"values":[{"enable":true,"name":"单品活动","value":"1"},{"enable":false,"name":"订单活动","value":"2"},{"enable":true,"name":"单品优惠券","value":"3"},{"enable":true,"name":"订单优惠券","value":"4"}],"name":"叠加规则","id":"","desc":"叠加规则","group":"group"}}}',
                    "activityOwnerCode": "0",
                    "activityLevel": 0,
                    "rejectOpinion": None,
                    "ticketRule": None,
                    "modifyUserId": "1",
                    "couponRange": None,
                    "activityPriority": 1898,
                    "subscript": "$subscript",
                    "activityRange": 2,
                    "platformId": "0",
                    "tickets": None,
                    "createUserName": "运营平台管理员",
                    "modifyUserName": "运营平台管理员",
                    "createTime": "$activityStart",
                    "modifyTime": "$activiyEnd",
                    "goingCount": None,
                    "pendingCount": None,
                    "itemCode": None,
                    "skuCode": None,
                    "receive": False,
                    "ticketType": None,
                    "ticketId": None,
                    "ticketCode": None,
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
        ),
        Step(
            RunRequest("/ops/api/activity/editStatus")
            .patch("/ops/api/activity/editStatus")
            .with_headers(
                **{
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                    "Token": "$token",
                    "Content-Type": "application/json; charset=utf-8",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .with_json(
                {
                    "id": "$activity_id",
                    "activityNo": "$activityNo",
                    "templateName": "满减",
                    "templateCode": "FullReduction",
                    "activityName": "$activityName",
                    "activityStart": "$activityStart",
                    "activiyEnd": "$activiyEnd",
                    "activityType": 2,
                    "activityDescription": "",
                    "activityUrl": None,
                    "extData": None,
                    "activityChannel": "1",
                    "remarks": None,
                    "createUserId": "1",
                    "activityStatus": 0,
                    "activityParameters": '{"configurations":{"CHANNEL_RULE":{"values":[{"enable":true,"name":"电商","type":[{"enable":false,"name":"全部店铺","value":"1"},{"enable":true,"name":"部分店铺","value":"2"}],"value":"1"}],"name":"活动平台","id":"","desc":"活动平台","group":"group"},"PROMOTION_RULE":{"values":[{"range":"63","value":"2"}],"name":"满减活动","id":"overoff","desc":"满减活动，满range元减value","group":"group"},"USER_RULE":{"values":[{"enable":true,"name":"黄金会员","value":"LV4"},{"enable":false,"name":"白银会员","value":"LV3"},{"enable":false,"name":"青铜会员","value":"LV2"},{"enable":false,"name":"铂金会员","value":"LV5"},{"enable":false,"name":"普通会员","value":"LV1"}],"name":"会员等级","id":"","desc":"活动会员等级","group":"group"},"USE_RANGE_TYPE":{"values":[{"enable":false,"name":"全部商品","value":"all"},{"enable":true,"name":"部分商品","value":"part"}],"name":"商品范围","id":"USE_RANGE_TYPE","desc":"商品范围","group":"radio"},"singlevalue":"configurationItemValue","OVERLYING_RULE":{"values":[{"enable":true,"name":"单品活动","value":"1"},{"enable":false,"name":"订单活动","value":"2"},{"enable":true,"name":"单品优惠券","value":"3"},{"enable":true,"name":"订单优惠券","value":"4"}],"name":"叠加规则","id":"","desc":"叠加规则","group":"group"}}}',
                    "activityOwnerCode": "0",
                    "activityLevel": 0,
                    "rejectOpinion": None,
                    "ticketRule": None,
                    "modifyUserId": "1",
                    "couponRange": None,
                    "activityPriority": 1898,
                    "subscript": "$subscript",
                    "activityRange": 2,
                    "platformId": "0",
                    "tickets": None,
                    "createUserName": "运营平台管理员",
                    "modifyUserName": "运营平台管理员",
                    "createTime": "$activityStart",
                    "modifyTime": "$activiyEnd",
                    "goingCount": None,
                    "pendingCount": None,
                    "itemCode": None,
                    "skuCode": None,
                    "receive": False,
                    "ticketType": None,
                    "ticketId": None,
                    "ticketCode": None,
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
    TestCaseAddReductionActivity().test_start()
