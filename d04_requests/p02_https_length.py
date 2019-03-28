# coding = utf-8
import re
import socket
import ssl


def read_line(s):
    buffer = b''
    while True:
        buf = s.recv(1, 0)
        buffer += buf
        last_two_bytes = buffer[-2:]
        if last_two_bytes == b'\r\n':
            break
    return buffer


def read_bytes(s, size):
    buffer = b''
    size_ = size
    while size_ != 0:
        buf = s.recv(size_, 0)
        buffer += buf
        # 计算剩余的字节
        size_ -= len(buf)
        print(size_)

    return buffer


server_addr = ('ke.qq.com', 443)

# 创建socket
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
# 包装socket
ssl_sk = ssl.wrap_socket(sk)
# 链接https服务器
ssl_sk.connect(server_addr)
# 发起数据请求

str_request = 'GET / HTTP/1.1\r\n'
str_request += f'Host: {server_addr[0]}\r\n'
str_request += 'Accept: text/html\r\n'
str_request += 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36\r\n'
str_request += 'Accept-Language: zh-cn\r\n'
str_request += 'Connection: keep-alive\r\n'
str_request += '\r\n\r\n'

ssl_sk.send(str_request.encode('utf-8'), 0)
# 接收服务器响应
# 开始分析数据（行，头，空行，体）
# 1. 读取头
buf_header = b''
while True:
    buf = ssl_sk.recv(1, 0)
    buf_header += buf
    # 取最后四个字节
    last_four_byte = buf_header[-4:]
    if last_four_byte == b'\r\n\r\n':
        print('响应头读取完毕')
        break

# 分析头
str_header = buf_header.decode('utf-8')
print(str_header)
# 判定是否分包：Content-Length,
regexp = r'Content-Length: (\d*?)\r\n'
str_len = re.findall(regexp, str_header, re.M)
if str_len:
    int_len = int(str_len[0], 10)
    print('数据大小是：', int_len)
    # 读取体(注意：不需要扔掉数据）
    buffer = read_bytes(ssl_sk, int_len)
    print(buffer.decode('utf-8'))
else:
    print('分块数据体')
