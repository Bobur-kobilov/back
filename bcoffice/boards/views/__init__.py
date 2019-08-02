import uuid, socket, re
from django.conf                import settings
from django.db.models           import F ,Q
from django.shortcuts           import render
from django.db.models.sql.query import RawQuery
from django.db.models.query     import RawQuerySet

import boto3
from boto3.s3.transfer import S3Transfer

from rest_framework.generics    import (
    CreateAPIView
    , ListAPIView
    , RetrieveUpdateDestroyAPIView
    , DestroyAPIView
)
from rest_framework             import status
from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.parsers     import MultiPartParser, FormParser

from boards.models import *
from boards.serializers import *
from boards.permissions import *

from bcoffice.generics          import RawQueryListAPIView, RawQuerySyntax
from bcoffice.pagination        import RawQuerySetPagination, StandardPagination
from bcoffice.message           import ResponseMessage
from bcoffice.utils             import string_utils
from bcoffice.utils.send_utils  import SendMail, SendSMS
from bcoffice.utils.date_util   import set_time_zone

from becoin.model               import Members

from datetime                   import datetime
from pytz import timezone

from .faq_list                          import FaqList
from .faq_create                        import FaqCreate
from .faq_detail_update_destroy         import FaqDetailUpdateDestroy
from .faq_category_list                 import FaqCategoryList
from .notice_list                       import NoticeList
from .notice_create                     import NoticeCreate
from .notice_detail_update_destroy      import NoticeDetailUpdateDestroy
from .notice_attach_create              import NoticeAttachCreate
from .notice_attach_destroy             import NoticeAttachDestroy
from .dailynews_list                    import DailyNewsList
from .dailynews_create                  import DailyNewsCreate
from .dailynews_detail_update_destroy   import DailyNewsDetailUpdateDestroy
from .dailynews_attach_create           import DailyNewsAttachCreate
from .dailynews_attach_destroy          import DailyNewsAttachDestroy
from .coinguide_list                    import CoinGuideList
from .coinguide_create                  import CoinGuideCreate
from .coinguide_detail_update_destroy   import CoinGuideDetailUpdateDestroy
from .coinguide_attach_create           import CoinGuideAttachCreate
from .coinguide_attach_destroy          import CoinGuideAttachDestroy
from .coinguide_usefullink_create       import CoinGuideUsefulLinkCreate
from .coinguide_usefullink_destroy      import CoinGuideUsefulLinkDestroy
from .image_upload                      import ImageUpload