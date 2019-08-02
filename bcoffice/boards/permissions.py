from rest_framework import permissions
from bcoffice.permission import PermissionUtil


"""
FAQ 목록 조회
"""
class FaqListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
        # allow_list = ["ROLE_Super", "ROLE_H"]
        # return PermissionUtil.read_only_permission(request, allow_list)


"""
FAQ 작성 권한
"""
class FaqCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
FAQ 상세 조회
"""
class FaqDetailPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"]  :
            return True
        elif request.method in ["PUT", "PATCH", "DELETE"] :
            allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        else :
            allow_list = ["ROLE_Super"]
        return PermissionUtil.read_only_permission(request, allow_list)


"""
FAQ 상세 수정, 제거
"""
class FaqUpdateDestroyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"]  :
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.method in ["PUT", "PATCH", "DELETE"] :
            allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        else :
            allow_list = ["ROLE_Super"]
        
        return PermissionUtil.has_permission(request, allow_list)


"""
FAQ 카테고리 목록 조회
"""
class FaqCategoryListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.read_only_permission(request, allow_list)


"""
FAQ 카테고리 작성
"""
class FaqCategoryCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
FAQ 카테고리 상세조회, 수정, 제거
"""
class FaqCategoryUpdateDestroyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.method in ['POST', 'PUT', 'DELETE'] :
            allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
공지사항 목록
"""
class NoticeListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.read_only_permission(request, allow_list)


"""
공지사항 작성
"""
class NoticeCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
공지사항 목록 상세 조회
"""
class NoticeDetailPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.read_only_permission(request, allow_list)

"""
공지사항 목록 수정, 삭제
"""
class NoticeUpdateDestroyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
공지사항 첨부파일 생성
"""
class NoticeAttachCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Mail"]
        return PermissionUtil.has_permission(request, allow_list)


"""
공지사항 첨부파일 제거
"""
class NoticeAttachDestroyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Mail"]
        return PermissionUtil.has_permission(request, allow_list)


"""
Daily뉴스 목록
"""
class DailyNewsListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.read_only_permission(request, allow_list)


"""
Daily뉴스 작성
"""
class DailyNewsCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
Daily뉴스 목록 상세 조회
"""
class DailyNewsDetailPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

"""
Daily뉴스 목록 수정, 삭제
"""
class DailyNewsUpdateDestroyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
Daily뉴스 첨부파일 생성
"""
class DailyNewsAttachCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
Daily뉴스 첨부파일 제거
"""
class DailyNewsAttachDestroyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
코인가이드 목록
"""
class CoinGuideListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.read_only_permission(request, allow_list)


"""
코인가이드 작성
"""
class CoinGuideCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
코인가이드 목록 상세 조회
"""
class CoinGuideDetailPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


"""
코인가이드 목록 수정, 삭제
"""
class CoinGuideUpdateDestroyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
코인가이드 로고 생성
"""
class CoinGuideAttachCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
코인가이드 로고 제거
"""
class CoinGuideAttachDestroyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
코인가이드 유용한링크 생성
"""
class CoinGuideUsefulLinkCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)


"""
코인가이드 유용한링크 제거
"""
class CoinGuideUsefulLinkDeletePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Notice_Board"]
        return PermissionUtil.has_permission(request, allow_list)
        
        
"""
위지윅 에디터 이미지 업로드 권한
"""
class ImageUploadPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)