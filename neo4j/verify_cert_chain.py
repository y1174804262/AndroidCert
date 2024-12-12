import subprocess

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, ec
from cryptography.hazmat.backends import default_backend
import base64
from Scan_Certificate.read_android_cert import read_android_cert
from Scan_Certificate.resolve_certchain import split_cert_chain



# from log_config import create_log

# log_driver = create_log()
def load_certificate(cert_pem):
    return x509.load_pem_x509_certificate(cert_pem, default_backend())


def verify_certificate_issuer(child_cert, parent_cert, child_cert_pem, parent_cert_pem):
    # 检查子证书的Issuer和父证书的Subject是否匹配
    if child_cert.issuer != parent_cert.subject:
        print("Issuer and Subject do not match.")
        return False
    # 验证子证书的签名
    try:
        temp_flag = parent_cert.public_key_algorithm_oid
        if "rsa" in str(temp_flag).lower():
            parent_cert.public_key().verify(
                child_cert.signature,
                child_cert.tbs_certificate_bytes,
                padding.PKCS1v15(),
                child_cert.signature_hash_algorithm,
            )
            return True
        elif "ec" in str(temp_flag).lower():
            parent_cert.public_key().verify(
                child_cert.signature,
                child_cert.tbs_certificate_bytes,
                ec.ECDSA(child_cert.signature_hash_algorithm)
            )
            return True
    except Exception as e:
        print(f"Verification failed: {e}")
        if "Curve 1.2.156.10197.1.301 is not supported" in str(e):
            try:
                with open("temp/child.txt", "wb") as f:
                    f.write(child_cert_pem)
                with open("temp/father.txt", "wb") as f:
                    f.write(parent_cert_pem)
                son_file_path = "E://PythonProject//All_Android_Certificate_2//neo4j//temp//child.txt"
                father_file_path = "E://PythonProject//All_Android_Certificate_2//neo4j//temp//father.txt"
                result = subprocess.run(['gmssl', 'certverify', '-in', son_file_path, '-cacert', father_file_path],
                                        capture_output=True, text=True, shell=True, encoding='utf-8')
                print(result.stdout)
                if "Verification success" in result.stdout:
                    return True
                else:
                    return False
            except Exception as e:
                print(f"Verification failed: {e}")
                return False
        # log_driver.info("错误原因：" + str(e) + ",错误位置：" + ", 错误行数：" + str(e.__traceback__.tb_lineno))
        return False

def test(result_cert_chain, cert_chain):
    son_cert_bytes = result_cert_chain[-1]
    son_cert = load_certificate(son_cert_bytes)
    for cert in cert_chain:
        father_cert_bytes = cert
        father_cert = load_certificate(father_cert_bytes)
        if verify_certificate_issuer(son_cert, father_cert, son_cert_bytes, father_cert_bytes):
            result_cert_chain.append(cert)
            cert_chain.remove(cert)
            return test(result_cert_chain, cert_chain)
    return result_cert_chain


def verify_cert(cert_chain):
    result_cert_chain = list()
    result_cert_chain.append(cert_chain.pop(0))
    result_cert_chain = test(result_cert_chain, cert_chain)
    return result_cert_chain


