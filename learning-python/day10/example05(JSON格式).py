# JSON格式的字符串
"""
操作系统:Windows,iOS,Android,macOS,Linux,Unix
编程语言:Python,Java,PHP,Go,C++

1.两个异构的系统之间交换数据最好的选择式交换纯文本（可以屏蔽系统和编程语言的差异）
2.纯文本应该是结构化或半结构化的纯文本（有一定的格式）  
  ~ XML --> eXtensible Markup Language --> 可扩展标记语言
  ~ JSON --> JavaScript Object Notation js中的对象语法 --> 大多数网站和数据接口服务使用的数据格式
  ~ YAML --> Yet Another Markup Language
3. 如何将JSON格式转换成Python程序中的字典？
  --> json --> loads

URL --> Universal Resource Locator --> 统一资源定位符
"""

import json

data="""
{
  "code": 200,
  "message": "获取用户列表成功",
  "newList": [
    {
      "id": 1001,
      "username": "zhangsan",
      "nickname": "张三",
      "email": "zhangsan@example.com",
      "avatar": "https://api.example.com/avatars/1001.png",
      "status": "active",
      "roles": ["user", "reader"],
      "created_at": "2023-08-15T10:30:00Z"
    },
    {
      "id": 1002,
      "username": "lisi",
      "nickname": "李四",
      "email": "lisi@example.com",
      "avatar": "https://api.example.com/avatars/1002.png",
      "status": "active",
      "roles": ["user"],
      "created_at": "2023-09-20T14:22:00Z"
    },
    {
      "id": 1003,
      "username": "wangwu",
      "nickname": "王五",
      "email": "wangwu@example.com",
      "avatar": "https://api.example.com/avatars/1003.png",
      "status": "inactive",
      "roles": ["user", "reader", "editor"],
      "created_at": "2023-10-05T09:15:00Z"
    }
  ]
}
"""

news_dict=json.loads(data)
news_list=news_dict['newList']

for news in news_list:
  # print(type(news))
  # print(news)
  print(news['avatar'])
# print(news_list)