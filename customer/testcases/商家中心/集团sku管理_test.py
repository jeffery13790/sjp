import json
import io
import os
import loguru
from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


def getCommonVariables(privateVariables={}):
    if not isinstance(privateVariables, dict):
        raise TypeError("公共变量函数的参数需要为字典形式：{}".format(privateVariables))
    privateVariables.update(getPrivateVariables())
    with io.open("common.json", "r") as f:
        data = json.load(f)
    # privateVariables = getPrivateVariables()
    if isinstance(data.get("variables", {}), dict) and isinstance(privateVariables, dict):
        #在这里填写参数数据
        data["variables"].update(privateVariables)
    else:
        raise Exception("参数类型错误")
    return data["variables"]

def getCommonHeaser(privateHeaders={}):
    with io.open("common.json", "r") as f:
        common = json.load(f)
    commonHeaders = common.get("headers", {})
    if isinstance(commonHeaders, dict) and commonHeaders and isinstance(privateHeaders, dict):
        commonHeaders.update(privateHeaders)
        return commonHeaders
    elif not isinstance(commonHeaders, dict) or not isinstance(privateHeaders, dict):
        raise TypeError("数据格式错误commonHeaders = {}, privateHeaders = {}".format(commonHeaders, privateHeaders))

def getPrivateVariables():
    current_dir = os.path.dirname(__file__)
    current_file = os.path.basename(__file__)
    if current_file.endswith(".py"):
        private_variable_file = os.path.join(current_dir, "{}.json".format(current_file[0:current_file.rindex(".")]))
    else:
        raise FileExistsError("文件不存在：{}".format(current_file))
    if os.path.isfile(private_variable_file):
        with io.open(private_variable_file, 'r') as f:
            privateVariables = json.load(f)
            if isinstance(private_variable_file, list) and len(private_variable_file):
                if isinstance(private_variable_file[0], dict):
                    return private_variable_file[0]
                else:
                    raise TypeError("参数类型不是字典类型，请求改以后在行执行：{}".format(os.path.abspath(__file__)))
            elif isinstance(private_variable_file, dict):
                return private_variable_file
    else:
        loguru.logger.warning("{}测试用例的私有配置文件{}不存在".format(os.path.abspath(__file__), private_variable_file))
        return {}

class TestCaseLogin(HttpRunner):
    config = (
        Config("testcase description")
        .variables(**getCommonVariables())
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
                    #
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
                    # #
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
                    #
                    "Connection": "keep-alive",
                    #  "Content-Length": "107",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
                    "Token": "",
                    "Content-Type": "application/json; charset=utf-8",
                    # "Origin": "",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    #
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
            RunRequest("/ops/api/brand/getBrandList")
            .get("/ops/api/brand/getBrandList?")
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476099711820d0001")
        ),
        Step(
            RunRequest("/ops/api/class/getClassList")
            .get("/ops/api/class/getClassList")
            .with_params(**{"current": "1", "pageSize": "10"})
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476099771821d0001")
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuSignList")
            .get("/ops/api/sku/getSkuSignList")
            .with_params(**{"qp-ownerId-eq": "0"})
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476099841822d0001")
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuSignList")
            .get("/ops/api/sku/getSkuSignList")
            .with_params(**{"qp-skuCode-like": "XHSKU82", "qp-ownerId-eq": "0"})
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476257621826d0001")
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuSignList")
            .get("/ops/api/sku/getSkuSignList")
            .with_params(
                **{
                    "qp-skuCode-like": "XHSKU82",
                    "qp-name-like": "十二",
                    "qp-ownerId-eq": "0",
                }
            )
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476359341829d0001")
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuSignList")
            .get("/ops/api/sku/getSkuSignList")
            .with_params(
                **{
                    "qp-skuCode-like": "XHSKU82",
                    "qp-name-like": "十二",
                    "qp-classId-in": "1267997599515484162",
                    "qp-ownerId-eq": "0",
                }
            )
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476399111831d0001")
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuSignList")
            .get("/ops/api/sku/getSkuSignList")
            .with_params(
                **{
                    "qp-skuCode-like": "XHSKU82",
                    "qp-name-like": "十二",
                    "qp-classId-in": "1267997599515484162",
                    "qp-brandId-in": "1259828930640547841",
                    "qp-ownerId-eq": "0",
                }
            )
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476429011832d0001")
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuSignList")
            .get("/ops/api/sku/getSkuSignList")
            .with_params(**{"qp-ownerId-eq": "0"})
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476453861834d0001")
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuListBySKuCodes")
            .get("/ops/api/sku/getSkuListBySKuCodes")
            .with_params(**{"skuCodes": "XHSKU82"})
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476535261836d0001")
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuSignList")
            .get("/ops/api/sku/getSkuSignList")
            .with_params(**{"qp-ownerId-eq": "0"})
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476580431838d0001")
        ),
        Step(
            RunRequest("/ops/api/labelGroup/queryLabelGroup")
            .get("/ops/api/labelGroup/queryLabelGroup")
            .with_params(
                **{"currentPage": "1", "pageSize": "100000", "qp-type-eq": "2"}
            )
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476651401841d0001")
        ),
        Step(
            RunRequest("/ops/api/label/list")
            .get("/ops/api/label/list")
            .with_params(
                **{
                    "currentPage": "1",
                    "pageSize": "100000",
                    "qp-groupType-eq": "2",
                    "qp-failureTime-ge": "2020-06-30 00:14:31",
                }
            )
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476653961842d0001")
        ),
        Step(
            RunRequest("/ops/api/label/queryLabelBySkuId")
            .get("/ops/api/label/queryLabelBySkuId")
            .with_params(**{"skuIds": "1261864554453843970"})
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476654981843d0001")
        ),
        Step(
            RunRequest("/ops/api/label/list")
            .get("/ops/api/label/list")
            .with_params(
                **{
                    "qp-groupId-eq": "722820094255828992",
                    "qp-failureTime-ge": "2020-06-30 00:14:31",
                }
            )
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476679791844d0001")
        ),
        Step(
            RunRequest("/ops/api/skuLabel/addSkuLabel")
            .post("/ops/api/skuLabel/addSkuLabel")
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Content-Length": "64",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                    "Token": "$token",
                    "Content-Type": "application/json; charset=utf-8",
                    "Origin": "",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",

                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }
            )
            .with_json(
                {"labelIds": "722821532797243392", "skuIds": "1261864554453843970"}
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "application/json;charset=UTF-8")
            .assert_equal("body.code", "000000")
            .assert_equal("body.msg", "Success")
            #.assert_equal("body.traceId", "ac1400d215934476736841846d0001")
            .assert_equal("body.data", True)
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuListBySKuCodes")
            .get("/ops/api/sku/getSkuListBySKuCodes")
            .with_params(**{"skuCodes": "XHSKU82"})
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476846501850d0001")
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuSignList")
            .get("/ops/api/sku/getSkuSignList")
            .with_params(**{"qp-ownerId-eq": "0"})
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476883391851d0001")
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuListBySKuCodes")
            .get("/ops/api/sku/getSkuListBySKuCodes")
            .with_params(**{"skuCodes": "XHSKU82"})
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476923611853d0001")
        ),
        Step(
            RunRequest("/ops/api/sku/getSkuSignList")
            .get("/ops/api/sku/getSkuSignList")
            .with_params(**{"qp-ownerId-eq": "0"})
            .with_headers(
                **{

                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
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
            #.assert_equal("body.traceId", "ac1400d215934476951131855d0001")
        ),
    ]


if __name__ == "__main__":
    TestCase集团Sku管理().test_start()
