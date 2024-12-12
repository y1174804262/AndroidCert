"""
这个文件主要是用来解析证书的一些信息，比如证书的有效期，证书的公钥类型，证书的长度等等
传入的参数均为经过x509.load_cert_der(data)处理过的证书数据
"""
from datetime import datetime


def parse_key(cert):
    cert = cert.get_pubkey()
    key_index = cert.type()
    if key_index == 6:
        key_value = 'RSA'
    elif key_index == 116:
        key_value = 'DSA'
    elif key_index == 28:
        key_value = 'DH'
    elif key_index == 408:
        key_value = 'EC'
    elif key_index == -1:
        key_value = 'ECC'
    else:
        key_value = key_index
    key_length = cert.bits()
    return key_length, key_value


def parse_date(cert_data):
    start_time = cert_data.get_notBefore().decode()
    end_time = cert_data.get_notAfter().decode()
    start_time_obj = datetime.strptime(start_time, "%Y%m%d%H%M%SZ")
    end_time_obj = datetime.strptime(end_time, "%Y%m%d%H%M%SZ")
    vila_time = (end_time_obj - start_time_obj).days
    return start_time_obj, end_time_obj, vila_time


def parse_subject(cert_data):
    subject = cert_data.get_subject()
    subject_info = {
        "CN": subject.CN,
        "ST": subject.ST,
        "L": subject.L,
        "O": subject.O,
        "C": subject.C,
        "OU": subject.OU
    }
    return subject_info


def parse_issuer(cert_data):
    issuer = cert_data.get_issuer()
    issuer_info = {
        "CN": issuer.CN,
        "ST": issuer.ST,
        "L": issuer.L,
        "O": issuer.O,
        "C": issuer.C,
        "OU": issuer.OU
    }
    return issuer_info


def parse_serial_number(cert_data):
    serial_number = hex(cert_data.get_serial_number())
    return serial_number
