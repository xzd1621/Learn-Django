"""
构造账户发送文件的csv
三元组 account,password,file
"""
import os
import random



def send_file(file_path,accounts):
    file_list = os.listdir(file_path)
    with open('device_send_file.csv', 'w+') as f:
        for file in file_list:
            file = os.path.join(file_path, file)
            account = random.choice(accounts)
            f.write(account['id']+ ',' + account['password']+','+ file+ '\n')


import psutil


def netstat(sport=None):
    status_list = ["LISTEN", "ESTABLISHED", "TIME_WAIT", "CLOSE_WAIT", "LAST_ACK", "SYN_SENT"]
    status_temp = []
    net_connections = psutil.net_connections()
    for key in net_connections:
        if sport is None:
            status_temp.append(key.status)
        else:
            if key.laddr[1] == sport:
                status_temp.append(key.status)

    for status in status_list:
        print(status, status_temp.count(status))


if __name__ == '__main__':

    accounts = [
        {'id': '00001', 'password': '123456'},
        {'id': '00002', 'password': '123456'},
        {'id': '00003', 'password': '123456'},
        {'id': '00004', 'password': '123456'},
        {'id': '00005', 'password': '123456'},
        {'id': '10001', 'password': '123456'},
        {'id': '10002', 'password': '123456'},
        {'id': '10003', 'password': '123456'},
    ]
    file_path = '/home/xuzhida/PycharmProjects/send'
    send_file(file_path, accounts)
    # netstat()