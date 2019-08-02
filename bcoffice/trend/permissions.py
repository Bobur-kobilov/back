from rest_framework import permissions
from bcoffice.permission import PermissionUtil

class TrendPermission(permissions.BasePermission):                        
    """
    trend 내역
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)


class CoinTransactionStatusPermission(permissions.BasePermission):
    """
    코인별 거래현황
    """
    def has_permission(self, request, view):
        if request.method in ["GET"]:
            allow_list = ["ROLE_Super", "ROLE_Trend"]
        elif request.method in ["DELETE"]:
            allow_list = ["ROLE_Super", "ROLE_Manage_Data"]
        return PermissionUtil.has_permission(request, allow_list)

class TradeOperationsPermission(permissions.BasePermission):
    """
    거래 운영
    """
    def has_permission(self, request, view):
        if request.method in ["GET"]:
            allow_list = ["ROLE_Super", "ROLE_Trend"]
        elif request.method in ["DELETE"]:
            allow_list = ["ROLE_Super", "ROLE_Manage_Data"]
        return PermissionUtil.has_permission(request, allow_list)

class ReferralStatusPermission(permissions.BasePermission):
    # 레퍼럴 현황
    def has_permission(self, request, view):
        if request.method in ["GET"]:
            allow_list = ["ROLE_Super", "ROLE_Trend"]
        elif request.method in ["DELETE"]:
            allow_list = ["ROLE_Super", "ROLE_Manage_Data"]
        return PermissionUtil.has_permission(request, allow_list)