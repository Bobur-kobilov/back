from rest_framework import permissions
from bcoffice.permission import PermissionUtil


class OrderPermission(permissions.BasePermission):
    """
    주문내역
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

class OrderExcelPermission(permissions.BasePermission):
    """
    주문내역 엑셀 내보내기
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)
        
class OrderDetailPermission(permissions.BasePermission):
    """
    주문내역 조회
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

class OrderDetailExcelPermission(permissions.BasePermission):
    """
    주문내역 엑셀 내보내기
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

class OrderDonePermission(permissions.BasePermission):                
    """
    체결내역 조회
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

class OrderDoneExcelPermission(permissions.BasePermission):
    """
    체결내역 엑셀 내보내기
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

class OrderStopPermission(permissions.BasePermission):                        
    """
    STOP 주문내역
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

class OrderStopExcelPermission(permissions.BasePermission):
    """
    STOP주문 내역 엑셀 내보내기
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

class OrderForceCancelPermission(permissions.BasePermission):
    """
    주문내역 강제취소
    """

    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Order_Force_Cancel"]
        return PermissionUtil.has_permission(request, allow_list)