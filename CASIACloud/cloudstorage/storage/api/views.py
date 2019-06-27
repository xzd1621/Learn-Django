import datetime
import hashlib
import json
import os
import psutil

from django.http import HttpResponse
from rest_framework import generics, mixins

from .. import CONFIG
from ..models import device, data
from .serializers import deviceSerializers


class deviceListView(mixins.ListModelMixin, mixins.CreateModelMixin,  generics.GenericAPIView):
    # authentication_classes = [deviceAuth, ]
    # permission_classes = [devicePermission, ]
    queryset = device.objects.all()
    serializer_class = deviceSerializers

    # 获取文件后缀名
    def get_file_extension(self, filename):
        arr = os.path.splitext(filename)
        return arr[len(arr) - 1].replace(".", "")

    # 判断系统是否繁忙, 是否可以接收文件
    # disk_usage:磁盘利用率
    # memory_percent: 内存占用率
    def is_acceptable(self):
        disk_usage = psutil.disk_usage('/').percent
        memory_percent = psutil.virtual_memory().percent
        net_connections = psutil.net_connections()
        if disk_usage<90 and memory_percent <95:
            return True
        else:
            return False


    # 登录验证
    def authenticate(self, id, password):
        this_device = None
        result = {"state": "fail", "reason": "用户名或密码错误", "code": 2}
        if id is not None and password is not None:
            try:
                this_device = device.objects.filter(id=id, password=password).first()
                if this_device is not None:
                    device.objects.filter(id=id, password=password).update(is_login=True)
                    device.objects.filter(id=id, password=password).update(
                        uuid=str(hashlib.md5(id.encode()).hexdigest()))
                    print(str(hashlib.md5(id.encode()).hexdigest()))
                    device.objects.filter(id=id, password=password).update(last_login_time=datetime.datetime.now())
                    result = {"state": "sucess", "reason": "登录成功", "code": 1}
            except:
                result = {"state": "fail", "reason": "用户名或密码错误", "code": 2}
        else:
            result["reason"] = "用户名或密码未填写完整"
        return result, this_device

    # 验证连接超时
    def not_time_out(self, uuid):
        try:
            this_device = device.objects.filter(uuid=uuid).first()
            if (datetime.datetime.now() - this_device.last_login_time).seconds > 15:
                device.objects.filter(uuid=uuid).update(is_login=False)
                return False, None
            if this_device.is_login:
                device.objects.filter(uuid=uuid).update(last_login_time=datetime.datetime.now())
                return True, this_device
        except:
            return False, None
        return False, None


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file', None)
        result = {"state": "fail", "reason": "云端繁忙", "code":4}
        # id = request.POST.get('id', None)
        # password = request.POST.get('password', None)
        print(request.POST.get('id'))
        print(request.data)
        id = request.data['id']
        password= request.data['password']

        print(id, password, '*'*10)
        uuid = request.POST.get('uuid', None)
        if uuid is not None:
            is_connect, this_device = self.not_time_out(uuid)
            if not is_connect:
                result = {"state": "fail", "reason": "uuid错误或连接超时", "code":5}
        else:
            result, this_device = self.authenticate(id, password)

        if this_device is not None:
            if file is not None:
                if self.is_acceptable():
                    name = file.name
                    data_type = self.get_file_extension(file.name)

                    # 无后缀的文件
                    if data_type == '':
                        data_type = 'other'

                    receive_time = datetime.datetime.now()
                    from_device = this_device
                    device_location = from_device.location
                    size = file.size
                    storage_location = os.path.join(CONFIG.RECEIVE_PATH, device_location, data_type)
                    if not os.path.exists(storage_location):
                        os.makedirs(storage_location)
                    destination = open(os.path.join(CONFIG.RECEIVE_PATH, device_location, data_type, file.name), 'wb+')
                    for chunk in file.chunks():
                        destination.write(chunk)
                    destination.close()
                    file_data = data(name=name, data_type=data_type, receive_time=receive_time, size=size, from_device=from_device, storage_location=storage_location)
                    file_data.save()
                    result = {"state":"success", "reason": "云端存储成功", "code":3}
                else:
                    result = {"state": "fail", "reason": "云端繁忙", "code": 4}
            else:
                result = {"state": "Require files","reason": "设备已登录，但未选择要发送的文件", "code": 6}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


    # def permission_denied(self, request, message=None):
    #     result = {
    #         "state": "fail",
    #         "reason": "其它登录错误",
    #         "code": 0,
    #     }
    #     if request.authenticators and request.user is None:
    #         if request.POST.get('uuid', None) is not None:
    #             result["reason"] = "连接超时或uuid错误"
    #             result["code"] = 5
    #         else:
    #             result["reason"] = "用户名或密码错误，或未填写完整"
    #             result["code"] = 2
    #     elif request.user is not None:
    #         result = {"state":"sucess", "reason":"登录成功", "code":1}
    #     return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
