from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import datetime

import uuid

STATUS = {
    'ACTV' : 'ACTV' # 정상
    , 'STOP' : 'STOP' # 정지
    , 'VCTN' : 'VCTN' # 휴가
    , 'LAVE' : 'LAVE' # 퇴사
    , 'NTUS' : 'NTUS' # NOT USE 더이상 사용하지 않음
}

# 사용자 정모 관리 클래스
class UserManager(BaseUserManager):
    
    # 사용자 생성
    def create_user(
        self
        , email
        , password=None
        , cell_phone=""
        , status="ACTV"
        , joined_date=None
        , dept_type=1
        , dept_rank=1
        , dept_duty=1
        , is_active=False
        , role="ROLE_Default"):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        
        user_obj = self.model(
            email = self.normalize_email(email)
        )

        user_obj.set_password(password)
        user_obj.cell_phone = cell_phone
        user_obj.status = status
        user_obj.joined_date = joined_date
        user_obj.dept_type = dept_type
        user_obj.dept_rank = dept_rank
        user_obj.dept_duty = dept_duty
        
        user_obj.active = is_active
        user_obj.save(using=self.db)

        # 사용자 생성이 완료되면 권한 테이블에도 사용자 정보를 추가한다.
        self.create_auth(user_obj, role)

        return user_obj
    
    # 스테프 사용자 추가
    def create_staffuser(
        self
        , email
        , password
        , cell_phone
        , status
        , joined_date
        , dept_type
        , dept_rank
        , dept_duty):
        user = self.create_user( email
            , password = password
            , cell_phone = cell_phone
            , status = status
            , joined_date = joined_date
            , dept_type=dept_type
            , dept_rank=dept_rank
            , dept_duty=dept_duty
            , is_active = True
            , role="ROLE_M"
        )
        return user
    
    # 슈퍼관리자 추가
    def create_superuser(
        self
        , email
        , password
        , cell_phone
        , status
        , joined_date
        , dept_type
        , dept_rank
        , dept_duty):
        user = self.create_user( 
            email
            , password=password
            , cell_phone = cell_phone
            , status = status
            , joined_date = joined_date
            , dept_type = dept_type
            , dept_rank = dept_rank
            , dept_duty = dept_duty
            , is_active = True
            , role = "ROLE_Super"
        )
        return user
    
    # 권한 정보 등록
    def create_auth( self, user_obj, role='ROLE_Default'):
        role_obj = Auth(
            user_id = user_obj.get_id(),
            role = role
        )

        role_obj.save(using=self.db)

        return role_obj


"""
부서코드
"""
class DepartmentType(models.Model):
    id              = models.BigAutoField(primary_key=True)
    dept_cd         = models.CharField(max_length=5, null=False) # 부서코드
    team_cd         = models.CharField(max_length=5, null=False, unique=True) # 팀코드
    dept_name       = models.CharField(max_length=100) # 부서명
    dept_eng_name   = models.CharField(max_length=100, null=True, blank=True) # 부서명(영어)
    managerial      = models.BooleanField(default=False) # 관리직구분
    status          = models.CharField(max_length=20, default=STATUS['ACTV'])
    close_date      = models.DateTimeField(null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dept_type'

"""
직급코드
"""
class DepartmentRank(models.Model):
    id              = models.BigAutoField(primary_key=True)
    rank_cd         = models.CharField(max_length=5, null=False, unique=True)
    rank_name       = models.CharField(max_length=100)
    rank_eng_name   = models.CharField(max_length=150, null=True, blank=True)
    status          = models.CharField(max_length=20, default=STATUS['ACTV'])
    close_date      = models.DateTimeField(null=True)
    created_at      = models.DateTimeField(auto_now_add=True) # 레코드 생성일
    updated_at      = models.DateTimeField(auto_now=True) # 레코드 수정일
    class Meta:
        db_table = 'dept_rank'

"""
직책코드
"""
class DepartmentDuty(models.Model):
    id            = models.BigAutoField(primary_key=True)
    duty_cd       = models.CharField(max_length=5, null=False, unique=True)
    duty_name     = models.CharField(max_length=100)
    duty_eng_name = models.CharField(max_length=150, null=True, blank=True)
    status        = models.CharField(max_length=20, default=STATUS['ACTV'])
    close_date    = models.DateTimeField(null=True)
    created_at    = models.DateTimeField(auto_now_add=True) # 레코드 생성일
    updated_at    = models.DateTimeField(auto_now=True) # 레코드 수정일
    class Meta:
        db_table = 'dept_duty'

# 유저 모델
class User(AbstractBaseUser):
    id                  = models.BigAutoField(primary_key=True)
    email               = models.EmailField(max_length=255, unique=True) # 이메일
    cell_phone          = models.CharField(max_length=255, unique=False, null=False, default='') # 휴대전화번호
    name                = models.CharField(max_length=255, default='') # 이름
    eng_name            = models.CharField(max_length=255, default='', null=True, blank=True) # 영어이름
    emp_no              = models.CharField(max_length=20, unique=False, null=False, default='') # 사원번호
    active              = models.BooleanField(default=False) # 활성화 여부
    status              = models.CharField(max_length=50, default=STATUS['ACTV']) # 상태정보 : ACTV(활성화), STOP(정지), VCTN(휴가), LAVE(퇴사)
    
    dept_type           = models.ForeignKey(DepartmentType, related_name='dept_type', on_delete=models.CASCADE, default=1) # 부서
    dept_rank           = models.ForeignKey(DepartmentRank, related_name='dept_rank', on_delete=models.CASCADE, default=1) # 직급
    dept_duty           = models.ForeignKey(DepartmentDuty, related_name='dept_duty', on_delete=models.CASCADE, default=1) # 직책
    
    joined_date         = models.DateTimeField(null=True) # 입사일
    close_date          = models.DateTimeField(null=True) # 해지일
    created_at          = models.DateTimeField(auto_now_add=True) # 레코드 생성일
    updated_at          = models.DateTimeField(auto_now=True) # 레코드 수정일
    secret              = models.UUIDField(default=uuid.uuid4) # 시크릿 필드

    USERNAME_FIELD  = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
    # 사용자 PK 얻는 메서드
    def get_id(self):
        return self.id

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.active
    
    def has_module_perms(self, app_label):
        return self.active

    # 활성 사용자 여부 확인    
    @property
    def is_active(self):
        return self.active

    # 스태프 사용자 확인
    @property
    def is_staff(self):
        result = False
        for auth in self.auth_list.all():
            if auth.role in ['ROLE_Super', 'ROLE_M']:
                result = True
                break
        return result
    
    # 슈퍼어드민 확인
    @property
    def is_admin(self):
        result = False
        for auth in self.auth_list.all():
            if auth.role in ['ROLE_Super']:
                result = True
                break
        return result

# 권한 테이블 모델
class Auth(models.Model):
    user = models.ForeignKey(User, related_name='auth_list', on_delete=models.CASCADE)
    role = models.CharField(max_length=30)

    def get_role(self):
        return self.role

# 사용자 개인 정보를 담기위한 모델
# 사용할지는 미지수
class UserProfile(models.Model):
    user                = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)


