from rest_framework.generics    import ListAPIView
from rest_framework.views       import APIView

from bcoffice.utils             import string_utils

from django.db.models.sql.query import RawQuery

class RawQueryListAPIView(ListAPIView):
    having_fields = []
    group_fields = []
    ordering = []
    filter_fields = []
    search_fields = []

    # 쿼리셋가져오기
    # model: 쿼리에 사용될 모델 객체
    # query : RawQuery에 사용될 질의문
    # __db__ : 멀티 DB에서 쿼리문을 전송시킬 DB의 설정 아이디값(기본값: default)
    # relate_operator : WHERE 절의 조건을 AND 혹은 OR로 이어붙일지 결정하는 파라미터(기본값: AND)
    def get_queryset(self, model, query, __db__ = 'default', relate_operator = 'AND'):
        # 혹시 Having 쿼리가 필요한 경우 적용한다
        having_query = self.filter_operation( self.having_fields )

        # 일치 검색이 필요한 경우 적용하기 위해 쿼리를 만든다.
        condition_query = self.filter_operation( self.filter_fields )

        # 정렬 쿼리 적용
        order_query = self.get_ordering_filter(self.ordering)

        # 정렬 쿼리 적용
        group_query = self.get_grouping_filter()
        
        # Ordering 처리를 위한 정렬조건 추가
        # request 파라미터에 ordering 조건이 있는지 확인한다
        if self.request.query_params.get("ordering", False):
            order_query = self.get_ordering_filter(self.request.query_params["ordering"].split(","))

        # LIKE 검색을 위한 검색 조건 추가
        search_query = self.get_search_filter()

        if len(condition_query) > 0 :
            condition_query = " WHERE " + condition_query
        
        if len(search_query) > 0 :
            if len(condition_query) > 0 :
                    condition_query += " " + relate_operator + " " + search_query
            else :
                condition_query = " WHERE " + search_query

        if len(having_query) > 0 :
            having_query = " HAVING " + having_query

        # 쿼리 정리
        query = query + condition_query + group_query + having_query + order_query
        
        # 쿼리셋을 만든다.
        queryset = model.objects.using(__db__).raw(query)
        return queryset

    # 필터관련 쿼리문 작성 메서드
    def filter_operation(self,  fields, relate_operator = "AND" ):
        conditions = ""

        for key in fields:
            operator = '='
            
            if self.request.query_params.get(key, False):
                if len(conditions) > 0:
                    conditions += relate_operator + " "
                
                conditions += "{0} {1} '{2}'".format(key, operator, self.request.query_params[key] )

        # BOOLEAN 처리
        while conditions.find('true') > -1 :
            conditions = conditions.replace('true', '1')
        
        while conditions.find('false') > -1 :
            conditions = conditions.replace('false', '0')

        return conditions

    def get_search_filter(self, relate_operator = "OR"):
        conditions = ""

        for key in self.search_fields:
            if self.request.query_params.get("search", False):
                if len(conditions) > 0 :
                    conditions += " " + relate_operator + " "

                conditions += "{0} LIKE CONCAT('%%', '{1}', '%%')".format(key, self.request.query_params['search'])

        return conditions

    def get_ordering_filter(self, ordering_data):
        order_query = ""

        for key in self.ordering_fields:
            for param in ordering_data:
                if param.find(key) > -1 :
                    if order_query.find('ORDER BY') == -1 :
                        order_query += ' ORDER BY'
                    else :
                        order_query += ','

                    if param.find("-") > -1:
                        order_query += " " + key + " DESC"
                    else :
                        order_query += " " + key + " ASC"
        return order_query

    def get_grouping_filter(self):
        group_query = ""

        for key in self.group_fields:
            if group_query.find('GROUP BY') == -1 :
                group_query += ' GROUP BY'
            else :
                group_query += ','

            group_query += ' ' + key

        return group_query

    def add_filter(self, key, value, queryset, relate_operator = 'AND' ):
        query = string_utils.replace_percent_mark(
            " ".join( str(queryset.query).
                            strip().
                            replace("\n", "").
                            split()
                    )
            )

        operator = '='

        if key.find('__') > 0:
            if key.find("__gte")    > 0: operator = '>='
            elif key.find("__lte")  > 0: operator = '<='
            elif key.find("__gt")   > 0: operator = '>'
            elif key.find("__lt")   > 0: operator = '<'
            elif key.find("__in")   > 0: 
                operator = 'in'

                list_str = '('

                for item in value:
                    list_str += "'" + str(item) + "',"
                
                value = list_str[0: list_str.__len__() - 1] + ')'
            elif key.find("__contain") > 0:
                operator = "LIKE"
                value =  "CONCAT('%%', '{0}', '%%')".format(value)
            
            key = key.split("__")[0]

        if operator is not 'in' and operator is not 'LIKE' :
            value = "'" + value + "'"

        check_groupby = False
        query_arr = query.split("GROUP BY")
        query_arr[0] = self.add_where(query_arr[0], relate_operator)

        if query_arr.__len__() > 1 :
            query = query_arr[0] + "{0} {1} {2}".format(key, operator, value ) + " GROUP BY " + query_arr[1]
            check_groupby = True
        else :
            query = query_arr[0] + "{0} {1} {2}".format(key, operator, value )

        query_arr = query.split("ORDER BY")

        if check_groupby:
            query_arr[0] = self.add_where(query_arr[0], "")
            if query_arr.__len__() > 1 :
                query = query_arr[0] + " ORDER BY " + query_arr[1]
        else :
            query_arr[0] = self.add_where(query_arr[0], relate_operator)
            if query_arr.__len__() > 1 :
                query = query_arr[0] + "{0} {1} {2}".format(key, operator, value ) + " ORDER BY " + query_arr[1]
            else :
                query = query_arr[0] + "{0} {1} {2}".format(key, operator, value )

        queryset.query = RawQuery(query, queryset.db)

        return queryset

    def add_where(self, query, relate_operator):
        if query.find('WHERE') == -1 :
            query += ' WHERE '
        else :
            query += ' ' + relate_operator + ' '

        return query

    def add_condition(self, sentence, queryset, relate_operator = 'AND'):
        query = string_utils.replace_percent_mark(
            " ".join( str(queryset.query).
                            strip().
                            replace("\n", "").
                            split()
                    )
            )

        query_arr = query.split("ORDER BY")

        if query_arr[0].find('WHERE') == -1 :
            query_arr[0] += ' WHERE '
        else :
            query_arr[0] += ' ' + relate_operator + ' '

        if query_arr.__len__() > 1 :
            query = query_arr[0] + "{0}".format( sentence ) + " ORDER BY " + query_arr[1]   
        else :
            query = query_arr[0] + "{0}".format( sentence )

        queryset.query = RawQuery(query, queryset.db)

        return queryset

    # 정렬대상이 a.id같은 경우 프론트에서 처리가 번거로운 상황이 발생할때
    # 쿼리에 직접 넣어 사용
    def add_ordering(self, queryset = None, ordering = None):
        # 정렬하기
        query = string_utils.replace_percent_mark(
            " ".join(                   # ' '로 다시 붙이기
                str(queryset.query).
                strip().                # 공백 제거
                replace("\n", "").      # 개행 없애기
                split()                 # 공백으로 구분
            )
        )
        # ordering 값에 '-'가 있으면 DESC
        if ordering is not None and ordering is not '':
            ordering = ordering.split(',')
            order_by_query = []
            for order_column in ordering:
                if order_column.find('-') > -1:
                    order_by_query.append(' {0} DESC'.format(order_column.split('-')[1]))
                else:
                    order_by_query.append(' {0} ASC'.format(order_column))
            query = query + ' ORDER BY{0}'.format(",".join(order_by_query))

        queryset.query = RawQuery(query, queryset.db)

        return queryset

class RawQuerySyntax():
    # query에 where 유무 파악후 and 할지 where를 붙일지(like concat 등 사용시 용이하려고 만듬)
    def add_where(query = None, condition = None, relate_operator = 'AND'):
        where_query = query

        if where_query.find('WHERE') == -1:
            relate_operator = 'WHERE'

        where_query = where_query + ' {0} {1}'.format(relate_operator, condition)

        return where_query