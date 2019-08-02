from . import *

# FAQ 카테고리 목록조회
class FaqCategoryList(ListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "faq-category-list"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    # permission_classes = [FaqCategoryListPermission]

    #--------------------------------------
    #  PROPERTIES : FILTER
    #--------------------------------------
    filter_fields   = ['lang']
    search_fields   = []
    ordering_fields = ['id']
    ordering        = ['id']
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = FaqCategorySerializer
        return serializer
    
    # 쿼리셋 가져오기
    def get_queryset(self):
        return FaqCategory.objects