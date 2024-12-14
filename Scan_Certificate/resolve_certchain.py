"""
解析TLS证书链，非常重要！！！
"""
import os
import re

from OpenSSL import crypto

from Scan_Certificate.read_android_cert import read_android_cert

def split_cert_chain(cert_data):
    re_pattern = b"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----"
    cert_list = re.findall(re_pattern, cert_data, re.DOTALL)
    return cert_list

def resolve_cert_chains(cert_data):
    bytes_list_cert = resolve(cert_data)
    list_cert = []
    for _cert in bytes_list_cert:
        # 使用OpenSSL将DER格式的证书转换为X.509对象
        cert = crypto.load_certificate(crypto.FILETYPE_ASN1, _cert)
        # 将X.509对象编码为PEM格式（CRT格式）
        pem_content = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
        list_cert.append(pem_content)
    return list_cert


if __name__ == '__main__':
    file_paths = "../Scan_result/certs/music/kgyy"
    path = os.listdir(file_paths)
    for file in path:
        if file.endswith(".crt"):
            file_path = os.path.join(file_paths, file)
            try:
                print(file_path)
                file_path = "../Scan_result/certs/music/hwyysc_1/120.220.34.237_443_11.crt"
                cert_data = read_android_cert(file_path)
                chain, list_c = resolve_cert_chains(cert_data)
                i = 0
                for cert in list_c:
                    i = i + 1
                    with open(f'{file_path}_chain_{i}.crt', 'wb') as cert_file:
                        pass
                    with open(f'{file_path}_chain_{i}.crt', 'ab') as cert_file:
                        cert_file.write(cert)
                    print(cert)
                print("===")
                for cert in list_c:
                    print(cert)
                break
            except Exception as e:
                print(f"Error decoding certificate: {e}")

