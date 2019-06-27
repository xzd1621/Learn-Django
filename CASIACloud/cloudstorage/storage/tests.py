# Create your tests here.
import json
import multiprocessing
import os
import random
import requests
from urllib.error import URLError

import CONFIG

url = 'http://127.0.0.1:8000/api/device/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1;WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
           }


def make_data(id):
    """制造请求数据"""
    data = {
        "id": "0000"+str(id),
        "password": "123456",
    }
    return data


def run():
    """三种模拟请求"""
    num = random.randint(1, 4)
    data = make_data(num)
    send_path = CONFIG.SEND_PATH
    file_list = os.listdir(send_path)
    file = {"file": open(os.path.join(send_path, random.choice(file_list)), 'rb')}
    try:
        # s1:request请求
        # req = request.Request(url=url, data=data, headers=headers, method="POST")
        # response = request.urlopen(req)
        # resp = response.read()
        # print("服务器返回值为:\n", resp.decode('utf-8'))

        # s2:httpclient请求
        # httpclient = http.client.HTTPConnection(host='127.0.0.1', port=8001)
        # httpclient.request("POST", '/insert', data, headers)
        # response = httpclient.getresponse()
        # print(response.read().decode())

        # s3:requests请求
        resp = requests.post(url=url, data=data, files=file)
        print("状态:\n", resp)
        print("请求头:\n", resp.headers)
        print("服务器返回值为:\n", resp.text)
    except URLError as e:
        print('请求', e)
    except Exception as e:
        print('请求错误：', e)


# def call_gevent(count):
#     """调用gevent 模拟高并发"""
#     begin_time = time.time()
#     run_gevent_list = []
#     for i in range(count):
#         print('--------------%d--Test-------------' % i)
#         run_gevent_list.append(gevent.spawn(run()))
#     gevent.joinall(run_gevent_list)
#     end = time.time()
#     print('单次测试时间（平均）s:', (end - begin_time) / count)
#     print('累计测试时间 s:', end - begin_time)


if __name__ == '__main__':
    # 10万并发请求
    # test_count = 1000000
    # call_gevent(count=test_count)
    pool = multiprocessing.Pool(processes=100)
    for i in range(1):
        pool.apply(run)
    pool.close()

