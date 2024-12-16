import logging
from tb_rest_client.rest_client_pe import *
from tb_rest_client.rest import ApiException

# 配置日志记录
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# ThingsBoard REST API URL
url = "http://localhost:8080"

# 默认租户管理员凭据
username = "tenant@thingsboard.org"
password = "tenant"

FATHER_ASSET_ID = ""

ASSET_BEGIN_ID = ""

ASSET_IDS = [ASSET_BEGIN_ID]

NUM = 3

# ------------------------------------------------------在上面设置参数，下面别动----------------------------------------------------------------------

#批量生成ID
head = ASSET_BEGIN_ID.split("-")[0]
tail = ASSET_BEGIN_ID[8:]
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
    ASSET_IDS.append(hex_string+tail)

# 使用上下文管理器创建REST客户端对象以自动刷新令牌
with RestClientPE(base_url=url) as rest_client:
    try:
        # 使用凭据进行认证
        rest_client.login(username=username, password=password)

        # 获取默认资产配置文件ID
        default_asset_profile_id = rest_client.get_default_asset_profile_info().id

        for ASSET_ID in ASSET_IDS:
            # 创建资产到资产的关系
            # 假设我们想要创建一个"ManagedBy"类型的关系，其中asset1由asset2管理
            relation = EntityRelation(_from=FATHER_ASSET_ID, to=ASSET_ID, type="Contains")
            rest_client.save_relation(relation)

            logging.info(f"资产{FATHER_ASSET_ID}到资产{ASSET_ID}的关系已创建：\n%r\n", relation)
    except ApiException as e:
        # 记录异常信息
        logging.exception(e)


