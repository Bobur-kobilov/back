from django.conf.urls   import url
from .views           import *

urlpatterns = [
    url(r'^v1/system/coin-block-height/$'           , CoinBlockHeight.as_view()          , name=MtsVersionList.name),
    url(r'^v1/system/coin-balance/$'                , CoinBlanace.as_view()              , name=CoinBlanace.name),
    url(r'^v1/system/hot-wallet-balance/$'          , HotWalletBlanace.as_view()         , name=HotWalletBlanace.name),

    url(r'^v1/system/mts-version/$'                 , MtsVersionList.as_view()         , name=CoinBlockHeight.name),
    url(r'^v1/system/mts-version/item/$'            , MtsVersionItem.as_view()          , name=MtsVersionItem.name),
    url(r'^v1/system/mts-version/(?P<pk>[0-9]+)/$'  , MtsVersionUpdateDelete.as_view()  , name=MtsVersionUpdateDelete.name),
    url(r'^v1/system/mts-version/history/$'         , MtsVersionHistory.as_view()       , name=MtsVersionHistory.name),
]
