from . import *

# TODO: 프론트도 api 제거
class TagCoinList(APIView):
    """
    태그가 필요한 코인 목록
    """
    name = "tag-coin-list"

    def get(self, request, *args, **kwargs):
        data = []
        permission_classes = [TagCoinListPermission]

        for item in settings.TAG_COINS:
            currency = ValuationAssetsUtil.get_currency_item_for_code(item)

            if currency is not None:
                data.append( currency )

        return Response(data=data, status=status.HTTP_200_OK)