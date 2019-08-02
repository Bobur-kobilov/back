from django.conf import settings
from django.conf.urls           import url
from django.conf.urls.static    import static
from .views import *

urlpatterns = [
    url(r'^v1/board/faq/$'                                      , FaqList.as_view()                 , name=FaqList.name)                    # FAQ 목록
    , url(r'^v1/board/faq-create/$'                             , FaqCreate.as_view()               , name=FaqCreate.name)                  # FAQ 작성
    , url(r'^v1/board/faq/(?P<pk>[0-9]+)/$'                     , FaqDetailUpdateDestroy.as_view()  , name=FaqDetailUpdateDestroy.name)     # FAQ 상세 조회, 수정, 제거
    , url(r'^v1/board/faq-category/$'                           , FaqCategoryList.as_view()         , name=FaqCategoryList.name)            # FAQ 카테고리 목록
        
    , url(r'^v1/board/notice-attach-create/$'                   , NoticeAttachCreate.as_view()      , name=NoticeAttachCreate.name)         # 공지사항 첨부파일 작성
    , url(r'^v1/board/notice-attach-delete/$'                   , NoticeAttachDestroy.as_view()     , name=NoticeAttachDestroy.name)        # 공지사항 첨부파일 제거
    , url(r'^v1/board/notice/$'                                 , NoticeList.as_view()              , name=NoticeList.name)                 # 공지사항 목록
    , url(r'^v1/board/notice-create/$'                          , NoticeCreate.as_view()            , name=NoticeCreate.name)               # 공지사항 작성
    , url(r'^v1/board/notice/(?P<pk>[0-9]+)/$'              , NoticeDetailUpdateDestroy.as_view()   , name=NoticeDetailUpdateDestroy.name)  # 공지사항 상세 조회, 수정, 제거

    , url(r'^v1/board/daily-attach-create/$'                    , DailyNewsAttachCreate.as_view()   , name=DailyNewsAttachCreate.name)      # Daily뉴스 첨부파일 작성
    , url(r'^v1/board/daily-attach-delete/$'                    , DailyNewsAttachDestroy.as_view()  , name=DailyNewsAttachDestroy.name)     # Daily뉴스 첨부파일 제거
    , url(r'^v1/board/daily/$'                                  , DailyNewsList.as_view()           , name=DailyNewsList.name)              # Daily뉴스 목록
    , url(r'^v1/board/daily-create/$'                           , DailyNewsCreate.as_view()         , name=DailyNewsCreate.name)            # Daily뉴스 작성
    , url(r'^v1/board/daily/(?P<pk>[0-9]+)/$'               , DailyNewsDetailUpdateDestroy.as_view(), name=DailyNewsDetailUpdateDestroy.name)   # Daily뉴스 상세 조회, 수정, 제거

    , url(r'^v1/board/coinguide-attach-create/$'                , CoinGuideAttachCreate.as_view()   , name=CoinGuideAttachCreate.name)      # 코인가이드 로고 작성
    , url(r'^v1/board/coinguide-attach-delete/$'                , CoinGuideAttachDestroy.as_view()  , name=CoinGuideAttachDestroy.name)     # 코인가이드 로고 제거
    , url(r'^v1/board/coinguide/$'                              , CoinGuideList.as_view()           , name=CoinGuideList.name)              # 코인가이드 목록
    , url(r'^v1/board/coinguide-create/$'                       , CoinGuideCreate.as_view()         , name=CoinGuideCreate.name)            # 코인가이드 작성
    , url(r'^v1/board/coinguide-link-create/$'              , CoinGuideUsefulLinkCreate.as_view()   , name=CoinGuideUsefulLinkCreate.name)  # 코인가이드 유용한링크 작성
    , url(r'^v1/board/coinguide-link-delete/$'              , CoinGuideUsefulLinkDestroy.as_view()  , name=CoinGuideUsefulLinkDestroy.name) # 코인가이드 유용한링크 제거
    , url(r'^v1/board/coinguide/(?P<pk>[0-9]+)/$'           , CoinGuideDetailUpdateDestroy.as_view(), name=CoinGuideDetailUpdateDestroy.name)   # 코인가이드 상세 조회, 수정, 제거
    
    , url(r'^v1/image-upload/$'                                 , ImageUpload.as_view()             , name=ImageUpload.name )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)      # 이미지경로 -> (localhost + 경로)로 호출 가능
