from rest_framework import permissions
from bcoffice.permission import PermissionUtil


class SecurityLevelPolicyPermission(permissions.BasePermission):
    """
    거래소 회원 상세정보 조회
    """
    def has_permission(self, request, view):
        if request.method in ["GET"] :
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.method in ["POST", "PUT", "PATCH", "DELETE"] :
            allow_list = ["ROLE_Super", "ROLE_Edit_Policy"]
        else :
            allow_list = ["ROLE_Super"]

        return PermissionUtil.has_permission(request, allow_list)

        
class SystemAlarmViewPermission(permissions.BasePermission):
    """
    시스템 메시지 전송방식 설정
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Edit_Policy"]
        return PermissionUtil.has_permission(request, allow_list)
        

class SystemAlarmUpdateViewPermission(permissions.BasePermission):
    """
    시스템 메시지 전송방식 수정
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Edit_Policy"]
        return PermissionUtil.has_permission(request, allow_list)
        

class ReferralCommissionPermission(permissions.BasePermission):
    """
    추천인 커미션 보상비율 가져오기
    """
    def has_permission(self, request, view):
        if request.method in ["GET"] :
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.method in ["POST", "PUT", "DELETE"] :
            allow_list = ["ROLE_Super", "ROLE_Edit_Policy"]
        else :
            allow_list = ["ROLE_Super"]
            
        return PermissionUtil.has_permission(request, allow_list)

        
class DepositAddressListPermission(permissions.BasePermission):
    """
    입금주소 가져오기
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)
        

class DepositAddressCreatePermission(permissions.BasePermission):
    """
    입금주소 작성하기
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Edit_Policy"]
        return PermissionUtil.has_permission(request, allow_list)
        

class DepositAddressRetrieveDestroyPermission(permissions.BasePermission):
    """
    입금주소 조회 및 삭제
    """
    def has_permission(self, request, view):
        if request.method in ["GET"] :
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.method in ["POST", "PUT", "PATCH", "DELETE"] :
            allow_list = ["ROLE_Super", "ROLE_Edit_Policy"]
        else :
            allow_list = ["ROLE_Super"]
            
        return PermissionUtil.has_permission(request, allow_list)
        

class DepositAddressUpdatePermission(permissions.BasePermission):
    """
    입금주소 수정
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super"]
        return PermissionUtil.has_permission(request, allow_list)
        

class TagCoinListPermission(permissions.BasePermission):
    """
    태그가 필요한 코인 목록
    """
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

        
class WalletRuleListPermission(permissions.BasePermission):
    """
    입금주소 작성하기
    """
    def has_permission(self, request, view):
        if request.method in ["GET"] :
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.method in ["POST", "PUT", "PATCH", "DELETE"] :
            allow_list = ["ROLE_Super", "ROLE_Edit_Policy"]
        else :
            allow_list = ["ROLE_Super"]
            
        return PermissionUtil.has_permission(request, allow_list)

class MarketManagementPermission(permissions.BasePermission):
    """
    마켓별 매도가격 제한
    """
    def has_permission(self, request, view):
        if request.method in ["GET"]:
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            allow_list = ["ROLE_Super", "ROLE_Edit_Policy"]
        else:
            allow_list = ["ROLE_Super"]

        return PermissionUtil.has_permission(request, allow_list)