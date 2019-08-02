from rest_framework import permissions
from bcoffice.permission import PermissionUtil


"""
1:1 문의 카테고리 조회
"""
class QuestionTypePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.read_only_permission(request, allow_list)


"""
1:1 문의 내역 조회
"""
class QuestionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.read_only_permission(request, allow_list)


"""
1:1 문의 내역 작성
"""
class QuestionCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.read_only_permission(request, allow_list)


"""
1:1 문의 내역 상세 조회
"""
class QuestionDetailPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"]  :
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.method in ["PUT", "PATCH", "DELETE"] :
            allow_list = ["ROLE_Super", "ROLE_QnA_Answer"]
        else :
            allow_list = ["ROLE_Super"]

        return PermissionUtil.read_only_permission(request, allow_list)


"""
1:1 문의 내역 답변 처리상태 변경
"""
class QuestionUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_QnA_Answer"]
        return PermissionUtil.has_permission(request, allow_list)


"""
1:1 문의 수정, 제거 (거래소 API)
"""
class QuestionUpdateDestroyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]  :
            # allow_list = ["ROLE_Super", "ROLE_Default"]
            return True
        else :
            allow_list = ["ROLE_Super"]

        return PermissionUtil.read_only_permission(request, allow_list)


"""
1:1 답변 내역 상세조회, 수정, 삭제
"""
class AnswerDetailUpdateDestroyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"]  :
            return True
        elif request.method in ["PUT", "PATCH", "DELETE"] :
            allow_list = ["ROLE_Super", "ROLE_QnA_Answer"]
        else :
            allow_list = ["ROLE_Super"]

        return PermissionUtil.has_permission(request, allow_list)


"""
메일, SMS 보내기 권한
"""
class SendPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Mail"]
        return PermissionUtil.has_permission(request, allow_list)


class SupportHistoryPermission(permissions.BasePermission):
    """
    고객 지원 내역
    """
    def has_permission(self, request, view):
        if request.method in ["GET"]:
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.method in ["PUT"]:
            allow_list = ["ROLE_Super", "ROLE_Support_History"]
        return PermissionUtil.has_permission(request, allow_list)