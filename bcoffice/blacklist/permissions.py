from rest_framework import permissions
from bcoffice.permission import PermissionUtil

"""
블랙 리스트 출금주소 등록
"""
class BlackListWithdrawAddrCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
블랙 리스트 출금주소 목록조회
"""
class BlackListWithdrawAddrListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
블랙 리스트 등록
"""
class BlackListCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
블랙 리스트 목록조회
"""
class BlackListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)