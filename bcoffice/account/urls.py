from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from .views import *

urlpatterns = [
    url(r'^v1/users/$'                              , UserList.as_view()            , name=UserList.name),    # 사용자 목록 가져오기
    url(r'^v1/users/(?P<pk>[0-9]+)/$'               , UserDetail.as_view()          , name=UserDetail.name),  # 사용자 상세정보 가져오기
    url(r'^v1/users/regist/$'                       , UserCreate.as_view()          , name=UserCreate.name),  # 사용자 등록하기
    url(r'^v1/users/update/(?P<pk>[0-9]+)/$'        , UserUpdate.as_view()          , name=UserUpdate.name),  # 사용자 정보수정(관리자용)
    url(r'^v1/users/update-pass/(?P<pk>[0-9]+)/$'   , UserPasswordUpdate.as_view()  , name=UserPasswordUpdate.name),  # 사용자 패스워드 수정(관리자용)
    url(r'^v1/users/info/update/$'                  , UserPersonalUpdate.as_view()  , name=UserPersonalUpdate.name),  # 사용자 정보수정(개인용)
    url(r'^v1/users/info/update-pass/$'             , UserPersonalPasswordUpdate.as_view(), name=UserPersonalPasswordUpdate.name),  # 사용자 패스워드 수정(개인용)
    url(r'^v1/auth/$'                               , AuthList.as_view()            , name=AuthList.name),    # 사용자 목록 가져오기
    url(r'^v1/auth/update/$'                        , AuthModified.as_view()        , name=AuthModified.name),    # 사용자 목록 가져오기
    url(r'^v1/dept-type/$'                          , DeptCreateList.as_view()      , name=DeptCreateList.name),    # 사용자 목록 가져오기
    url(r'^v1/dept-type/(?P<pk>[0-9]+)/$'           , DeptDetail.as_view()          , name=DeptDetail.name),    # 사용자 목록 가져오기
    url(r'^v1/dept-rank/$'                          , DeptRankCreateList.as_view()  , name=DeptRankCreateList.name),    # 사용자 목록 가져오기
    url(r'^v1/dept-rank/(?P<pk>[0-9]+)/$'           , DeptRankDetail.as_view()      , name=DeptRankDetail.name),    # 사용자 목록 가져오기
    url(r'^v1/dept-duty/$'                          , DeptDutyCreateList.as_view()  , name=DeptDutyCreateList.name),    # 사용자 목록 가져오기
    url(r'^v1/dept-duty/(?P<pk>[0-9]+)/$'           , DeptDutyDetail.as_view()      , name=DeptDutyDetail.name),    # 사용자 목록 가져오기
    url(r'^v1/admin/initialize/once/$'              , AdminUserCreate.as_view()     , name=AdminUserCreate.name),
    url(r'^v1/api-token-auth/'                      , obtain_jwt_token),   # 사용자 로그인(토큰발급)
    url(r'^v1/api-token-verify/'                    , verify_jwt_token),   # 사용자 토큰 유효성 검사
    url(r'^v1/api-token-refresh/'                   , refresh_jwt_token),  # 사용자 토큰 갱신
    url(r'^v1/api-logout/'                          , user_logout)   # 로그아웃
]
