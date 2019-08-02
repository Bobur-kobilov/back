from . import *
from bcoffice.utils.coin_util import CoinUtil
from rest_framework.exceptions import * 
from datetime import date
from dateutil.relativedelta import relativedelta
class DailyTotalSalesList(APIView):
    """
    일자별 매출액
    """
    name = "daliy_deposit_withdraw"
    permission_classes = [DailyTotalSalesPermission]
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self, *args, **kwargs):
        date = kwargs.get('date', None)
        start_date = date + ' 00:00:00'
        end_date = date + ' 23:59:59'

        queryset = Trades.objects.using('exchange').values('currency') \
            .annotate(ask_volume=Sum('volume')) \
            .annotate(bid_volume=Sum('funds')) \
            .annotate(fee_ask=Sum('bid_fee')) \
            .annotate(fee_bid=Sum('ask_fee')) \
            .filter(created_at__range=(start_date, end_date)) \
            .order_by('currency')

        # 수수료 제외 (m2)
        m2 = kwargs.get('m2', None)
        if m2 is not None:
            queryset = queryset.filter(Q(ask_member_id__in=m2) | Q(bid_member_id__in=m2))

        return queryset

    def get_referral_fee_queryset(self, *args, **kwargs):
        date = kwargs.get('date', None)
        start_date = date + ' 00:00:00'
        end_date = date + ' 23:59:59'

        queryset = ReferralFeeHistories.objects.using('exchange').values('currency') \
            .annotate(amount=Sum('amount')) \
            .filter(created_at__range=(start_date, end_date)) \
            .order_by('currency')
        return queryset

    def get_process(self, start_date, end_date):
        result_data = []
        mongodb = BCOfficeMongoDB(__setting_name__='trend', collection=TBL_BCOFFICE_DAILY_TOTAL_SALES)
        #check Mongo connection
        if mongodb is None:
            return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00034), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        while True:
            # GET MONGO DB
            params = {}
            params['body.date'] = start_date
            mongo_result = (mongodb.collection.find(params).sort('_id', pymongo.DESCENDING))

            # MONGO DB에 없는 경우 (MYSQL에서 추출 값을 MONGO DB에 저장 후 표기)
            daily_data = []
            dbCheck = mongo_result.count()
            dataExist = 0
            # if dbCheck>0:
            #     dataExist = len(mongo_result[0]['body']['results'])
            if dataExist == 0:
                # 일일값 계산 (mysql - trades)
                trades_queryset = self.get_queryset(date=start_date)
                for trades in trades_queryset:
                    trades['bid_currency'] = self.currencyId(self.getBidAskCoin(market_id=trades['currency'], trade_type='bid'))
                    trades['ask_currency'] = self.currencyId(self.getBidAskCoin(market_id=trades['currency'], trade_type='ask'))

                    trades_data = {}
                    trades_data['currency'] = trades['bid_currency']
                    trades_data['volume'] = float(trades['bid_volume'])
                    trades_data['usd_volume'] = ValuationAssetsUtil.get_valuation_for_dollar(trades_data['currency'], trades_data['volume'])
                    trades_data['fee'] = float(trades['fee_bid'])
                    trades_data['usd_fee'] = ValuationAssetsUtil.get_valuation_for_dollar(trades_data['currency'], trades_data['fee'])
                    daily_data = CoinUtil.addValue(daily_data, trades_data)

                    trades_data = {}
                    trades_data['currency'] = trades['ask_currency']
                    trades_data['volume'] = float(trades['ask_volume'])
                    trades_data['usd_volume'] = ValuationAssetsUtil.get_valuation_for_dollar(trades_data['currency'], trades_data['volume'])
                    trades_data['fee']= float(trades['fee_ask'])
                    trades_data['usd_fee'] = ValuationAssetsUtil.get_valuation_for_dollar(trades_data['currency'], trades_data['fee'])
                    daily_data = CoinUtil.addValue(daily_data, trades_data)
                # 수수료 제외 항목 (m2)
                m2_list = settings.M2_MEMBER_ID_LIST
                trades_m2_queryset = self.get_queryset(date=start_date, m2=m2_list)

                for m2_trades in trades_m2_queryset:
                    m2_trades['bid_currency'] = self.currencyId(self.getBidAskCoin(market_id=m2_trades['currency'], trade_type='bid'))
                    m2_trades['ask_currency'] = self.currencyId(self.getBidAskCoin(market_id=m2_trades['currency'], trade_type='ask'))

                    trades_except_data = {}
                    trades_except_data['currency'] = m2_trades['bid_currency']
                    trades_except_data['except_fee'] = float(m2_trades['fee_bid'])
                    trades_except_data['except_usd_fee'] = ValuationAssetsUtil.get_valuation_for_dollar(trades_except_data['currency'], trades_except_data['except_fee'])
                    daily_data = CoinUtil.addValue(daily_data, trades_except_data)

                    trades_except_data = {}
                    trades_except_data['currency'] = m2_trades['ask_currency']
                    trades_except_data['except_fee'] = float(m2_trades['fee_ask'])
                    trades_except_data['except_usd_fee'] = ValuationAssetsUtil.get_valuation_for_dollar(trades_except_data['currency'], trades_except_data['except_fee'])
                    daily_data = CoinUtil.addValue(daily_data, trades_except_data)
                # 수수료 제외항목 (추천인 수수료)
                referral_fee_queryset = self.get_referral_fee_queryset(date=start_date)
                for referral_fee in referral_fee_queryset:
                    referral_fee_data = {}
                    referral_fee_data['currency'] = referral_fee['currency']
                    referral_fee_data['except_fee'] = float(referral_fee['amount'])
                    referral_fee_data['except_usd_fee'] = ValuationAssetsUtil.get_valuation_for_dollar(referral_fee_data['currency'], referral_fee_data['except_fee'])
                    daily_data = CoinUtil.addValue(daily_data, referral_fee_data)
                # 결과값 MONGO DB 저장 (오늘이전날짜까지)
                if datetime.strptime(start_date, '%Y-%m-%d') < datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d'):
                    body = {
                        "date": start_date
                        , "results": daily_data
                    }
                    mongodb.insert_db(body)

                # result_data에 daily_data 추가
                result_data = CoinUtil.mergeListData(result_data, daily_data)
            # MONGO DB에 있는 경우 (MONGO DB 값 그대로 누적)
            else:
                for obj in mongo_result:
                    daily_data = obj['body']['results']
                # result_data에 daily_data 추가
                result_data = CoinUtil.mergeListData(result_data, daily_data)
            # 마감일까지 실행하면 종료
            if start_date == end_date:
                break
            else:
                start_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

        mongodb.close()
        return result_data
    def get(self, request, *args, **kwargs):
        checkChart  = request.query_params.get('data',None);
        if checkChart == 'chart':
            # result_data = self.chartData()
            result_data = ''
            return Response(data={'results':result_data})
        else:    
            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('end_date', None)  
            # assert start_date is not None and end_date is not None
            if start_date is None and end_date is None:
                return Response(data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00033), status=status.HTTP_400_BAD_REQUEST)

            result_data = self.get_process(start_date, end_date)
            return Response(data={'results': result_data})
    
    def chartData (self): 
        dates = CoinUtil.get_date()
        result_data_1 = self.get_process(dates[0]['month_1']['start_date'],dates[0]['month_1']['end_date'])
        result_data_2 = self.get_process(dates[0]['month_2']['start_date'],dates[0]['month_2']['end_date'])
        result_data_3 = self.get_process(dates[0]['month_3']['start_date'],dates[0]['month_3']['end_date'])
        
        usd_fee_month_1 = 0.0
        usd_fee_month_2 = 0.0
        usd_fee_month_3 = 0.0

        fee_month1 = 0.0
        fee_month2 = 0.0
        fee_month3 = 0.0
        

        for data in result_data_1:
            usd_fee_month_1 += data['usd_fee']
            fee_month1 += data['fee']
        for data in result_data_2:
            usd_fee_month_2 +=data['usd_fee']
            fee_month2 +=data['fee']
        for data in result_data_3:
            usd_fee_month_3 += data['usd_fee']
            fee_month3 +=data['fee']            
  

        data=[
        [   {
            "name":dates[0]['month_3']['month_name'],
            "value":usd_fee_month_3
            },
            {
            "name":dates[0]['month_2']['month_name'],
            "value":usd_fee_month_2
            },
            {
            "name":dates[0]['month_1']['month_name'],
            "value":usd_fee_month_1
            }
        ],
        [
            {
            "name":dates[0]['month_3']['month_name'],
            "value":fee_month3
            },
            {
            "name":dates[0]['month_2']['month_name'],
            "value":fee_month2
            },
            {
            "name":dates[0]['month_1']['month_name'],
            "value":fee_month1
            }
        ],
        [
            {
                "name":"BTC",
                "value":100
            },
            {
                "name":"ETH",
                "value":120
            },
            {
                "name":"Synco",
                "value":150
            }
        ]
        ]
        return data
    
    # 코인명 가져오기
    def getBidAskCoin(self, market_id=None, trade_type=None):
        for market in settings.MARKET_LIST:
            if market['market_id'] == market_id:
                return market[trade_type]['currency']
        return '-'

    def currencyId(self, currency_name=None):
        for currency in settings.CURRENCY_LIST:
            if currency['code'].lower() == currency_name.lower():
                return currency['id']
        return -1

    def get_currency_name_by_id(self, currency_id):
        assert currency_id is not None

        for currency in settings.CURRENCY_LIST:
            if currency['id'] == currency_id:
                return currency['code'].upper()
        return '알 수 없는 코인(ID:{})'.format(currency['id'])

    def delete(self, request, *args, **kwargs):
        mongodb = BCOfficeMongoDB(__setting_name__='trend', collection=TBL_BCOFFICE_DAILY_TOTAL_SALES)
        mongodb.remove_db(init=True)
        mongodb.close()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DailyTotalSalesCSVRenderer(CSVRenderer):
    header = ['currency', 'volume', 'usd_volume', 'fee', 'usd_fee', 'except_fee', 'except_usd_fee', 'net', 'usd_net']
    labels = {
        'currency': 'currency',
        'volume': 'volume',
        'usd_volume': 'volume(usd)',
        'fee': 'fee',
        'usd_fee': 'fee(usd)',
        'except_fee': 'except_fee',
        'except_usd_fee': 'except_fee(usd)',
        'net': 'net',
        'usd_net': 'net(usd)'
    }


