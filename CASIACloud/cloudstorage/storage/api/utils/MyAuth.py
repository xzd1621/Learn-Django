import datetime
import hashlib
import json

from rest_framework.authentication import BaseAuthentication

from storage.models import device, data


class deviceAuth(BaseAuthentication):
    def authenticate(self, request):
        if request.method == 'POST':
            id = request.POST.get('id', None)
            password = request.POST.get('password', None)
            uuid = request.POST.get('uuid', None)

            # 首次登录，post id和password
            if id is not None and password is not None:
                try:
                    this_device = device.objects.filter(id=id, password=password).first()
                    print(this_device)
                    if this_device is not  None:
                        device.objects.filter(id=id, password=password).update(is_login=True)
                        device.objects.filter(id=id, password=password).update(
                            uuid=str(hashlib.md5(id.encode()).hexdigest()))
                        device.objects.filter(id=id, password=password).update(last_login_time=datetime.datetime.now())
                    return this_device, None
                except:
                    return None, None
            # 使用uuid登录
            elif uuid is not None:
                try:
                    this_device = device.objects.filter(uuid=uuid).first()
                    if (datetime.datetime.now() - this_device.last_login_time).seconds > 15:
                        device.objects.filter(uuid=uuid).update(is_login=False)
                    if this_device.is_login:
                        device.objects.filter(uuid=uuid).update(last_login_time=datetime.datetime.now())
                    return this_device, None
                except:
                    return None, None
            else:
                return None, None
        else:
            return None, None
