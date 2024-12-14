"""
获取证书链，这个模块暂时保留，但是没有用到，因为AIA中可能没有包含证书颁发者的路径，所以先留着后续再考虑如何提取证书链
"""
from OpenSSL import crypto
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import requests


# 提取TLS证书父证书的下载url
def get_issuer_certificate_url(cert):
    aia = cert.extensions.get_extension_for_oid(x509.oid.ExtensionOID.AUTHORITY_INFORMATION_ACCESS)
    for access in aia.value:
        if access.access_method == x509.AuthorityInformationAccessOID.CA_ISSUERS:
            return access.access_location.value


# 下载父证书
def download_certificate(issuer_url):
    response = requests.get(issuer_url)
    return response.content


def get_father_cert(cert, cert_chains):
    cert_chains.append(cert)  # 将该证书添加到证书链
    cert = x509.load_pem_x509_certificate(cert, default_backend())  # 加载证书
    issuer_url = get_issuer_certificate_url(cert)  # 获取父证书的下载url
    issuer_pem = download_certificate(issuer_url)  # 下载父证书
    cert = crypto.load_certificate(crypto.FILETYPE_ASN1, issuer_pem)  # 加载父证书
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)  # 转换为PEM格式
    issuer_cert = x509.load_pem_x509_certificate(cert, default_backend())  # 加载父证书

    # 进行判断，判断该证书是否是根证书，可判断该证书的issuer是否等于subject<判断自签名证书用同样的办法>
    if issuer_cert.issuer == issuer_cert.subject:
        return cert_chains

    cert_chains = get_father_cert(cert, cert_chains)  # 递归调用，获取父证书的父证书
    return cert_chains


# 示例使用
with open('../Scan_result/certs/test/chongchong_6/test.crt', 'rb') as f:
    terminal_cert_pem = f.read()
cert_chains = []
cert_chains = get_father_cert(terminal_cert_pem, cert_chains)
print(cert_chains)
