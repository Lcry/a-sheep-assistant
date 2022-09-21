import struct
import base64
import requests

while True:
    headers = {'t':'', }
    #url = 'https://cat-match.easygame2021.com/sheep/v1/game/personal_info?'
    #r = requests.get(url, headers=headers)
    #print(r.json())
    url = 'https://cat-match.easygame2021.com/sheep/v1/game/map_info_ex?matchType=3'
    r = requests.get(url, headers=headers)
    map_md5 = r.json()['data']['map_md5'][1]
    #print(map_md5)
    url = f'https://cat-match-static.easygame2021.com/maps/{map_md5}.txt'  # 由于每天获取的地图不一样，需要计算地图大小
    r = requests.get(url)
    levelData = r.json()['levelData']

    # 核心算法解密******************************************************:
    # 生成操作序列
    p = []
    for h in range(len(sum(levelData.values(), []))):
        p.append({'chessIndex': 127 if h > 127 else h, 'timeTag': 127 if h > 127 else h})
    GAME_DAILY = 3
    data = struct.pack('BB', 8, GAME_DAILY)
    # print(data)
    for i in p:
        c, t = i.values()
        data += struct.pack('BBBBBB', 34, 4, 8, c, 16, t)

    # MatchPlayInfo   base64加密
    MatchPlayInfo = base64.b64encode(data).decode('utf-8')
    #print(MatchPlayInfo)
    # *******************************************************************

    # 最后打印 {'err_code': 0, 'err_msg': '', 'data': 0}  则表示提交成功
    url = 'https://cat-match.easygame2021.com/sheep/v1/game/game_over_ex?'
    r = requests.post(url, headers=headers,json={'rank_score': 1, 'rank_state': 1, 'rank_time': 1, 'rank_role': 1, 'skin': 1,'MatchPlayInfo': MatchPlayInfo})
    print(r.json())
