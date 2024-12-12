def store_cert(file_path, cert):
    with open(file_path, 'wb') as f:
        f.write(cert)