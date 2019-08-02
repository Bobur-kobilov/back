from . import *

def get_conditional_query(field_name = None, date_format = None):
    conditional_query = ''
    field_types       = ['origin_volume', 'volume',  'funds', 'amount']

    if field_name == 'count':
        conditional_query = 'count(' + date_format + ')'
    elif field_name in field_types:
        conditional_query = 'sum(' + field_name + ')'
    else:
        # 일치하는 값이 없습니다
        return Response(data = ResponseMessage.MESSAGE_ERR00008, status=status.HTTP_400_BAD_REQUEST)

    return conditional_query

# serial data query
def trend_list_query(self, table_name = None, field_name = None, date_format = None, start_date = None, end_date = None):

    query = ''

    conditional_query = get_conditional_query(field_name, date_format)

    query = """
        SELECT
            {0} as result,
            {1} as id 
        FROM
            {2}
        WHERE
            {2}.created_at BETWEEN '{3}' AND '{4}'
        group by {1};
    """.format(conditional_query, date_format, table_name, start_date, end_date)

    print("================trend_list_query===========")
    print(query)
    return query


# serial data list
class TrendList(ListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "trend-list"
    # permission_classes = [TrendPermission]
    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    filter_fields   = ['id']
    search_fields   = []
    ordering_fields = ['created_at']
    ordering        = ['-created_at']
    pagination_class = StandardPagination
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------

    def get_queryset(self):
        return

    def list(self, request, *args, **kwargs):

        # 트랜드 검색 유형 (table_name__field_name)
        trend_type     = request.query_params.get('trend_type', None)
        trend_type     = trend_type.split('__')
        table_name     = trend_type[0]
        field_name     = trend_type[1]

        # 테이블명 범위 확인하기
        tables_types   = ['orders', 'trades',  'deposits', 'withdraws', 'signup_histories', 'members']
        if not table_name in tables_types:
            return Response(data = ResponseMessage.MESSAGE_ERR00008, status=status.HTTP_400_BAD_REQUEST)

        # 조회 기간 검색 유형 (day, hour, minute)
        lookup_types   = ['day', 'hour', 'minute']
        lookup_name    = request.query_params.get('lookup_name' , None)

        # date_format 생성
        if lookup_name is not None and lookup_name in lookup_types:
            if lookup_name == 'day':
                date_type = "date_format(created_at, '%%Y-%%m-%%d')"
            elif lookup_name == 'hour':
                date_type = "date_format(created_at, '%%Y-%%m-%%d %%H')"
            elif lookup_name == 'minute':
                date_type = "date_format(created_at, '%%Y-%%m-%%d %%H:%%i')"
            else:
                # 일치하는 값이 없습니다
                return Response(data = ResponseMessage.MESSAGE_ERR00008, status=status.HTTP_400_BAD_REQUEST)

        # 조회 기간 선택
        today = datetime.today().strftime('%Y-%m-%d')

        start_date = request.query_params.get('start_date' , today)
        start_date = set_time_zone(start_date, timezone('UTC'), 'start')

        end_date = request.query_params.get('end_date' , today)
        end_date = set_time_zone(end_date, timezone('UTC'), 'end')

        query = trend_list_query(self, table_name, field_name, date_type, start_date, end_date)

        # queryset 얻기
        # __db__ = 'exchange'
        # cursor = connections[__db__].cursor()
        # cursor.execute(query)
        # queryset = cursor.fetchall()

        queryset = Orders.objects.using('exchange').raw(query)

        # 결과값 생성

        result_data = []
        for obj in queryset:
            result_data.append({"created_at": obj.id, "result": obj.result})

        return Response(data = result_data)