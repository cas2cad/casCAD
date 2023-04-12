import os
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, load_pem_private_key, load_pem_public_key

# 生成SM2私钥
def generate_sm2_private_key():
    return ec.generate_private_key(ec.BrainpoolP256R1(), os.urandom)

# 生成Secp256k1私钥
def generate_secp256k1_private_key():
    return ec.generate_private_key(ec.SECP256K1(), os.urandom)

# 使用私钥签名消息
def sign_message(private_key, message):
    message_hash = hashlib.sha256(message.encode()).digest()
    signature = private_key.sign(message_hash, ec.ECDSA(hashes.SHA256()))
    r, s = decode_dss_signature(signature)
    return (r, s)

# 使用公钥验证签名
def verify_signature(public_key, message, signature):
    message_hash = hashlib.sha256(message.encode()).digest()
    try:
        public_key.verify(encode_dss_signature(*signature), message_hash, ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False

# 将私钥序列化为PEM格式
def serialize_private_key(private_key):
    return private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, ec.NoEncryption())

# 将公钥序列化为PEM格式
def serialize_public_key(public_key):
    return public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

# 从PEM格式反序列化私钥
def deserialize_private_key(pem_data):
    return load_pem_private_key(pem_data, None)

# 从PEM格式反序列化公钥
def deserialize_public_key(pem_data):
    return load_pem_public_key(pem_data)

# 示例
message = "This is a test message."

# SM2签名
# sm2_private_key = generate_sm2_private_key()
# sm2_public_key = sm2_private_key.public_key()
sm2_private_key = "0xea50f2f45c17c14945b5bf3d439b2d29f7e8a46cfa2bd4e9c875aaff1ef8fc1d"
sm2_public_key = "0x3c27cb638044c8bdf9147ab983c0f3ab810be2791b6eb80ae8a3ee40340bdb7c69a98307e7cfcd324bb7f82e4bba20782d16d7e2fb6205005586fe69e739f439"
sm2_signature = sign_message(sm2_private_key, message)
print("SM2 Signature:", sm2_signature)
print("SM2 Signature is valid?", verify_signature(sm2_public_key, message, sm2_signature))

# Secp256k1签名
secp256k1_private_key = generate_secp256k1_private_key()
secp256k1_public_key = secp256k1_private_key.public_key()
secp256k1_signature = sign_message(secp256k1_private_key, message)
print("Secp256k1 Signature:", secp256k1_signature)
print
