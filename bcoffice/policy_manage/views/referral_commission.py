from . import *


class ReferralCommission(APIView):
    """
    추천인 커미션 가져오기
    """
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "referral-commission"
    permission_classes = [ReferralCommissionPermission]
    #--------------------------------------
    #  METHODS
    #--------------------------------------
    def get(self, request, *args, **kwargs):
        fee = ReferralInfos.objects.using("exchange").get(pk = 1)

        data = {}
        data['commission'] = fee.fee

        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        params ={}
        params['fee'] = request.data.get("fee", None)

        if params['fee'] is None :
            return Response(
                data=ResponseMessage.getMessageData(ResponseMessage.MESSAGE_ERR000017.format("fee"))
                , status = status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.get(id = request.user.get_id())
        fee = ReferralInfos.objects.using("exchange").get(pk = 1)

        body = {
            "user_id"       : request.user.get_id()
            , "emp_no"      : user.emp_no
            , "before"      : float(fee.fee)
            , "after"       : float(params['fee'])
            , "created_at"  : str(datetime.now())
        }

        response = APIService.request_api(request, APIService.REFERRAL_POLICY_FEE_SET, params)

        log = CentralLogging()
        log.setLog(body, request, CREATE, response.status_code, 5200)

        # MONGO DB 추가
        logging_utils.set_log(TBL_BCOFFICE_REFERRAL_COMMISSION_MOD, log.toJsonString())

        return response