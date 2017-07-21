# 36氪新闻爬虫

## 简介

- 36氪新闻爬虫
- 主要功能为  爬取各分类标签下的文章
- 基于Scrapy框架
- 采用MongoDB数据库储存


## 运行
需要安装
- `Scrapy`
  - pip
  - lxml
  - pywin32
  - Zope.Interface
  - Twisted
  - pyOpenSSL
- MongoDB（最下面有Win的教程）
- 数据库可视化工具（可选。推荐`Studio 3T`）
- Python `pymongo`库

cmd或编译器下直接执行`main.py`文件即可。


## 目录结构

- spiders
  - `a36kr` 爬虫主要文件


- `items` 数据结构化容器

- `piplines` 管道（用于处理数据）

- `middlewares` 爬虫中间构件（未编辑）

- `settings` 爬虫配置文件


## 爬取思路

### 内容部分
36氪网站主体部分的DOM采用JavaScript生成，并且新闻列表、文章内容等均采用JSON格式通信保存，因此无法使用Scrapy提供的`Selector`选择器。

故对JSON数据：
1. 使用正则表达式来匹配JSON的内容
2. 去除JSON数据中多余的HTML标签
3. 然后使用`json`库将其格式化

### 翻页部分

通过观察Network可以发现 http://36kr.com/api/tag/yiliaojiankang?page=2&ts=1500286828&per_page=20&_=1500286832385 为api接口地址。其中`ts`与`_`每次刷新都不一样。

四个参数中一眼可以看出其中两个甚至是三个的作用。测试得知`ts`参数不得删除，否则无法翻页。

`ts` 简单想一下觉得可能是时间戳，使用[时间戳转换工具](http://tool.chinaz.com/tools/unixtime.aspx)验证后即可确定。

`_` 参数通过观察，前几位与时间戳一样，后几位不同，而且比时间戳多了几位。时间戳后几位为秒数位，多的位猜测为毫秒精度，初步猜测`_`参数为与第一次访问的时间间隔。
将与时间戳不同的部分通过[时间戳转换工具](http://tool.chinaz.com/tools/unixtime.aspx)直接转化（秒级）得到`1970/1/1 16:59:45`短暂时间后变为`1970/1/2 15:13:5`，时间跨度过大。调整为毫秒级后年月固定在`1970/1/1`，时间部分与现在时间一致，得出结论：`_`为此刻时间的时间戳。

地址中四个参数：
- `page` —— \*页码
- `ts` —— \*首次访问页面的时间戳（秒级）
- `per_page` —— \*列表中新闻个数
- `_` —— 现在时刻的时间戳（毫秒级）

经测试，其中带`*`的为必须参数，若缺少`ts`参数则无法翻页。


## 数据库

> [完整教程传送门](http://www.jianshu.com/p/9e5bc16c48c3)

### Windows下MongoDB安装

手动创建文件夹
`C:\Program Files\MongoDB\data\db`
`C:\Program Files\MongoDB\log`
分别用来安装db和日志文件，在log文件夹下创建一个日志文件MongoDB.log，即
`C:\Program Files\MongoDB\log\MongoDB.log`
```cmd
cd C:\Program Files\MongoDB\Server\3.4\bin
```
```cmd
mongod -dbpath "C:\Program Files\MongoDB\data\db"
```

测试：新开一个cmd窗口，进入MongoDB的bin目录，输入`mongo`或者`mongo.exe`

最后，为了以后方便快速启动，将MongoDB添加到Windows的`服务`中：
添加服务
```cmd
mongod --dbpath "C:\Program Files\MongoDB\data\db" --logpath "C:\Program Files\MongoDB\log\MongoDB.log" --install --serviceName "MongoDB"
```

启动服务
```cmd
C:\Program Files\MongoDB\Server\3.4\bin>net start MongoDB
```

停止服务
```cmd
C:\Program Files\MongoDB\Server\3.4\bin>net stop MongoDB
```

删除服务
```cmd
mongod --dbpath "C:\Program Files\MongoDB\data\db" --logpath "C:\Program Files\MongoDB\log\MongoDB.log" --remove --serviceName "MongoDB"
```


## 声明
*本爬虫为个人学习使用。若有不当，请指教，会立刻删除*
