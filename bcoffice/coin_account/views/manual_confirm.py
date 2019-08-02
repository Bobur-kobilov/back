from . import *

class ManualConfirm(APIView):
    name = "manual-confirm"

    def post(self, request, *args, **kwargs):
        withdraw_id = request.data.get("withdraw_id", None)
        txid = request.data.get("txid", None)
        params = {
            "withdraw_id": withdraw_id,
            "txid": txid
        }
        request.method = 'get'
        response = APIService.request_api(request,APIService.MANUAL_WITHDRAW_CONFIRM,params)
        
        return response

