"""
主程序类
@author : lcry
@time : 2022/9/15 12:00
"""
import base64
import random
import sys
import time

import requests
import urllib3

import config

map_api = "https://cat-match.easygame2021.com/sheep/v1/game/map_info?map_id=%s"
# 完成羊群接口
finish_sheep_api = "https://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=1&rank_time=%s&rank_role=1&skin=%s&t=%s"
# 完成话题接口
finish_topic_api = "https://cat-match.easygame2021.com/sheep/v1/game/topic_game_over?rank_score=1&rank_state=1&rank_time=%s&rank_role=2&skin=%s&t=%s"
# 获取用户信息接口
get_user_info_api = "https://cat-match.easygame2021.com/sheep/v1/game/user_info?uid=%s&t=%s"
# 用户登录接口，POST请求 需要wx_open_id
user_login_api = "https://cat-match.easygame2021.com/sheep/v1/user/login_tourist"

header_t = config.get("header_t")
header_user_agent = config.get("header_user_agent")
cost_time = config.get("cost_time")
cycle_count = config.get("cycle_count")
sheep_type = config.get("sheep_type")
topic_type = config.get("topic_type")
target_uid = config.get("target_uid")
# 用于请求oppenid以及token的t，感谢@lyzcren 老哥 ，简单加密处理
sacrifice_t_encryption = "ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmxlSEFpT2pFMk9UUTFNelF4TXpjc0ltNWlaaUk2TVRZMk16UXpNVGt6Tnl3aWFXRjBJam94TmpZek5ETXdNVE0zTENKcWRHa2lPaUpEVFRwallYUmZiV0YwWTJnNmJIUXhNak0wTlRZaUxDSnZjR1Z1WDJsa0lqb2lJaXdpZFdsa0lqb3hNelU1TmprMU1pd2laR1ZpZFdjaU9pSWlMQ0pzWVc1bklqb2lJbjAucnhOcDY5Q3lfVW1ZWnQxdXpzR2tJS0ZCT1plaFczdlh6bzNrbHRKdHliWQ=="
sacrifice_t = base64.b64decode(sacrifice_t_encryption.encode("utf-8")).decode("utf-8")

urllib3.disable_warnings()
request_header = {
    "Host": "cat-match.easygame2021.com",
    "User-Agent": header_user_agent,
    "t": header_t,
    "Referer": "https://servicewechat.com/wx141bfb9b73c970a9/17/page-frame.html",
    "Accept-Encoding": "gzip,compress,br,deflate",
    "Connection": "close"
}
"""
uid转token，实现逻辑就是先用一个正常帐号去获取wx_open_id，然后再去调生成token策略
Parameters:
  uid - 目标用户uid
  legitimate_token - 合法权限token
"""


def uid2token(uid, legitimate_token):
    uuid = None
    user_token = None
    try_get_user_info_api_count = 1
    try_user_login_api = 1
    max_try_count = 5
    while True:
        print(f"开始尝试第{try_get_user_info_api_count}次换取用户uuid")
        wait_for_random_interval(False)
        try:
            get_res = requests.get(get_user_info_api % (uid, legitimate_token), headers=request_header, timeout=15,
                                   verify=False)
            uuid = get_res.json()["data"]["wx_open_id"]
            login_body = {
                "uuid": str(uuid)
            }
        except Exception:
            try_get_user_info_api_count += 1
        finally:
            # 最大尝试次数，可能是个瞎搞的uid不可能一直访问
            if try_get_user_info_api_count > max_try_count:
                print(f"超过target_uid模式最大尝试次数，本次程序运行结束，请稍后重试或者检查uid是否正确！")
                sys.exit(0)
        if uuid:
            print(f"第{try_get_user_info_api_count}次尝试换取用户uuid成功")
            break

    while True:
        print(f"开始尝试第{try_user_login_api}次换取用户header_t")
        wait_for_random_interval(False)
        try:
            login_res = requests.post(user_login_api, headers=request_header, json=login_body, timeout=15, verify=False)
            # 响应模型
            # {
            #    "data" : {
            #       "openid" : "123",
            #       "token" : "eyxxxx",
            #       "uid" : 111
            #    },
            #    "err_code" : 0,
            #    "err_msg" : ""
            # }
            user_token = login_res.json()["data"]["token"]
            print("获取token成功:", user_token)
            global header_t
            header_t = user_token
        except Exception:
            try_user_login_api += 1
        finally:
            if try_user_login_api > max_try_count:
                print(f"超过target_uid模式最大尝试次数，本次程序运行结束，请稍后重试或者检查uid是否正确！")
                sys.exit(0)
        if user_token:
            print(f"第{try_user_login_api}次尝试换取用户header_t成功")
            break
    return user_token


"""
调用完成闯关羊群
Parameters:
  cost_time - 耗时
"""


def finish_game_sheep(skin, rank_time):
    s = requests.session()
    s.keep_alive = False
    res = requests.get(finish_sheep_api % (rank_time, skin, header_t), headers=request_header, timeout=10, verify=False)
    # err_code为0则成功
    if res.json()["err_code"] == 0:
        print("\033[1;36m恭喜你! 本次闯关羊群状态成功\033[0m")
    else:
        print(res.json())
        print("请检查t的值是否获取正确!")


"""
调用完成闯关话题
Parameters:
  cost_time - 耗时
"""


def finish_game_topic(skin, rank_time):
    s = requests.session()
    s.keep_alive = False
    res = requests.get(finish_topic_api % (rank_time, skin, header_t), headers=request_header, timeout=10, verify=False)
    # err_code为0则成功
    if res.json()["err_code"] == 0:
        print("\033[1;36m恭喜你! 本次闯关话题状态成功\033[0m")
    else:
        print(res.json())
        print("请检查t的值是否获取正确!")


"""
等待随机时间
Parameters:
    - is_show ： 是否显示提示
"""


def wait_for_random_interval(is_show):
    interval_time = random.randint(2, 6)
    if is_show:
        print(f"等待随机时间间隔，防止游戏服务器接口限流导致失败 : {interval_time} s")
    time.sleep(interval_time)


if __name__ == '__main__':
    if header_t == "":
        print("> 你所选择的是使用target_uid模式")
        header_t = uid2token(target_uid, sacrifice_t)
    else:
        print("> 你所选择的是直接使用header_t模式")
    print("【羊了个羊一键闯关启动】")
    # 前置判断，程序员何必为难程序员呢，针对恶意刷次数对服务器造成压力的进行拦截
    if cycle_count > 10:
        print("程序员何必为难程序员,请勿恶意刷次数对服务器造成压力，请设定cycle_count的值小于10以下的值，本次程序运行结束")
        print("【羊了个羊一键闯关开始结束】")
        sys.exit(0)

    i = 1
    success = 0
    while True:
        print(f"...第{i}次尝试完成闯关...")
        if cost_time == -1:
            cost_time = random.randint(1, 3600)
            print(f"生成随机闯关完成耗时: {cost_time} s")
        try:
            if sheep_type == 1:
                wait_for_random_interval(True)
                finish_game_sheep(1, cost_time)
                success += 1
            if topic_type == 1:
                wait_for_random_interval(True)
                finish_game_topic(1, cost_time)
                success += 1
        except Exception as e:
            print(f"游戏服务器响应超时或崩溃中未及时响应，缓缓吧，等待服务器恢复后再试！本次失败请忽略，错误日志: {e}")
        if success >= cycle_count:
            print("【羊了个羊一键闯关结束】")
            sys.exit(0)
        print(f"\033[4;32m已成功完成{success}次\033[0m")
        i += 1
