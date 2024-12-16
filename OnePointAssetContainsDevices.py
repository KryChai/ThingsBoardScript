import requests
import json

'''
批量设置资产到设备关联的脚本：
只需修改下面几个参数即可一键运行
其中要分配的设备列表DEVICE_IDS，如果当初是批量导入的，那么他们的设备id都是连续的，可以写个循环批量生成的解决问题
AUTH_TOKEN参数即租户管理员的AWT格式的TOKEN，登录到Thingsboard的Web界面，进入右上角“账号” -> “安全”部分直接复制AWT格式的令牌即可。
注意此TOKEN每隔一段时间就会自己改变，每次使用此脚本前需要更新

需要设置的参数列表：
THINGBOARD_URL
AUTH_TOKEN
DEVICE_BEGIN_ID
NUM

由于官网上给出的Python REST API示例脚本中，直接调用tb_rest_client.rest库中的json格式存在问题，官方说是3.4版本以上的都可以使用，
但是我3.8.1版本的json格式和官方的不一致，此脚本主要是根据3.8.1后端的json格式，修改了post到后端的json格式，经测试运行稳定
'''

THINGBOARD_URL = "http://localhost:8080"

AUTH_TOKEN = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZW5hbnRAdGhpbmdzYm9hcmQub3JnIiwidXNlcklkIjoiZjQyN2I2MDAtYTMwMi0xMWVmLTg5ZTAtZjEzNDJmYTJjN2QyIiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJzZXNzaW9uSWQiOiJiNmRkMmFmNi0xNjc3LTQ4MjctYjQ0OS03MTg2MjY5MDA0MWUiLCJleHAiOjE3MzQyMzU0MDMsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNzM0MjI2NDAzLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiYTAyMThjNzAtYTMwMi0xMWVmLTg5ZTAtZjEzNDJmYTJjN2QyIiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCJ9.qk2blpeIUGZ5abNbFYZRIni5o0sC12fGqGJWPykS8T0l1HeV1vEA3oxQe9qHxUpL_OKh_LqZGj_OSHBS-tEbgw"

# 资产的ID
ASSET_ID = "0daf0130-ba8e-11ef-8560-8522badd8322"

# 开始的设备
DEVICE_BEGIN_ID = "f199dae0-ba8a-11ef-8560-8522badd8322"

# NUM 设置为你需要分配的设备数量减一
NUM = 3

# ------------------------------------------------------在上面设置参数，下面别动----------------------------------------------------------------------

DEVICE_IDS = [DEVICE_BEGIN_ID]

url = f"{THINGBOARD_URL}/api/relation"

headers = {
    "Content-Type": "application/json",
    "X-Authorization": AUTH_TOKEN
}

#批量生成ID
head = DEVICE_BEGIN_ID.split("-")[0]
tail = DEVICE_BEGIN_ID[8:]
Hex_head = [int(c, 16) for c in head]# 将字符串中的每个字符直接转换为十六进制数值
sum=0
c=0
for i in reversed(Hex_head):
    sum=sum+i*pow(16,c)
    c+=1

#批量生成ID
for i in range(NUM):
    sum+=1
    hex_string = hex(sum)[2:]
    DEVICE_IDS.append(hex_string+tail)

for i in range(NUM+1):
    data = {
        "from": {
            "entityType": "DEVICE",
            "id": DEVICE_IDS[i]
        },
        "to": {
            "entityType": "ASSET",
            "id": ASSET_ID
        },
        "type": "Contains",
        "typeGroup": "COMMON"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("关系创建成功")
    else:
        print("关系创建失败，状态码：", response.status_code)

