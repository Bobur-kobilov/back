from rest_framework import permissions
from bcoffice.permission import PermissionUtil

"""
KRW 잔고조회 권한
"""
class BankBalanceListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)


"""
KRW 입금내역조회
"""
class BankDepositHistoryListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
KRW 출금내역조회
"""
class BankWithdrawHistoryListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)