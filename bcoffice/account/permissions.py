from rest_framework import permissions
from bcoffice.permission import PermissionUtil
from .models import Auth

class AccountAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allowRoleList = ["ROLE_Super", "ROLE_Default"]
        user = request.user
        authentications = Auth.objects.get(user_id=user.id)

        result = False

        for item in authentications:
            if item.get_role() in allowRoleList:
                result = True
                break
        
        return result

"""
사용자 목록 조회 권한
"""
class UserListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
사용자 생성 권한
"""
class UserCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Default"]
        return PermissionUtil.has_permission(request, allow_list)

"""
사용자 업데이트 권한
"""
class UserUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow_list = ["ROLE_Super", "ROLE_Auth_Mgmt"]
        return PermissionUtil.has_permission(request, allow_list)

"""
조직부서 권한
"""
class DeptTypePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"] :
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.method in ["POST", "PUT", "PATCH", "DELETE"] :
            allow_list = ["ROLE_Super", "ROLE_Organization_Mgmt"]
        else :
            allow_list = ["ROLE_Super"]
        return PermissionUtil.has_permission(request, allow_list)

"""
조직부서 직급
"""
class DeptRankPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"] :
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.method in ["POST", "PUT", "PATCH", "DELETE"] :
            allow_list = ["ROLE_Super", "ROLE_Organization_Mgmt"]
        else :
            allow_list = ["ROLE_Super"]
        return PermissionUtil.has_permission(request, allow_list)

"""
조직부서 직책
"""
class DeptDutyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"] :
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.method in ["POST", "PUT", "PATCH", "DELETE"] :
            allow_list = ["ROLE_Super", "ROLE_Organization_Mgmt"]
        else :
            allow_list = ["ROLE_Super"]

        return PermissionUtil.has_permission(request, allow_list)

"""
권한목록
"""
class AuthListCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"] :
            allow_list = ["ROLE_Super", "ROLE_Default"]
        elif request.method in ["POST", "PUT", "PATCH", "DELETE"] :
            allow_list = ["ROLE_Super", "ROLE_Auth_Mgmt"]
        else :
            allow_list = ["ROLE_Super"]
        return PermissionUtil.has_permission(request, allow_list)