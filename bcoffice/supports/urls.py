from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^v1/support/question/$',                          QuestionList.as_view(),                 name=QuestionList.name),                    # 1:1 문의 내역 조회
    url(r'^v1/support/question-create/$',                   QuestionCreate.as_view(),               name=QuestionCreate.name),                  # 1:1 문의 내역 작성
    url(r'^v1/support/question-type/$',                     QuestionTypeList.as_view(),             name=QuestionTypeList.name),                # 1:1 문의 카테고리
    url(r'^v1/support/question/(?P<pk>[0-9]+)/$',           QuestionDetailUpdate.as_view(),         name=QuestionDetailUpdate.name),            # 1:1 문의 내역 상세조회 / 답변 처리상태 변경
    url(r'^v1/support/question-mod/(?P<pk>[0-9]+)/$',       QuestionUpdateDestroy.as_view(),        name=QuestionUpdateDestroy.name),           # 1:1 문의 내역 수정, 삭제
    url(r'^v1/support/answer/(?P<target>[0-9]+)/$',         AnswerDetailUpdateDestroy.as_view(),    name=AnswerDetailUpdateDestroy.name),       # 1:1 답변 내역 상세조회, 수정, 삭제

    url(r'^v1/support/send-mail/$',                         SendMailView.as_view(),                     name=SendMailView.name),                        # 메일 보내기 및 Log 남기기
    url(r'^v1/support/send-sms/$',                          SendSMSView.as_view(),                     name=SendSMSView.name),                        # 메일 보내기 및 Log 남기기

    url(r'^v1/support/history/$', SupportHistory.as_view(), name=SupportHistory.name),  # 고객지원 내역
]