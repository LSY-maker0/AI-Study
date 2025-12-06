"""
联网获取JSON格式的数据并解析出需要的内容

修改三方库的下载来源为国内的镜像网站 --> pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

下载三方库 --> pip3 install requests

协议 --> 通信双方需要遵守的会话的规则

HTTP/HTTPS --> 通过URL访问网络资源的协议 --> 超文本传输协议

请求(request) - 响应(response)
"""

import json
import requests

# requests.get('http://api.tianapi.com/guonei/index?key=e8c5524dd2a365f20908ced735f8e480&num=20')

# requests.get(
#   url='http://api.tianapi.com/guonei/index',
#   params={'key':'e8c5524dd2a365f20908ced735f8e480','num':20}
# )

res=requests.post(
  url='http://121.43.111.133:3000/project/getTopLevelModules',
  params={'projectId':1},
  headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJsaWFvc3kiLCJpYXQiOjE3NjQ5NTU1MDUsImV4cCI6MTc2NTA0MTkwNX0.VrGJYqBAhjNm9ff79qzcwo_0Gce___ByF-9BLXqSL9A','Content-Type': 'application/json',}
)

# print(res.text)

# news_dict=json.loads(res.text)
news_dict=res.json()

news_list=news_dict['data']
print(news_list)