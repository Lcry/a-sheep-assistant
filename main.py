"""
主程序类
@author : lcry
@time : 2022/9/15 12:00
"""
import random
import sys

import requests

import config

map_api = "https://cat-match.easygame2021.com/sheep/v1/game/map_info?map_id=%s"
# 完成游戏接口 需要参数状态以及耗时（单位秒）
finish_api = "https://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=%s&rank_time=%s&rank_role=1&skin=1"

header_t = config.get("header_t")
header_user_agent = config.get("header_user_agent")
cost_time = config.get("cost_time")
cycle_count = config.get("cycle_count")

request_header = {
    "Host": "cat-match.easygame2021.com",
    "User-Agent": header_user_agent,
    "t": header_t
}

"""
调用完成闯关
Parameters:
  state - 状态
  cost_time - 耗时
"""


def finish_game(state, rank_time):
    res = requests.get(finish_api % (state, rank_time), headers=request_header, timeout=6)
    # err_code为0则成功
    if res.json()["err_code"] == 0:
        print("状态成功")
    else:
        print(res.json())
        print("请检查t的值是否获取正确!")


if __name__ == '__main__':
    print("【羊了个羊一键闯关开始启动】")
    # 前置判断，程序员何必为难程序员呢，针对恶意刷次数对服务器造成压力的进行拦截
    if cycle_count > 10:
        print("程序员何必为难程序员,请勿恶意刷次数对服务器造成压力，请设定cycle_count的值小于10以下的值，本次程序运行结束")
        print("【羊了个羊一键闯关开始结束】")
        sys.exit(0)

    for i in range(cycle_count):
        print(f"...第{i + 1}次开始完成闯关...")
        if cost_time == -1:
            cost_time = random.randint(1, 3600)
            print(f"生成随机完成耗时:{cost_time} s")
        try:
            finish_game(1, cost_time)
        except Exception as e:
            print(f"游戏服务器响应超时或崩溃中未及时响应，缓缓吧，等待服务器恢复后再试！本次程序运行结束，错误日志: {e}")
            print("【羊了个羊一键闯关开始结束】")
            sys.exit(0)
        print(f"...第{i + 1}次完成闯关...")
    print("【羊了个羊一键闯关开始结束】")
