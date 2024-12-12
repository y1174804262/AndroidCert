from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def load_certificate(file_path):
    with open(file_path, "rb") as f:
        cert_data = f.read()
    return x509.load_pem_x509_certificate(cert_data, default_backend())


def verify_certificate_chain(cert, intermediate_certs, root_cert):
    try:
        # 验证证书的颁发者是否是根证书或任一中间证书
        for issuer_cert in intermediate_certs + [root_cert]:
            if cert.issuer == issuer_cert.subject:
                # 检查签名
                issuer_cert.public_key().verify(
                    cert.signature,
                    cert.tbs_certificate_bytes,
                    padding.PKCS1v15(),
                    cert.signature_hash_algorithm
                )
                print(f"验证成功: {cert.subject} 由 {issuer_cert.subject} 颁发")
                return True
        print("证书验证失败。")
        return False
    except Exception as e:
        print(f"验证过程中出错: {e}")
        return False


# 加载证书
leaf_cert = load_certificate("test/n_3.crt")
intermediate_cert = load_certificate("test/n_3.crt")
root_cert = load_certificate("test/n_2.crt")

# 验证叶子证书是否由中间证书和根证书颁发
if verify_certificate_chain(leaf_cert, [intermediate_cert], root_cert):
    print("叶子证书有效。")
else:
    print("叶子证书无效。")
