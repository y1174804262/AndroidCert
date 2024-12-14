# Scanresult/cert is our collect certdata

if you have any question, please contact me by 1174804262@qq.com

# 项目介绍

# 项目结构
## 1.Scan_Certificate
该类中主要是对证书进行扫描，获取证书的信息，包括证书的颁发者、证书的有效期、证书的公钥、证书的签名算法等信息。
### 1.1 get_andriod_cert.py
该脚本主要是对Android应用的证书进行扫描,扫描使用tshark，监听网卡中的流量 **（具体使用时请修改网卡，监听实际需要监听的网卡）**。使用前首先需要将tshark在本地配置为环境变量，可在DOS命令行中使用命令
```angular2html
tshark -v
```
检查tshark安装情况，使用下面的命令可以检查可监听的网卡
```angular2html
tshark -D
```
### 1.2 result_change.py
该脚本主要是对扫描结果进行处理，由于网站可能使用CDN或负载均衡等其它手段，一个证书可能部署在多个ip上，因此需要对扫描结果进行处理，将重复证书剔除。

### 1.3 read_android_cert.py
从文件中读取证书，并定义有函数将读取到的证书转换为x509对象

### 1.4 parse_cert_plus.py
为了便于处理证书，该脚本主要是对已经读取完成的证书进行解析，获取证书的基本信息，包括证书的颁发者、证书的有效期、证书的公钥、证书的签名算法等信息。

### 1.5 resolv_certchain.py
读取已有证书解析证书链

## 2. neo4j
该类主要是对证书的信息进行存储，使用neo4j数据库进行存储，主要包括证书的颁发者、证书的有效期、证书的公钥、证书的签名算法等信息。

### 2.1 __init.py__
neo4j数据库的初始化，创建neo4j数据库驱动。

### 2.2 get_cert_data.py
最核心的函数，读取提取到的证书，并与解析证书进行相连处理证书

### 2.3 pack_data.py
对证书的信息进行打包，方便存储，简单讲该类为数据封装函数，将数据封装为neo4j的节点或关系

### 2.4 upload.py
上传数据到neo4j数据库,直接对neo4j数据库的操作，编写Cypher语句的直接位置

### 2.5 upload_root_cert.py
上传根证书到neo4j数据库，由于证书链解析是根据AIA进行解析，往往只能提取到中间证书，根证书很难提取到。因此将根证书数据库中的证书直接上传至neo4j。# PythonProject2