if __name__ == '__main__':
    file_path = "../Scan_result/certs\\gupiaojijin\\MainActivityAMC_55\\223.71.95.16_8443_12.crt"
    cert_data_bytes = read_android_cert(file_path)
    cert_chain = split_cert_chain(cert_data_bytes)
    result = verify_cert(cert_chain)

    # 示例证书 (PEM格式)
    child_cert_pem = b"""-----BEGIN CERTIFICATE-----
MIIDbDCCAxKgAwIBAgIQZ48Ecul4v/i2BAfC5NDgdjAKBggqgRzPVQGDdTBKMQsw
CQYDVQQGEwJDTjERMA8GA1UECgwIVW5pVHJ1c3QxKDAmBgNVBAMMH1VuaVRydXN0
IE9WIFNlY3VyZSBTZXJ2ZXIgQ0EgRzQwHhcNMjMxMTEwMDIzMzEyWhcNMjQxMTEw
MTU1OTU5WjCBhzELMAkGA1UEBhMCQ04xEjAQBgNVBAgMCeS4iua1t+W4gjESMBAG
A1UEBwwJ5LiK5rW35biCMScwJQYDVQQKDB7ljY7lrp3ln7rph5HnrqHnkIbmnInp
mZDlhazlj7gxDTALBgNVBAsTBEhCSkoxGDAWBgNVBAMMDyouZ20uZnNmdW5kLmNv
bTBZMBMGByqGSM49AgEGCCqBHM9VAYItA0IABC5rO7EGZ/LsNgvO7ihiz8mIxBeJ
p384ye18d44k4cPjIJWlFUSyJslskcF9TlI5mePoVujQyJ5RVrZzjkanz/6jggGa
MIIBljAfBgNVHSMEGDAWgBTWVG+mWHJ1QgvyBHlMTG3kNoqL1TAdBgNVHQ4EFgQU
wlWO+OMj9S5ag2SeC2C/0XXtg8IwDgYDVR0PAQH/BAQDAgbAMB0GA1UdJQQWMBQG
CCsGAQUFBwMBBggrBgEFBQcDAjAWBgNVHSAEDzANMAsGCSqBHIbvOgEBAjApBgNV
HREEIjAggg8qLmdtLmZzZnVuZC5jb22CDWdtLmZzZnVuZC5jb20wDAYDVR0TAQH/
BAIwADBYBgNVHR8EUTBPME2gS6BJhkdodHRwOi8vbGRhcDIuc2hlY2EuY29tL2Ew
ZWI0MGVjLzRhYjQvYWI2My8wNWM3NDhhMS84Mjc5NTBlNjYxNTRiNWFhLmNybDB6
BggrBgEFBQcBAQRuMGwwOAYIKwYBBQUHMAGGLGh0dHA6Ly9vY3NwMy5zaGVjYS5j
b20vb2NzcC9zaGVjYS9zaGVjYS5vY3NwMDAGCCsGAQUFBzAChiRodHRwOi8vY2Vy
dHMuc2hlY2EuY29tL3Mvb3Zzc2NnNC5jZXIwCgYIKoEcz1UBg3UDSAAwRQIgasHJ
QFEED+0SIDAIFn/bISif8hE8gg5yACpVWLg4HjoCIQCysebo3jEpacqamOEV/cnO
y1/rnbL4rsCJx/huc2x4Lw==
-----END CERTIFICATE-----"""
    parent_cert_pem = b"""-----BEGIN CERTIFICATE-----
MIICizCCAi+gAwIBAgIQQ+9lLgdXc+SS/QFXvh7hGTAMBggqgRzPVQGDdQUAMDcx
CzAJBgNVBAYTAkNOMREwDwYDVQQKDAhVbmlUcnVzdDEVMBMGA1UEAwwMVUNBIFJv
b3QgU00yMB4XDTE5MDYxODE2MDAwMFoXDTM0MDYxODE1NTk1OVowSjELMAkGA1UE
BhMCQ04xETAPBgNVBAoMCFVuaVRydXN0MSgwJgYDVQQDDB9VbmlUcnVzdCBPViBT
ZWN1cmUgU2VydmVyIENBIEc0MFkwEwYHKoZIzj0CAQYIKoEcz1UBgi0DQgAEB+tP
qDFIEr41tUYe3A3d9ttJJaOUYLyZVnJrRLMv4vsYhthvMp20/nJQlYQM6cd2oJbD
GDunocltEh6H5eEBNqOCAQYwggECMA4GA1UdDwEB/wQEAwIBhjASBgNVHRMBAf8E
CDAGAQH/AgEAMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAdBgNVHQ4E
FgQU1lRvplhydUIL8gR5TExt5DaKi9UwHwYDVR0jBBgwFoAU7uiwnNXc7HP973z6
UCzGwUDmTLMwQQYDVR0gBDowODA2BgRVHSAAMC4wLAYIKwYBBQUHAgEWIGh0dHBz
Oi8vd3d3LnNoZWNhLmNvbS9yZXBvc2l0b3J5MDoGA1UdHwQzMDEwL6AtoCuGKWh0
dHA6Ly9sZGFwMi5zaGVjYS5jb20vcm9vdC91Y2FzbTJzdWIuY3JsMAwGCCqBHM9V
AYN1BQADSAAwRQIhAOzvKOeMp/BD3Wv5mzt5KdYQBwwFKqcWgMU/0iiFFJ6+AiAb
+8jo1B0ENxTdsk0pHZXybqbHkcyhAz0obkCWqUBC8A==
-----END CERTIFICATE-----"""

    # 加载证书
    child_cert = load_certificate(child_cert_pem)
    parent_cert = load_certificate(parent_cert_pem)

    # 验证父子关系
    if verify_certificate_issuer(child_cert, parent_cert, child_cert_pem, parent_cert_pem):
        print("子证书由父证书签署。")
    else:
        print("子证书未由父证书签署。")
