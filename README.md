# AlgorithmPlatform
优亿智能算法平台，包括了各类常用的算法模块，比如图像识别、本文分类、推荐系统等，为各类常用的场景提供算法模型。
# api接口说明
接口地址 |http://192.168.0.16:32776/api
---|---
请求方式 | HTTP POST

POST 二进制图片文件，图片格式为png', 'jpg', 'jped最大16m

POST 格式为

```
{
    "file": "<censored...binary...data>"
  }
```


返回是json格式，包含以下字段

图片文字描述 |loss值
---|---



响应

```
[
    ['a cat is sitting on a bed with a stuffed animal .', 2.983238269870574e-06],
    ['a cat is sitting on a couch with a stuffed animal .', 2.31435927877478e-06],
    ['a cat is sitting on a chair with a stuffed animal .', 2.213130359373113e-06]

 ]
```
示例代码（python）

```
import requests
url='http://192.168.0.16:32776/api'
files={'file':open('/home/kenwood/图片/mao.jpg','rb')}#上传图片
r=requests.post(url,files=files)
print (r.json())
```


