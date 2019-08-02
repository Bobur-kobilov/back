
from . import *
# 거래소 회원 상세정보 조회
class MemberDetail(ListAPIView):
    # --------------------------------------
    #  PROPERTIES
    # --------------------------------------
    name = "member-detail"
    permission_classes = [MemberDetailPermission]

    # --------------------------------------
    #  OVERRIDEN METHODS
    # --------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = MemberSerializer
        return serializer

    # 쿼리셋 가져오기
    def get_queryset(self, search_type=None, search_value=None):
        types = ['id', 'email', 'phone']

        query = Members.objects.using("exchange")

        if search_type in types:
            if search_type == 'id':
                query = query.filter(id=int(search_value))
            elif search_type == 'email':
                query = query.filter(email=search_value)
            elif search_type == 'phone':
                query = query.filter(phone_number=search_value)
            return query
        else:
            return None

    def list(self, request, *args, **kwargs):

        # 거래소 이용자 검색
        search_type = request.GET.get('search_type', None)
        search_value = request.GET.get('search_value', None)

        if search_type is None or search_type is '' or search_value is None or search_value is '':
            return Response(
                # "회원검색 값을 넣어주세요."
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00007)
                , status=status.HTTP_400_BAD_REQUEST
            )

        if search_type == 'id':
            try:
                if type(int(search_value)) is int:
                    pass
            except Exception:
                return Response(
                    # "ID를 숫자형식으로 입력해주세요."
                    data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00012)
                    , status=status.HTTP_400_BAD_REQUEST
                )

        queryset = self.get_queryset(
            search_type=search_type
            , search_value=search_value
        )

        if queryset is None:
            return Response(
                # "일치하는 값이 없습니다."
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00008)
                , status=status.HTTP_404_NOT_FOUND
            )

        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data.__len__() is 0:
            return Response(
                # "일치하는 값이 없습니다."
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR00022)
                , status=status.HTTP_404_NOT_FOUND
            )
        serializer_length = len(serializer.data)
        n = 0
        total_data = []
        while n < serializer_length:

            result = serializer.data[n]
            question_count = Question.objects.filter(member_id=result['id']).aggregate(count=Count('id'))

            no_answer_count = (Question.objects
                            .filter(member_id=result['id'])
                            .exclude(status='CPLT')
                            .aggregate(count=Count('id'))
                            )

            last_login = (
                SignupHistories.objects.using("exchange")
                    .filter(member_id=result['id'])
                    .values('created_at')
                    .order_by('-id')
            )

            last_login_date = None

            if last_login.exists():
                last_login_date = list(last_login)[0]['created_at'].strftime("%Y-%m-%d %H:%M:%S")
                utc_time = datetime.strptime(last_login_date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
                last_login_date = utc_time.astimezone(timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S")

            result['question_count'] = question_count['count']
            result['no_answer_count'] = no_answer_count['count']
            result['last_login'] = last_login_date

            # OTP, SMS 등록일 해제일 (mongoDB)
            mongodb = BCOfficeHistoryMongoDB(collection=TBL_BCOFFICE_MEMBER_MOD)

            mongo_params = {}
            mongo_params['body.member_id'] = int(result['id'])
            mongo_params['body.category'] = 'twofactor'
            otp_regist_time = "이력없음"
            sms_regist_time = "이력없음"
            for two_factor in result['two_factors']:
                if two_factor['type'] == 'TwoFactor::App':
                    if two_factor['activated'] is 1:
                        mongo_params['body.reason'] = {'$regex': '^regist otp'}
                    else:
                        mongo_params['body.reason'] = {'$regex': '^unregist otp'}
                    try:
                        otp_regist_time = (mongodb.collection.find(mongo_params).sort('_id', pymongo.DESCENDING).limit(1))[0]['body']['created_at']
                    except:
                        otp_regist_time = "이력없음"
                else:
                    if two_factor['activated'] is 1:
                        mongo_params['body.reason'] = {'$regex': '^regist sms'}
                    else:
                        mongo_params['body.reason'] = {'$regex': '^unregist sms'}
                    try:
                        sms_regist_time = (mongodb.collection.find(mongo_params).sort('_id', pymongo.DESCENDING).limit(1))[0]['body']['created_at']
                    except:
                        sms_regist_time = "이력없음"

            mongodb.close()

            result['otp_regist_time'] = otp_regist_time
            result['sms_regist_time'] = sms_regist_time
            total_data.append(result)
            n = n + 1
        return Response({'results': total_data})

