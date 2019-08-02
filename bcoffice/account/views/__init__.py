from datetime import datetime

from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib import auth
from django.dispatch import receiver

import uuid

from account.models import ( User
                    , Auth
                    , DepartmentType
                    , DepartmentRank
                    , DepartmentDuty
                    , STATUS )
from account.serializers import *
from account.permissions import *
from bcoffice.generics import RawQueryListAPIView
from bcoffice.pagination import RawQuerySetPagination
from bcoffice.message import ResponseMessage

from .logout                import user_logout
from .user_list             import UserList
from .user_detail           import UserDetail
from .user_create           import UserCreate
from .admin_user_create     import AdminUserCreate
from .user_update           import UserUpdate
from .user_personal_update  import UserPersonalUpdate
from .user_password_update  import UserPasswordUpdate
from .user_personal_password_update import UserPersonalPasswordUpdate
from .auth_list             import AuthList
from .auth_modified         import AuthModified
from .dept_create           import DeptCreateList
from .dept_detail           import DeptDetail
from .dept_rank_create      import DeptRankCreateList
from .dept_rank_datail      import DeptRankDetail
from .dept_duty_create      import DeptDutyCreateList
from .dept_duty_detail      import DeptDutyDetail