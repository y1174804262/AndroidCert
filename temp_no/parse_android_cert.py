"""
读取Android证书链，并解析读取到的证书，提取基本内容
"""
from OpenSSL import crypto
from Scan_Certificate.read_android_cert import read_android_cert
from Scan_Certificate.resolve_certchain import resolve_cert_chains


def get_tls_certificate_chain(file_name):
    """
    获取TLS证书链,从cert_chain_resolver中提取
    :param file_name: 证书链文件名
    :return:  证书链
    """
    with open(file_name, 'rb') as f:
        cert_data = f.read()
    cert_chain = resolve_cert_chains(cert_data)
    return cert_chain


def parse_certificate(pem_cert):
    """
    解析证书
    :param pem_cert:  PEM格式证书
    :return:  证书信息
    """
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, pem_cert)
    # 下面两行代码可以提取TLS证书
    key = cert.get_pubkey()
    # x509 = crypto.load_certificate(crypto.FILETYPE_PEM, pem_cert)
    # return x509
    version = cert.get_version()  # 证书版本

    subject = cert.get_subject()
    CN = subject.CN
    ST = subject.ST
    L = subject.L
    O = subject.O
    C = subject.C
    OU = subject.OU
    issuer = cert.get_issuer()
    issuer_CN = issuer.CN
    issuer_ST = issuer.ST
    issuer_L = issuer.L
    issuer_O = issuer.O
    issuer_C = issuer.C
    issuer_OU = issuer.OU
    serial_number = hex(cert.get_serial_number())
    not_before = cert.get_notBefore().decode('ascii')
    not_after = cert.get_notAfter().decode('ascii')
    signature_algorithm = cert.get_signature_algorithm().decode('utf-8')  # 证书签名算法
    cert.sign(key, signature_algorithm)
    print("a")

    certificate_info = {
        "主体": subject,  # 证书持有者的特定名称
        "版本号": version,  # 证书版本
        "公用名(CN)": CN,  # 证书持有者的公用名
        "国家(C)": C,  # 证书持有者的国家
        "省/州(ST)": ST,  # 证书持有者的省/州
        "城市(L)": L,  # 证书持有者的城市
        "组织(O)": O,  # 证书持有者的组织
        "组织单位(OU)": OU,  # 证书持有者的组织
        "CA": issuer,  # 证书发行机构的特定名称
        "CA公用名(CN)": issuer_CN,  # 证书发行机构的公用名
        "CA国家(C)": issuer_C,  # 证书发行机构的国家
        "CA省/州(ST)": issuer_ST,  # 证书发行机构的省/州
        "CA城市(L)": issuer_L,  # 证书发行机构的城市
        "CA组织(O)": issuer_O,  # 证书发行机构的组织
        "CA组织单位(OU)": issuer_OU,  # 证书发行机构的组织
        "序列号": serial_number,  # 证书的序列号
        "起始有效日期": not_before,  # 起始有效日期
        "终止无效日期": not_after  # 终止无效日期
    }

    return certificate_info


def main():
    file_path = "../Scan_result/certs/test/appmarket_8/39.136.186.41_443_13.crt"
    cert_bytes = read_android_cert(file_path)
    cert_info = parse_certificate(cert_bytes)
    # if cert_info['公用名(CN)'] is None:
    #     print(file_path)
    if cert_info['组织单位(OU)'] == "0002 48146308100036":
        print(file_path)
    print(cert_info['组织单位(OU)'])




if __name__ == '__main__':
    main()
