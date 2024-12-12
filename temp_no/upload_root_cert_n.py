import os

from Scan_Certificate.read_android_cert import read_android_cert, parse_certificate
from neo4j.get_cert_data import cert_data_parse


def upload_root_cert():
    """
    上传根证书
    :return:
    """
    file_paths = "../Scan_result/root_cert"
    path = os.listdir(file_paths)
    for file in path:
        if file.endswith(".crt"):
            file_path = os.path.join(file_paths, file)
            # file_path = "../Scan_result/certs/183.204.78.148_443.crt"
            cert_data_bytes = read_android_cert(file_path)
            x509 = parse_certificate(cert_data_bytes)
            cert_data_parse(x509, '根证书', file)
            print("上传完成")


if __name__ == '__main__':
    upload_root_cert()
