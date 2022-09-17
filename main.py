"""
主程序类
@author : lcry
@time : 2022/9/15 12:00
"""
import random
import sys
import time

import requests

import config

map_api = "https://cat-match.easygame2021.com/sheep/v1/game/map_info?map_id=%s"
# 完成羊群接口
finish_sheep_api = "https://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=1&rank_time=%s&rank_role=1&skin=%s"
# 完成话题接口
finish_topic_api = "https://cat-match.easygame2021.com/sheep/v1/game/topic_game_over?rank_score=1&rank_state=1&rank_time=%s&rank_role=2&skin=%s"

header_t = config.get("header_t")
header_user_agent = config.get("header_user_agent")
cost_time = config.get("cost_time")
cycle_count = config.get("cycle_count")
sheep_type = config.get("sheep_type")
topic_type = config.get("topic_type")

request_header = {
    "Host": "cat-match.easygame2021.com",
    "User-Agent": header_user_agent,
    "t": header_t,
    "Referer": "https://servicewechat.com/wx141bfb9b73c970a9/17/page-frame.html",
    "Accept-Encoding": "gzip,compress,br,deflate",
    "Connection": "close"
}

"""
调用完成闯关羊群
Parameters:
  cost_time - 耗时
"""


def finish_game_sheep(skin, rank_time):
    s = requests.session()
    s.keep_alive = False
    res = requests.get(finish_sheep_api % (rank_time, skin), headers=request_header, timeout=10, verify=True)
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
    res = requests.get(finish_topic_api % (rank_time, skin), headers=request_header, timeout=10, verify=True)
    # err_code为0则成功
    if res.json()["err_code"] == 0:
        print("\033[1;36m恭喜你! 本次闯关话题状态成功\033[0m")
    else:
        print(res.json())
        print("请检查t的值是否获取正确!")


if __name__ == '__main__':
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
        interval_time = random.randint(2, 6)
        print(f"生成随机时间间隔，防止游戏服务器接口限流导致失败 : {interval_time} s")
        if cost_time == -1:
            cost_time = random.randint(1, 3600)
            print(f"生成随机闯关完成耗时: {cost_time} s")
        try:
            if sheep_type == 1:
                finish_game_sheep(1, cost_time)
                success += 1
            time.sleep(interval_time)
            if topic_type == 1:
                finish_game_topic(1, cost_time)
                success += 1
        except Exception as e:
            print(f"游戏服务器响应超时或崩溃中未及时响应，缓缓吧，等待服务器恢复后再试！本次失败请忽略，错误日志: {e}")
        if success >= cycle_count:
            print("【羊了个羊一键闯关结束】")
            sys.exit(0)
        print(f"\033[4;32m已成功完成{success}次\033[0m")
        i += 1
