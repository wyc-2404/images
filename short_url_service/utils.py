import string
import random
from hashids import Hashids

# 62进制字符集: 0-9, a-z, A-Z
CHARSET = string.ascii_letters + string.digits

def generate_short_code(length=6):
    """
    生成随机短码
    :param length: 短码长度，默认6位
    :return: 随机字符串
    """
    return ''.join(random.choices(CHARSET, k=length))

def encode_id_to_short_code(id, salt='short_url_salt'):
    """
    将ID转换为短码（使用Hashids）
    :param id: 数据库ID
    :param salt: 加密盐值
    :return: 短码
    """
    hashids = Hashids(salt=salt, min_length=6)
    return hashids.encode(id)

def decode_short_code_to_id(short_code, salt='short_url_salt'):
    """
    将短码解码为ID
    :param short_code: 短码
    :param salt: 加密盐值
    :return: ID
    """
    hashids = Hashids(salt=salt, min_length=6)
    decoded = hashids.decode(short_code)
    return decoded[0] if decoded else None
