import json
import requests
import uuid
import os


# 酷学院/酷学云签到
def sign(access_token, enterprise_id, user_id):
    url = f'https://coolapi.coolcollege.cn/incentive-api/v2/enterprises/{enterprise_id}/users/{user_id}/sign/today'
    # 签到body
    data = {"access_token": access_token}

    # 头部信息
    header = {
        "authority": "coolapi.coolcollege.cn",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "app-id": "3829",
        "content-length": "51",
        "Content-Type": "application/json",
        "enterprise-id": enterprise_id,
        "origin": "https://pro.coolcollege.cn",
        "priority": "u=1, i",
        "referer": "https://pro.coolcollege.cn/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": "Windows",
        "accept": "application/json, text/plain, */*",
        "x-access-token": access_token
    }
    # 签到请求
    response = requests.post(url, data=json.dumps(data), headers=header).json()

    # 签到结果
    try:
        if response['code'] == 20000 and response['msg'] == 'success':
            print('签到成功')
        elif response['code'] == 40000 and response['msg'] == 'has signed':
            print('当天已签到，本次签到重复！')
        else:
            print('接口返回不符合预期，查看接口返回：\n', response)
    except AttributeError:
        print('接口报错：\n', response)


# 登录酷学院/酷学云
def login(mobile_yxt, password_yxt):

    # 随机请求
    new_uuid = str(uuid.uuid4())

    url = 'https://coolapi.coolcollege.cn/login-api/v3/login'
    # 信息body
    data = {
        "enterprise_id": "",
        "login_type": "account_password_login",
        "mobile": mobile_yxt,
        "outer_login_type": "",
        "password": password_yxt,
        "password_encrypted": "1",
        "sms_code": ""
    }

    # 头部
    header = {
        "authority": "coolapi.coolcollege.cn",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "app-id": "3829",
        "content-length": "328",
        "Content-Type": "application/json",
        "origin": "https://pro.coolcollege.cn",
        "priority": "u=1, i",
        "referer": "https://pro.coolcollege.cn/",
        "request-id": new_uuid,
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": "Windows",
        "accept": "application/json, text/plain, */*"
    }
    # 请求
    response = requests.post(url, data=json.dumps(data), headers=header).json()

    # 获取认证信息
    try:
        if response['code'] == '200000' and response['message'] == 'success' and response['request_id'] == new_uuid:
            return response['data']['user']['access_token'], response['data']['user']['enterprise_id'], response['data']['user']['id']
        elif response['code'] == '521024' and response['message'] == 'User not found' and response['request_id'] == new_uuid:
            print('用户不存在，检查变量“mobile_yxt”设置的账号是否正确！')
        elif response['code'] == '521013' and response['message'] == '密码错误' and response['request_id'] == new_uuid:
            print('密码错误，检查变量“password_yxt”配置的加密密码串是否正确！')
        else:
            print('认真接口返回不符合预期，查看接口返回：\n', response)
    except AttributeError:
        print('程序异常：\n', response)


if __name__ == '__main__':
    # 获取变量
    mobile_yxt = os.getenv('mobile_yxt')
    password_yxt = os.getenv('password_yxt')
    # 登录
    access_token, enterprise_id, user_id = login(mobile_yxt, password_yxt)
    # 签到
    sign(access_token, enterprise_id, user_id)

