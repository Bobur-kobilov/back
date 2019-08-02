from rest_framework import permissions
from bcoffice.permission import PermissionUtil

"""
거래소 회원 목록
"""
class MemberPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
거래소 회원 상세정보 조회
"""
class MemberDetailPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
거래소 회원 잔고조회
"""
class MemberBalancePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
회원 자산변동 이력
"""
class MemberAccountHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
회원 자산변동 이력 엑셀 내보내기
"""
class MemberAccountHistoryExcelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
회원 활동내역
"""
class MemberActiveHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
추천인정보 상단 값
"""
class ReferralCommonValuePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
추천인정보 피추천인
"""
class MemberReferralPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
추천인정보 지급내역
"""
class MemberReferralPayPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
추천인정보 수수료 변경내역 가져오기
"""
class MemberReferralFeeGetPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Referral_Rate"]
        return PermissionUtil.has_permission(request, allow_list)

"""
추천인정보 수수료 변경내역 수정하기
"""
class MemberReferralFeePostPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Referral_Rate"]
        return PermissionUtil.has_permission(request, allow_list)


"""
동결사유 가져오기
"""
class LockedReasonAPIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

# 사용자 인증내역, 비활성화, 이용제한, 탈퇴 수정 권한
class MemberForceDisablePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.META['PATH_INFO'].find('factor_auth') > -1 or request.META['PATH_INFO'].find('kyc_auth') > -1:
            allow_list = ["ROLE_Super", "ROLE_ID_Verification"]
        elif request.META['PATH_INFO'].find('disable') > -1:
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.META['PATH_INFO'].find('restrict') > -1:
            allow_list = ["ROLE_Super", "ROLE_Restrict_Use"]
        elif request.META['PATH_INFO'].find('deleted') > -1:
            allow_list = ["ROLE_Super", "ROLE_Member_Out"]
        return PermissionUtil.has_permission(request, allow_list)

"""
회원정보 정정이력
"""
class MemberModifyHistoryListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
코인수량정정
"""
class ModifyCoinAmountPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Member_Modify_Coin"]
        return PermissionUtil.has_permission(request, allow_list)

"""
코인수량정정 리스트
"""
class ModifyCoinListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)