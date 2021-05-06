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
            RunRequest("/ops/api/vwStock/getVwStockList")
            .get("/ops/api/vwStock/getVwStockList?")
            .with_headers(
                **{
                    
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
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
            RunRequest("/ops/api/class/getClassList")
            .get("/ops/api/class/getClassList")
            .with_params(**{"current": "1", "pageSize": "500"})
            .with_headers(
                **{
                    
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
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
            RunRequest("/ops/api/category/getCategoryList")
            .get("/ops/api/category/getCategoryList?")
            .with_headers(
                **{
                    
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
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
            RunRequest("/ops/api/virtualWarehouse/getVirtualWarehouseList")
            .get(
                "/ops/api/virtualWarehouse/getVirtualWarehouseList"
            )
            .with_params(**{"current": "1", "pageSize": "500"})
            .with_headers(
                **{
                    
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
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
            RunRequest("/ops/api/vwStock/getVwStockList")
            .get("/ops/api/vwStock/getVwStockList")
            .with_params(
                **{
                    "qp-virtualWarehouseCode-eq": "VW20200629000004",
                    "qp-skuCode-eq": "XHSKU1769",
                    "qp-name-like": "富有的习惯",
                    "qp-categoryId-eq": "722852300328669184",
                    "qp-classId-eq": "1267997599515484162",
                    "qp-availableStock-gt": "0",
                }
            )
            .with_headers(
                **{
                    
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
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
            RunRequest("/ops/api/vwStock/getVwStockList")
            .get("/ops/api/vwStock/getVwStockList")
            .with_params(
                **{
                    "qp-virtualWarehouseCode-eq": "VW20200629000004",
                    "qp-skuCode-eq": "XHSKU1769",
                    "qp-name-like": "富有的习惯",
                    "qp-categoryId-eq": "722852300328669184",
                    "qp-classId-eq": "1267997599515484162",
                }
            )
            .with_headers(
                **{
                    
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
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
            RunRequest("/ops/api/vwStock/getVwStockList")
            .get("/ops/api/vwStock/getVwStockList")
            .with_params(
                **{
                    "qp-virtualWarehouseCode-eq": "VW20200629000004",
                    "qp-skuCode-eq": "XHSKU1769",
                    "qp-name-like": "富有的习惯",
                    "qp-categoryId-eq": "722852300328669184",
                }
            )
            .with_headers(
                **{
                    
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
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
            RunRequest("/ops/api/vwStock/getVwStockList")
            .get("/ops/api/vwStock/getVwStockList")
            .with_params(
                **{
                    "qp-virtualWarehouseCode-eq": "VW20200629000004",
                    "qp-skuCode-eq": "XHSKU1769",
                    "qp-name-like": "富有的习惯",
                }
            )
            .with_headers(
                **{
                    
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
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
            RunRequest("/ops/api/vwStock/getVwStockList")
            .get("/ops/api/vwStock/getVwStockList")
            .with_params(
                **{
                    "qp-virtualWarehouseCode-eq": "VW20200629000004",
                    "qp-skuCode-eq": "XHSKU1769",
                }
            )
            .with_headers(
                **{
                    
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
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
            RunRequest("/ops/api/vwStock/getVwStockList")
            .get("/ops/api/vwStock/getVwStockList")
            .with_params(**{"qp-virtualWarehouseCode-eq": "VW20200629000004"})
            .with_headers(
                **{
                    
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
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
            RunRequest("/ops/api/vwStock/getVwStockList")
            .get("/ops/api/vwStock/getVwStockList?")
            .with_headers(
                **{
                    
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
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
            RunRequest("/ops/api/vwStock/getVwStockList")
            .get("/ops/api/vwStock/getVwStockList")
            .with_params(**{"currentPage": "20", "pageSize": "10"})
            .with_headers(
                **{
                    
                    "Connection": "keep-alive",
                    "Accept": "application/json",
                    "x-app-id": "$x_app_id",
                    "x-tenant-id": "$x_tenant_id",
                    "sso_sessionid": "$sessionId",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
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
    ]


if __name__ == "__main__":
    TestCase虚仓库存查询().test_start()
