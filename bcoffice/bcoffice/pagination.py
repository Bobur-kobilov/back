from collections import OrderedDict, namedtuple
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.db.models import Model
from django.db import connections
from django.db.models.query import RawQuerySet
from django.db.models.sql.query import RawQuery

from bcoffice.utils import string_utils
import re
    

# limit을 안 보내면 자동적으로 limt은 총 갯수
class StandardPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        self.limit = self.get_limit(request)
        if self.limit is None:
            self.limit = self.count

        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset:self.offset + self.limit])


class RawQuerySetPagination(StandardPagination):
    
    # 전체 카운트 가져오기
    def get_count(self, queryset, __db__="default", count_query = None):
        # count_query : raw query에서 select ~ from 사이에
        # 서브쿼리 발생할 경우 count하는 쿼리를 작성하여 사용
        query = ''
        if count_query is None:
            query = string_utils.replace_percent_mark(
                " ".join( str(queryset.query).
                                strip().
                                replace("\n", "").
                                split()
                        )
                )
            # SELECT와 FROM 사이의 컬럼 값을 count(*) 값으로 치환한다.
            if query.find("HAVING") > -1 or query.find("GROUP BY") > -1 :
                query = 'SELECT count(*) AS count FROM (' + query + ') as tmp'
                if query.find('ORDER BY') > -1:
                    query = query.split("ORDER BY")[0] + ') as tmp'
            else:
                query = re.sub('SELECT(.*?)FROM', 'SELECT count(*) AS count FROM', query, 0, re.I|re.S)
                query = query.split("ORDER BY")[0]
        else:
            query = count_query

        # DB 커넥션 객체에서 cursor를 뽑아온다.
        cursor = connections[__db__].cursor()

        # 커서를 통해 count 쿼리를 전달한다.
        cursor.execute(query)
        rows = cursor.fetchall()

        counts = []

        for row in rows:
            counts.append(row[0])
            
        return max(counts)

    # 응답객체 만들기
    # data : 시리얼라이즈 된 데이터 객체(serializer.data)
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('results', data)
        ]))

    # 페이징을 위한 쿼리셋 만들기 메서드
    # count_query : raw query에서 select ~ from 사이에
    # 서브쿼리 발생할 경우 count하는 쿼리를 작성하여 사용
    def paginate_queryset(self, queryset, request, view=None, __db__="default", count_query = None, count = None):

        if count is None:
            self.count = self.get_count(queryset, __db__=__db__, count_query = count_query)
        else:
            self.count = count

        self.limit = self.get_limit(request)
        if self.limit is None:
            return queryset

        self.offset = self.get_offset(request)
        self.request = request

        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        # if self.count == 0 or self.offset > self.count:
        #     return []
        
        sql = string_utils.replace_percent_mark(str(queryset.query))

        # LIMIT, OFFSET을 반영한 쿼리를 쿼리셋에 다시 반영시킨다.
        queryset.query = RawQuery(sql + " " + self.get_limit_filter(), queryset.db)
        
        return queryset

    # LIMIT, OFFSET 쿼리문을 작성하는 매서드
    def get_limit_filter(self):
        limit_query = ""
        if self.offset is not None: 
            limit_query += "LIMIT " + str(self.offset)

        if self.limit is not None and self.offset is not None:
            limit_query += ", " + str(self.limit)

        return limit_query
