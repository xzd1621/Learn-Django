from rest_framework.permissions import BasePermission


class devicePermission(BasePermission):
    def has_permission(self, request, view):
        if request.auth:
            print('认证成功！')
            return True
        else:
            print('认证失败！')
            return False
