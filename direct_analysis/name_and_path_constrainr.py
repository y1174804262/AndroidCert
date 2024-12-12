import os

from cryptography import x509
from cryptography.hazmat.backends import default_backend


def analysis(path):
    # 读取证书文件
    with open(path, 'rb') as cert_file:
        cert_data = cert_file.read()

    # 加载证书
    cert = x509.load_pem_x509_certificate(cert_data, default_backend())
    try:
        # 获取基本约束
        basic_constraints = cert.extensions.get_extension_for_class(x509.BasicConstraints).value
        print(f"CA: {basic_constraints.ca}")
        print(f"Path length constraint: {basic_constraints.path_length}")

        # 获取名称约束

        name_constraints = cert.extensions.get_extension_for_class(x509.NameConstraints).value
        if name_constraints.permitted_subtrees:
            for subtree in name_constraints.permitted_subtrees:
                print(f"Permitted subtree: {subtree}")
        if name_constraints.excluded_subtrees:
            for subtree in name_constraints.excluded_subtrees:
                print(f"Excluded subtree: {subtree}")
    except Exception as e:
        if "ExtensionNotFound" in str(e):
            print(f"Extension not found: {path}")


if __name__ == '__main__':
    file_path_1 = "../Scan_result/collect_root_cert"
    for file_path_2 in os.listdir(file_path_1):
        file_path_3 = os.path.join(file_path_1, file_path_2)
        analysis(file_path_3)
