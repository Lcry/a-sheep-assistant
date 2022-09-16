# IOS 抓包
### 安装抓包 App
#### 1. 前往 App Store 搜索"Stream" 下载安装
![](imgs/stream/16633346518135.jpg)

#### 2. 打开App
![](imgs/stream/16633347221380.jpg)
#### 配置 HTTPS 抓包
需要点击 app 首页 HTTPS 抓包 
* 需要手机安装证书
* 需要点击 清除缓存
![](imgs/stream/16633348675175.jpg)

#### 点击安装 CA 证书
![](imgs/stream/16633349246026.jpg)
#### 选取设备 
选择 iPhone 
![](imgs/stream/16633352499868.jpg)
#### 提示"已下载描述文件"成功

### 
![](imgs/stream/16633352080548.jpg)

### ios手机设置证书
#### 设置描述文件
> 通用-VPN与设备管理-设置描述文件

![](imgs/stream/16633353583141.jpg)
#### 选中刚刚下载的描述文件 "Stream Generated CA 427170DA"
![](imgs/stream/16633354006678.jpg)

#### 点击安装证书

![](imgs/stream/16633355000453.jpg)

#### 找到 "证书信任设置" 
> 通用-关于本机-证书信任设置

![](imgs/stream/16633356497868.jpg)

#### 启用完全信任证书 "Stream Generated CA 427170DA"
> 将下面 Stream Generated CA 427170DA 选项打开

![](imgs/stream/16633357410368.jpg)

![](imgs/stream/16633358297978.jpg)

### 准备抓包
#### 重新打开 Stream 
> 点击 HTTPS 抓包 显示CA设置成功 

![](imgs/stream/16633348347080.jpg)

#### 点击 清除 MITM 缓存
![](imgs/stream/16633360566918.jpg)

### 开始抓包
#### 点击开始抓包
> 点击开始抓包后, 打开微信小程序 

![](imgs/stream/16633360833422.jpg)

#### 进入游戏完成第一关
> 完成第一关后切换抓包工具

![](imgs/stream/16633361082444.jpg)

#### 查看抓包数据
> 点击抓包历史-选择最近抓包记录-按域名查询

![](imgs/stream/16633361677052.jpg)

#### 找到域名"cat-match.easygame2021.com"

![](imgs/stream/16633362396965.jpg)

#### 在详情记录找到对应 t 数据, 后续代码要用到的 t 参数拷贝下来
![](imgs/stream/16633362824354.jpg)
