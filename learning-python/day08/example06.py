# 凯撒加密
"""
明文: attack at dawn
密文: dwwdfn dw gdzq

对称加密:加密解密相同吗密钥 --> AES
非对称加密:加密和解密使用不同的密钥（公钥，私钥） --> RSA
"""

message='attack at dawn'
# 生成字符串转换的对照表
table=str.maketrans('abcdefghijklmnopqrstuvwxyz','defghijklmnopqrstuvwxyzabc')
# 通过字符串的translate方法实现字符串转译
print(message.translate(table))