import requests
from django.conf import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta

class CoinUtil :
    def getCoinBalance(coin, wallet_address):
        currency = None

        for item in settings.CURRENCY_LIST:
            if int(coin) == item['id']:
                currency = item['code'].upper()
                break

        try :
            if settings.IS_TEST_NET:
                api = settings.TEST_NET_COIN_API[currency].format(wallet_address)
            else :
                api = settings.MAIN_NET_COIN_API[currency].format(wallet_address)

            rs = requests.get(api)
            data = rs.json()

            if currency == 'BTC' :
                if settings.IS_TEST_NET:
                    balance = data['balance']
                else :
                    balance = data['final_balance']

            elif currency == 'QTUM' :
                balance = data['balance']

            elif currency == 'BCH' :
                if settings.IS_TEST_NET:
                    balance = data['balance']
                else :
                    balance = data

            elif currency == 'ADA':
                balance = data['Right']['caBalanace']['getCoin']

        except :
            balance = None

        return balance
    #Merge two lists    
    def mergeListData(a_list=[],b_list=[],type=None):
        # 코인 목록
        currency_list = []
        for obj in a_list:
            currency_list.append(obj['currency'])
        for obj in b_list:
            currency_list.append(obj['currency'])
        currency_list = list(set(currency_list))  # 중복제거
        currency_list.sort(reverse=False)  # 정렬

        merge_list = []
        for currency in currency_list:
            is_append = False
            append_data = {  # 코인별 값
                'currency': currency
                , 'volume': 0
                , 'usd_volume': 0
                , 'fee': 0
                , 'usd_fee': 0
                , 'except_fee': 0
                , 'except_usd_fee': 0
            }

            for obj in a_list:
                if obj['currency'] == currency:
                    for key in obj:
                        if key != 'currency':
                            append_data[key] += float(obj[key] if obj[key] is not None else 0)
                    is_append = True
                    break
            for obj in b_list:
                if obj['currency'] == currency:
                    for key in obj:
                        if key != 'currency':
                            append_data[key] += float(obj[key] if obj[key] is not None else 0)
                    is_append = True
                    break

            if is_append:
                merge_list.append(append_data)

        return merge_list
        
      # 리스트 내부 값 합치기
    def addValue(target_list=[],add_obj=[]):
        if len(target_list) > 0:
            for obj in target_list:
                if obj['currency'] == add_obj['currency']:
                    for field in add_obj:
                        if field != 'currency':
                            try:
                                obj[field] += add_obj[field]
                            except:
                                obj[field] = add_obj[field]
                    return target_list
            target_list.append(add_obj)
        else:
            target_list.append(add_obj)
        return target_list
    
    def get_date ():
        today = datetime.today()
        #---------MONTH 1----------------
        current_month = datetime(today.year, today.month, 1) 
        start_date = current_month
        end_date = (current_month + relativedelta(months=1)- relativedelta(days=1))
        month_name_1 = current_month.strftime('%B')

        end_date = end_date.strftime('%Y-%m-%d')
        start_date = start_date.strftime('%Y-%m-%d')
        

        #---------MONTH 2------------------    
        second_month_start = current_month - relativedelta(months=1)
        second_month_end = current_month - relativedelta(days=1)

        month_name_2 = second_month_start.strftime('%B')
        second_month_start = second_month_start.strftime('%Y-%m-%d')
        second_month_end = second_month_end.strftime('%Y-%m-%d')
      

        #--------MONTH 3 -------------
        third_month_start = current_month - relativedelta(months=2)
        third_month_end = (current_month - relativedelta(months=1)-relativedelta(days=1))

        third_month_name = third_month_start.strftime('%B')
        third_month_start = third_month_start.strftime('%Y-%m-%d')
        third_month_end = third_month_end.strftime('%Y-%m-%d')

        result = [
            {
            "month_1":{
                "start_date":start_date,
                "end_date":end_date,
                "month_name":month_name_1
            },
            "month_2":{
                "start_date":second_month_start,
                "end_date":second_month_end,
                "month_name":month_name_2
            },
            "month_3":{
                "start_date":third_month_start,
                "end_date":third_month_end,
                "month_name":third_month_name
            }
            }
        ]
        return result

