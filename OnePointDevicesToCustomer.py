import requests

'''
批量分配设备给客户的脚本：
只需修改下面几个参数即可一键运行
其中要分配的设备列表DEVICE_IDS，如果当初是批量导入的，那么他们的设备id都是连续的，可以写个循环批量生成的解决问题
AUTH_TOKEN参数即租户管理员的AWT格式的TOKEN，登录到Thingsboard的Web界面，进入右上角“账号” -> “安全”部分直接复制AWT格式的令牌即可。

需要设置的参数列表：
THINGBOARD_URL
AUTH_TOKEN
ASSET_BEGIN_ID
NUM
CUSTOMER_ID
'''

# Thingsboard REST API URL
THINGBOARD_URL = "http://localhost:8080/api/"

# Authorization token
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZW5hbnRAdGhpbmdzYm9hcmQub3JnIiwidXNlcklkIjoiZjQyN2I2MDAtYTMwMi0xMWVmLTg5ZTAtZjEzNDJmYTJjN2QyIiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJzZXNzaW9uSWQiOiIxMzljMzAxMC05NjVkLTRiOWEtOTBjYS0wYWEyOTMyM2VkM2MiLCJleHAiOjE3MzQxODU1NzEsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNzM0MTc2NTcxLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiYTAyMThjNzAtYTMwMi0xMWVmLTg5ZTAtZjEzNDJmYTJjN2QyIiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCJ9.s16CFEvzqeIN_MPlwkngBU2QLyB_cBu-a7lu3saVhVTLHGwrjqVe9uO-uUsK_XwKfg40tBxJq1x0rEPC_cwfJw"

'''
首先，我们观察批量导入的设备的ID规律，我们发现这一批设备的id都是6ffef3b_-b79e-11ef-8560-8522badd8322
只有_这个位置的数字不同，然后我们可以观察大量导入设备，我们会发现，他执行的是十六进制，
因此，我们可以得出下面的生成方法。
'''
# 刚才批量导入的第一个Device的ID
DEVICE_BEGIN_ID = "6ffef3b0-b79e-11ef-8560-8522badd8322"
# 要分配的设备ID列表
DEVICE_IDS = [DEVICE_BEGIN_ID]

# 批量导入的设备数量-1
NUM = 3

# 客户ID
CUSTOMER_ID = "2ca41db0-b5f6-11ef-8560-8522badd8322"


# ------------------------------------------------------在上面设置参数，下面别动----------------------------------------------------------------------

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

# 设置HTTP头部
headers = {
    "Content-Type": "application/json",
    "X-Authorization": AUTH_TOKEN
}

# 批量分配设备的函数
def assign_devices_to_customer(device_ids, customer_id):
    for device_id in device_ids:
        # 构建分配设备的URL
        assign_url = THINGBOARD_URL + "customer/" + customer_id + "/device/" + device_id
        print(assign_url)

        # 发送分配设备的请求
        response = requests.post(assign_url, headers=headers)
        print(response)

        # 检查响应状态
        if response.status_code == 200:
            print(f"Device {device_id} has been assigned to Customer {customer_id}.")
        else:
            print(f"Failed to assign Device {device_id} to Customer {customer_id}. Status code: {response.status_code}, Response: {response.text}")

# 调用函数执行分配操作
assign_devices_to_customer(DEVICE_IDS, CUSTOMER_ID)
