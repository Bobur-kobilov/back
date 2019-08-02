from rest_framework import permissions
from bcoffice.permission import PermissionUtil


"""
관리자 메모 목록 권한
"""
class ManagerMemoListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)


"""
관리자 메모 삭제 권한
"""
class ManagerMemoDestroyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super"]
        return PermissionUtil.has_permission(request, allow_list)