from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import (
    Auth
    , UserProfile
    , DepartmentType
    , DepartmentRank
    , DepartmentDuty
    , STATUS
)

from datetime import datetime

User = get_user_model()

# 권한 시리얼라이저
class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ['id', 'user_id', 'role']
        

# 권한 생성용 시리얼라이저
class AuthCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    role = serializers.CharField(required=True)

    def create(self, validated_data):
        user_id = validated_data['user_id']
        role = validated_data['role']

        auth_obj = Auth(
            user_id = user_id
            , role = role
        )

        auth_obj.save()
        return auth_obj

# 권한 시리얼라이저
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ['role']

class DepartmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentType
        fields = [
            'id'
            , 'dept_cd'
            , 'team_cd'
            , 'dept_name'
            , 'dept_eng_name'
            , 'managerial'
            , 'status'
            , 'close_date'
            , 'created_at'
            , 'updated_at'
        ]

class DepartmentRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentRank
        fields = [
            'id'
            , 'rank_cd'
            , 'rank_name'
            , 'rank_eng_name'
            , 'status'
            , 'close_date'
            , 'created_at'
            , 'updated_at'
        ]


class DepartmentDutySerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentDuty
        fields = [
            'id'
            , 'duty_cd'
            , 'duty_name'
            , 'duty_eng_name'
            , 'status'
            , 'close_date'
            , 'created_at'
            , 'updated_at'
        ]


# 사용자 프로파일 생성 시리얼라이저
class UserProfileCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)


# 사용자 생성 시리얼라이저
class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'email'
            , 'password'
            , 'cell_phone'
            , 'name'
            , 'eng_name'
            , 'emp_no'
            , 'active'
            , 'status'
            , 'joined_date'
            , 'close_date'
            , 'dept_type'
            , 'dept_rank'
            , 'dept_duty'
        ]

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }
    
    # 사용자 생성
    def create(self, validated_data):
        email       = validated_data['email']
        password    = validated_data['password']
        cell_phone  = validated_data['cell_phone']
        name        = validated_data['name']
        eng_name    = validated_data['eng_name']
        dept_type   = validated_data['dept_type']
        dept_rank   = validated_data['dept_rank']
        dept_duty   = validated_data['dept_duty']
        joined_date = validated_data['joined_date']
        active      = validated_data['active']
        status      = validated_data['status']
        close_date  = validated_data['close_date']

        user_obj = User(
            email           = email
            , cell_phone    = cell_phone
            , name          = name
            , eng_name      = eng_name
            , dept_type     = dept_type
            , dept_rank     = dept_rank
            , dept_duty     = dept_duty
            , joined_date   = joined_date
            , active        = active
            , status        = status
            , close_date    = close_date
        )

        count = int(User.objects.count()) + 1

        user_obj.emp_no = str(datetime.now().year) + '{0:04d}'.format(count)

        user_obj.set_password(password)
        user_obj.save()

        # 사용자 생성 후 기본권한을 부여한다.
        auth = Auth(user_id = user_obj.get_id(), role="ROLE_Default")
        auth.save()
        return user_obj

# 정보 업데이트용 시리얼라이저
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name'
            , 'eng_name'
            , 'cell_phone'
            , 'active'
            , 'status'
            , 'dept_type'
            , 'dept_rank'
            , 'dept_duty'
            , 'joined_date'
            , 'close_date'
        ]

# 개인 정보 업데이트용 시리얼라이저
class UserPersonalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name'
            , 'eng_name'
            , 'cell_phone'
        ]

# 패스워드 업데이트용 시리얼라이저
class UserPasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

# 사용자 일반 시리얼라이저 
class UserSerializer(serializers.ModelSerializer):
    auth_list = serializers.SlugRelatedField(many=True, read_only=True, slug_field='role')

    dept_type = DepartmentTypeSerializer(many=False,  read_only=True)
    dept_rank = DepartmentRankSerializer(many=False,  read_only=True)
    dept_duty = DepartmentDutySerializer(many=False,  read_only=True)

    class Meta:
        model = User
        fields = [
            'id'
            , 'name'
            , 'eng_name'
            , 'email'
            , 'password'
            , 'emp_no'
            , 'cell_phone'
            , 'active'
            , 'status'
            , 'joined_date'
            , 'dept_type'
            , 'dept_rank'
            , 'dept_duty'
            , 'close_date'
            , 'created_at'
            , 'updated_at'
            , 'auth_list'
        ]

# 토큰 발급용 유저 시리얼라이저
class UserAuthSerializer(serializers.ModelSerializer):
    auth_list = serializers.SlugRelatedField(many=True, read_only=True, slug_field='role')    
    class Meta:
        model = User
        fields = ['id'
            , 'name'
            , 'emp_no'
            , 'eng_name'
            , 'email'
            , 'active'
            , 'updated_at'
            , 'auth_list'
        ]