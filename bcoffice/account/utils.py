from .serializers import UserAuthSerializer

# JWT 관련 메서드

# 사용자 모델에서 secret 필드의 값을 가져오는 메서드
def get_secret_key(user_model):
    return user_model.secret

# 토큰 발급시 수행되는 핸들러 메서드
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserAuthSerializer(user, context={'request': request}).data
    }