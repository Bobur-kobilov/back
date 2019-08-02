from django.shortcuts           import render
from rest_framework.generics    import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response    import Response
from rest_framework             import status

from manager_memo.serializers   import ManagerMemoSerializer, ManagerMemoCreateSerializer
from manager_memo.models        import ManagerMemo
from bcoffice.message           import ResponseMessage
from manager_memo.permissions   import (
    ManagerMemoListPermission
    , ManagerMemoDestroyPermission
)

from .manager_memo_list         import ManagerMemoList
from .manager_memo_create       import ManagerMemoCreate
from .manager_memo_destroy      import ManagerMemoDestory