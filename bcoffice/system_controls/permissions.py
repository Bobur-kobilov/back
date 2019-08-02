from rest_framework import permissions
from bcoffice.permission import PermissionUtil


class CoinBlockHeightPermission(permissions.BasePermission):
    """
    CoinBlockHeight 조회 권한
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_System_Monitoring"]
        return PermissionUtil.has_permission(request, allow_list)

class CoinBalancePermission(permissions.BasePermission):
    """
    CoinBalance 권한
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Check_Exch_Balance"]
        return PermissionUtil.has_permission(request, allow_list)


class MtsVersionPermission(permissions.BasePermission):
    """
    MTS Version 조회 권한
    """
    def has_permission(self, request, view):
        if request.method in ["GET"] :
            return True
        elif request.method in ["POST", "PUT", "PATCH", "DELETE"] :
            allow_list = ["ROLE_Super", "ROLE_System_Activate"]
        return PermissionUtil.has_permission(request, allow_list)