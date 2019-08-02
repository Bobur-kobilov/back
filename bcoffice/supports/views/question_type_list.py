from . import *
import os

# 1:1 문의내역 카테고리
class QuestionTypeList(ListAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "question-type-list"

    filter_fields   = ['lang']
    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    #permission_classes = [QuestionTypePermission]

    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = QuestionTypeSerializer
        return serializer

    def list(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', "ko")

        response = super(QuestionTypeList, self).list(request, args, kwargs)
        for row in response.data:
            file_path = '{}/template/question/{}/{}.txt'.format(os.getcwd(), lang, row['id'])
            if os.path.exists(file_path):
                template = open(file_path, 'rt', encoding='UTF8').read()
            else:
                template = ''
            row['template'] = template
        print("**********")
        print(response)
        return response


    # 쿼리셋 가져오기
    def get_queryset(self):


        return QuestionType.objects.all()