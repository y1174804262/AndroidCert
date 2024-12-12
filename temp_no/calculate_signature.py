from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


def extract_signature_value(cert_path):
    # 读取证书文件
    with open(cert_path, "rb") as cert_file:
        cert_data = cert_file.read()

    # 解析证书
    cert = x509.load_pem_x509_certificate(cert_data, default_backend())

    # 提取签名值
    signature = cert.signature
    signature_hex = signature.hex()

    # 提取签名算法
    signature_algorithm = cert.signature_algorithm_oid

    return signature_hex, signature_algorithm


# 替换为你的 CRT 证书路径
cert_path = "test/m_2.crt"

signature_value, signature_algorithm = extract_signature_value(cert_path)
print(f"Signature Value (hex): {signature_value}")
print(f"Signature Algorithm: {signature_algorithm}")
