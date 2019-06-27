from django.db import models

# Create your models here.

"""
设备表
包括设备id,使用md5算法生成的uuid,密码，
最后登录时间，地理位置，和设备类型
"""


class device(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    uuid = models.CharField(max_length=50, blank=True, default='')
    password = models.CharField(max_length=30)
    is_login = models.BooleanField(default=False)
    last_login_time = models.DateTimeField()
    location = models.CharField(max_length=30)
    device_type = models.IntegerField(
        choices=((1, 'Phone'), (2, 'Camera')),
        default=1
    )

    def __str__(self):
        return self.id


"""
数据表
包括发送数据的文件名，数据类型、接收时间、数据大小、来源设备、存储位置
"""


class data(models.Model):
    name = models.CharField(max_length=30, default='')
    data_type = models.CharField(max_length=30)
    receive_time = models.DateTimeField()
    size = models.CharField(max_length=30)
    from_device = models.ForeignKey(device, related_name='device_data',
                                    on_delete=models.CASCADE)
    storage_location = models.CharField(max_length=100)

    def __str__(self):
        return self.storage_location
