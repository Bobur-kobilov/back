import json

from django.conf import settings
from django.core.cache  import cache

"""
평가자산 유틸
"""
class ValuationAssetsUtil:
    # Currency 코드로 Currency 객체를 탐색해주는 유틸
    def get_currency_item(currency = -1):
        item = None

        for obj in settings.CURRENCY_LIST:
            if obj['id'] == currency:
                item = obj
                break

        return item

    # Currency 코드로 Currency 객체를 탐색해주는 유틸
    def get_currency_item_for_code(currency = ""):
        item = None

        for obj in settings.CURRENCY_LIST:
            if obj['code'].lower() == currency.lower():
                item = obj
                break

        return item


    # 코인환전
    # from_currency : 현재 코인의 currency
    # to_currency : 환전을 원하는 코인의 currency
    # count : 코인 수량
    def coin_exchange(from_currency = -1, to_currency = -1, count = -1):
        from_coin = ValuationAssetsUtil.get_currency_item(from_currency)['code']
        to_coin = ValuationAssetsUtil.get_currency_item(to_currency)['code']

        base_data = cache.get("bcg:" + from_coin + to_coin +":ticker")

        if base_data is not None :
            base = float(json.loads(base_data)['last'])
        else :
            base = 0

        return base * count

    # 코인의 달러환율을 평가하는 메서드
    # currency : 평가를 원하는 코인의 id 값
    # count : 갯수
    def get_valuation_for_dollar(currency = -1, count = -1):
        item = ValuationAssetsUtil.get_currency_item(currency)

        if item is None:
            return None

        try :
            price = float(json.loads(cache.get("bcg_ext:ticker_coinmarket:" + item['eval_currency'].upper() + "USD"))[0])
        except :
            price = 0

        if count is None:
            count = 0

        if item['bid_currency'] is True :
            return price * count
        else:
            base = ValuationAssetsUtil.coin_exchange(item['id'], ValuationAssetsUtil.get_currency_item_for_code("btc")['id'], count)
            return price * base

    # 기준코인 환산
    # currency : 환산을 원하는 코인의 id 값
    # count : 갯수
    def get_base_coin_exchange(currency = -1, count = -1):
        item = ValuationAssetsUtil.get_currency_item(currency)
        if item is None:
            return None

        if item['bid_currency'] is True :
            return count
        else:
            if item['id'] is not None and item['eval_currency'] is not 'none':
                return ValuationAssetsUtil.coin_exchange(item['id'], ValuationAssetsUtil.get_currency_item_for_code(item['eval_currency'])['id'], count )