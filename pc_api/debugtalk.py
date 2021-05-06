
from loguru import logger
import uuid
import time
import ast


# 获取基础url地址的函数

def get_base_url():
    return "https://cs1.jsbooks.com.cn"

#这个是为了使用api直接修改订单状态 通过事件驱动
def get_trade_url():
    return "http://101.133.106.76:38286"

def get_good_name():
    return ["证券分析：原书第6版", "公文高手的修炼之道 笔杆子的写作必修课", "马云全传", "蔡康永的情商课"]

def get_store_code():
    storeCode = "STORE000086"
    return storeCode


def teardown_hook_sleep_N_secs(response, n_secs):
    if response.status_code == 200:
        time.sleep(n_secs)
    else:
        time.sleep(0.5)


def get_tenantId():
    return "2"

def get_appid():
    return  "201"

def get_Status_code(status_code):
    return ast.literal_eval(status_code)