class DailyTotalSalesCSVUSDRenderer(CSVRenderer):
    header = ['currency', 'usd_volume', 'usd_fee', 'except_usd_fee', 'usd_net']
    labels = {
        'currency': 'currency',        
        'usd_volume': 'volume(usd)',        
        'usd_fee': 'fee(usd)',        
        'except_usd_fee': 'except_fee(usd)',        
        'usd_net': 'net(usd)'
    }


class DailyTotalSalesListCSV(DailyTotalSalesList):
    """
    일자별 매출액 CSV
    """
    name = "daliy_total_sales_csv"
    permission_classes = ()
    authentication_classes = () 
    renderer_classes = (DailyTotalSalesCSVRenderer, )

    def get(self, request, *args, **kwargs):
        """일자별 매출액 CSV 반환    

        Args:
            start_date (str, YYYY-MM-DD)
            end_date (str, YYYY-MM-DD)
            api_key (str)
            csv_file_name (str, optional): filename except .csv

        Returns:
            csv file

        Examples:
            http://localhost:8000/v1/coin-account/daily-total-sales-csv/?start_date=2018-11-01&end_date=2019-01-16&api_key=kBzo2P6qEDymHbACR9Q1L1ZKaDuYIYos

        """        
        if settings.STATS_API_KEY != request.query_params.get('api_key', ''):            
            return Response({'error': 'API key is not valid.'}, status=status.HTTP_401_UNAUTHORIZED)

        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)        
        assert start_date is not None and end_date is not None
        
        result_data = self.get_process(start_date, end_date)
        final_data = self.calc_data(result_data)
                
        response = Response(final_data)
        csv_file_name = request.query_params.get('csv_file_name', self.get_csv_file_name_default(start_date, end_date))
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(csv_file_name)

        return response
    
    def get_csv_file_name_default(self, start_date, end_date):        
        if start_date == end_date:
            return 'total_trades_{}'.format(start_date.replace('-', ''))
        else:
            return 'total_trades_{}-{}'.format(start_date.replace('-', ''), end_date.replace('-', ''))

    def calc_data(self, data):
        total = {
            'usd_volume': 0.0,
            'usd_fee': 0.0,
            'except_usd_fee': 0.0
        }

        for row in data:
            row['currency'] = self.get_currency_name_by_id(row['currency'])
            row['net'] = row['fee'] - row['except_fee']
            row['usd_net'] = row['usd_fee'] - row['except_usd_fee']

            # 전체 합계 누적
            for column in ['usd_volume', 'usd_fee', 'except_usd_fee']:
                total[column] += row[column]
        
        # 전체 합계행 추가
        data.append({
            'currency': 'total',
            'volume': None,
            'usd_volume': total['usd_volume'], 
            'fee': None, 
            'usd_fee': total['usd_fee'], 
            'except_fee': None, 
            'except_usd_fee': total['except_usd_fee'], 
            'net': None, 
            'usd_net' : total['usd_fee'] - total['except_usd_fee']            
        })

        return data


class DailyTotalSalesListCSVUSD(DailyTotalSalesListCSV):
    """
    일자별 매출액 CSV USD only
    """
    name = "daliy_total_sales_csv_usd"    
    renderer_classes = (DailyTotalSalesCSVUSDRenderer, )