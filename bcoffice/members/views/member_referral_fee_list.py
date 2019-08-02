from . import *


# 추천인정보 수수료 변경내역
class MemberReferralFeeList(APIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "referral-fee"
    
    def get(self, request, *args, **kwargs):
        
        permission_classes = [MemberReferralFeeGetPermission]

        limit = request.query_params.get("limit", None)
        offset = request.query_params.get("offset", None)

        # 거래소 회원 검색
        member_id     = request.query_params.get('member_id', None)

        # 조회기간 선택
        start_date      = request.query_params.get('start_date' , None)
        end_date        = request.query_params.get('end_date'   , None)

        # 관리자 검색
        user_id         = request.query_params.get('user_id'    , None)
        
        params = {}
        date_param = {}
        data = {}
        is_date_params = False

        params['body.member_id'] = int(member_id)

        if user_id is not None :
            params['body.user_id'] = int(user_id)

        if start_date is not None :
            date_param['$gte'] = start_date
            is_date_params = True
        
        if  end_date is not None :
            date_param['$lte'] = end_date
            is_date_params = True

        if is_date_params :
            params['body.created_at'] = date_param

        # mongoDB 데이터 가져오기
        mongodb = BCOfficeHistoryMongoDB(collection=TBL_BCOFFICE_REFERRAL_FEE_MOD)
        
        result = (mongodb.collection.find(params).sort('_id', pymongo.DESCENDING))
        count = mongodb.collection.find(params).count()

        if limit is not None and offset is not None:
            result = result[int(offset):int(offset) + int(limit)]
            data['count'] = count
        
        data['results'] = []

        for item in result :
            obj = {}
            obj['header'] = item['header']
            obj['header']['sqlTime'] = date_util.removeMsec(obj['header']['sqlTime'])
            obj['body'] = item['body']
            obj['body']['created_at'] = date_util.removeMsec(obj['body']['created_at'])

            data['results'].append(obj)

        mongodb.close()

        return Response(data = data, status = status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        #--------------------------------------
        #  AUTHORITY
        #--------------------------------------
        permission_classes = [MemberReferralFeePostPermission]

        params = {}
        params['member_id'] = request.data.get('member_id'  , False)
        params['fee']       = request.data.get('fee'        , False)

        #QueueUtil.publish( CENTRAL_LOGGING, s, TBL_BCOFFICE_REFERRAL_FEE_MOD)
        # 거래소 DB 수정
        member = Members.objects.using("exchange").get(id = params['member_id'])
        user = User.objects.get(id = request.user.get_id())

        body = {
            "user_id"       : request.user.get_id()
            , "emp_no"      : user.emp_no
            , "member_id"   : int(params['member_id'])
            , "mod_fee"     : float(params['fee'])
            , "created_at"  : str(datetime.now())
        }

        response = APIService.request_api(request = request, url = APIService.REFERRAL_FEE_SET, params = params)

        log = CentralLogging()
        log.setLog(body, request, UPDATE, response.status_code, 1200)

        # MONGO DB 추가
        logging_utils.set_log(TBL_BCOFFICE_REFERRAL_FEE_MOD, log.toJsonString())
    
        return response