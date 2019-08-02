from django.conf.urls   import url
from .views           import *

urlpatterns = [
    url(r'^v1/manager-memo/(?P<target_id>[0-9]+)/$' , ManagerMemoList.as_view()     , name=ManagerMemoList.name),   # 관리자 메모 목록
    url(r'^v1/manager-memo/create/$'                , ManagerMemoCreate.as_view()   , name=ManagerMemoCreate.name), # 관리자 메모 작성
    url(r'^v1/manager-memo/delete/(?P<pk>[0-9]+)/$' , ManagerMemoDestory.as_view()  , name=ManagerMemoDestory.name)  # 관리자 메모 삭제
]
