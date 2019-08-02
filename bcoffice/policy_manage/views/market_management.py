from . import *
from django.core.cache  import cache

class MarketManagement(APIView):
    # 마켓별 매도가격 제한
    name = "market_management"
    permission_classes = [MarketManagementPermission]
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        # 마켓 추가
        market_list = []
        for market in settings.MARKET_LIST:
            market_list.append({
                'id': market['id'],
                'name': market['name'],
                'bid': market['bid']['currency'],
                'lowest_order_price': cache.get('bcg:{0}:lowest_order_price'.format(market['id']))
            })
        cache.close()
        return Response(data={'results': market_list})

    def post(self, request, *args, **kwargs):
        market_id = request.data.get('market_id')
        lowest_order_price = request.data.get('lowest_order_price')

        cache.set('bcg:{0}:lowest_order_price'.format(market_id), lowest_order_price, timeout=None)
        cache.close()
        return Response(status=status.HTTP_200_OK)