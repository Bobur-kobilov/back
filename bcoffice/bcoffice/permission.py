from account.models import Auth
from rest_framework.permissions import SAFE_METHODS


"""
권한 관련 유틸 클래스
"""
class PermissionUtil:
    """
    기본 권한처리 메서드
    """
    def has_permission(request, allow_list):
        if request.user is None:
            return False

        user = request.user
        authentications = Auth.objects.filter(user_id=user.id)

        result = False

        for item in authentications:
            if item.get_role() in allow_list:
                result = True
                break
        
        return result

    """
    읽기전용 권한 처리 메서드
    """
    def read_only_permission(request, allow_list):
        """
        request method가 GET, HEAD, OPTION를 포함하고 있다면
        권한문제 없이 해당 API를 호출할 수 있다.
        """
        if request.method in SAFE_METHODS:
            return True

        """
        그 외 method인 경우 지정된 권한을 할당 받은 사용자만
        해당 API를 호출할 수 있다.
        """
        if request.user is None:
            return False

        user = request.user
        authentications = Auth.objects.filter(user_id=user.id)

        result = False

        for item in authentications:
            if item.get_role() in allow_list:
                result = True
                break
        
        return result