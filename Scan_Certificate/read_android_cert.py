"""
读取Android证书，并解析读取到的证书，提取基本内容
"""
from OpenSSL import crypto


def read_android_cert(file_name):
    """
    从文件中读取证书
    :param file_name: 证书链文件名
    :return:  证书链
    """
    with open(file_name, 'rb') as f:
        cert_data = f.read()
    return cert_data


def parse_certificate(pem_cert):
    """
    解析证书
    :param pem_cert:  PEM格式证书
    :return:  证书信息
    """
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, pem_cert)
    return cert


def main():
    file = "../Scan_result/certs/music/hwyysc/117.78.10.204_443_14.crt"
    cert_data = read_android_cert(file)
    cert_info = parse_certificate(cert_data)
    print(cert_info)


if __name__ == '__main__':
    main()
