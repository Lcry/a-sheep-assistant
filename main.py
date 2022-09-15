# -*- coding: utf-8 -*-


"""
@author : lcry
@time : 2022/9/15 12:00
"""
# 接口地址,请求头参数必填:t
map_api = "https://cat-match.easygame2021.com/sheep/v1/game/map_info?map_id=%s"
finish_api = "https://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=%s&rank_time=%s&rank_role=1&skin=1"


# 完成闯关
def finish_game(state, cost_time):
    pass


if __name__ == '__main__':
    # 第一关map_id=80001
    # 第二关map_id=90015
    print("开始闯关...")
    print(map_api % 80001)
    print(finish_api % (1, 60))
    finish_game(1, 60)
    print("闯关成功...")
