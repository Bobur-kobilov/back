from rest_framework import permissions
from bcoffice.permission import PermissionUtil

"""
암호화폐 잔고조회
"""
class CoinBalancePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Check_Exch_Balance"]
        return PermissionUtil.has_permission(request, allow_list)
        
"""
암호화폐 입금내역조회
"""
class CoinDepositHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)
                
"""
암호화폐 입금내역 엑셀 내보내기
"""
class CoinDepositHistoryExcelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

        
"""
암호화폐 출금내역조회
"""
class CoinWithdrawHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
암호화폐 출금내역상세조회
"""
class CoinWithdrawHistoryDetailPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
암호화폐 출금내역 엑셀 내보내기
"""
class CoinWithdrawHistoryExcelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
HOT/COLD 출금 요청 사유 권한
"""
class WithdrawApplyReasonPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"] :
            allow_list = ["ROLE_Super", "ROLE_Default"]
        else :
            allow_list = ["ROLE_Super", "ROLE_Withdrawal_Request_HOT", "ROLE_Withdrawal_Request_COLD"]
        return PermissionUtil.has_permission(request, allow_list)

"""
HOT 출금 요청 승인, 거절 권한
"""
class HotWithdrawApplyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Withdrawal_Approve_HOT"]
        return PermissionUtil.has_permission(request, allow_list)


"""
COLD 출금 요청 승인, 거절 권한
"""
class ColdWithdrawApplyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Withdrawal_Approve_COLD"]
        return PermissionUtil.has_permission(request, allow_list)


"""
HOT/COLD 출금 요청 권한
"""
class WithdrawApplyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)


"""
거래소 출금내역 조회 권한
"""
class WithdrawHistoryListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
콜드 월렛 출금 TXID 입력 권한
"""
class ColdWithdrawTxidUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Withdrawal_Request_COLD",  "ROLE_Withdrawal_Approve_COLD"]
        return PermissionUtil.has_permission(request, allow_list)

"""
거래소 출금승인 권한
"""
class WithdrawConfirmPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
수동 출금 처리
"""
class ManualWithdrawConfirmePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Manual_Deposit_Withraw"]
        return PermissionUtil.has_permission(request, allow_list)

"""
콜드월렛 잔고 수동수정
"""
class ColdwalletBalanceUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Coldwallet_Balance_Update"]
        return PermissionUtil.has_permission(request, allow_list)

"""
일자별 입출금 내역
"""
class DailyDepositWithdrawPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"]:
            allow_list = ["ROLE_Super", "ROLE_Trend"]
        elif request.method in ["DELETE"]:
            allow_list = ["ROLE_Super", "ROLE_Manage_Data"]
        return PermissionUtil.has_permission(request, allow_list)

"""
일자별 매출액
"""
class DailyTotalSalesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"]:
            allow_list = ["ROLE_Super", "ROLE_Trend"]
        elif request.method in ["DELETE"]:
            allow_list = ["ROLE_Super", "ROLE_Manage_Data"]
        return PermissionUtil.has_permission(request, allow_list)

class HoldListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

