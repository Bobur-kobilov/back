from django.conf.urls   import url
from .views import *

urlpatterns = [
    url(r'^v1/blacklist-ip/regist/$', BlackListCreate.as_view(), name=BlackListCreate.name),  # 블랙리스트 IP 등록
    url(r'^v1/blacklist-ip/list/$', BlackList.as_view(), name=BlackList.name),  # 블랙리스트 IP 목록조회
    url(r'^v1/blacklist-ip/history/$', BlackListHistory.as_view(), name=BlackListHistory.name),  # 블랙리스트 IP제한 내역조회
    url(r'^v1/blacklist-withdraw-addr/regist/$',   BlackListCreate.as_view()  , name=BlackListCreate.name),  # 블랙리스트 출금주소 등록
    url(r'^v1/blacklist-withdraw-addr/list/$',     BlackList.as_view()    , name=BlackList.name),    # 블랙리스트 출금주소 목록조회
    url(r'^v1/blacklist-withdraw-addr/history/$',  BlackListHistory.as_view() , name=BlackListHistory.name), # 블랙리스트 출금주소 내역조회
    url(r'^v1/blacklist-device/regist/$', BlackListCreate.as_view(), name=BlackListCreate.name),  # 블랙리스트 단말기 등록
    url(r'^v1/blacklist-device/list/$', BlackList.as_view(), name=BlackList.name),  # 블랙리스트 단말기 목록조회
    url(r'^v1/blacklist-device/history/$', BlackListHistory.as_view(), name=BlackListHistory.name),  # 블랙리스트 단말기제한 내역조회

    url(r'^v1/blacklist-withdraw-proc/regist/$',   BlackListWithdrawProcCreate.as_view()    , name=BlackListWithdrawProcCreate.name),   # 블랙리스트 출금/취소
    url(r'^v1/blacklist-withdraw-proc/list/$',     BlackListWithdrawProcList.as_view()    , name=BlackListWithdrawProcList.name),       # 블랙리스트 출금요청 목록조회
    url(r'^v1/blacklist-withdraw-proc/history/$',  BlackListWithdrawProcHistory.as_view()    , name=BlackListWithdrawProcHistory.name), # 블랙리스트 출금 상세 내역조회
]
