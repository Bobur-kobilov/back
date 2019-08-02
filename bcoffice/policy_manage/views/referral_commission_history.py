from . import *

class ReferralCommissionHistory(APIView):
    name = "referral-commission-history"
    permission_classes = [ReferralCommissionPermission]

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get("limit", None)
        offset = request.query_params.get("offset", None)
        data = {}

        mongodb = BCOfficeHistoryMongoDB(collection=TBL_BCOFFICE_REFERRAL_COMMISSION_MOD)
        result = (mongodb.collection.find().sort('_id', pymongo.DESCENDING))
        count = mongodb.collection.find().count()

        if limit is not None and offset is not None:
            result = result[int(offset):int(offset) + int(limit)]
            data['count'] = count


        data['results'] = []

        for item in result :
            print(item)
            obj = {}
            obj['header'] = item['header']
            obj['body'] = item['body']

            sqlTime = obj['header']['sqlTime']
            created_at = obj['body']['created_at']

            if isinstance( sqlTime, str ):
                sqlTime = datetime.strptime(sqlTime, '%Y-%m-%d %H:%M:%S.%f')

            if isinstance( created_at, str ):
                created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S.%f')

            sqlTime = sqlTime.strftime("%Y-%m-%d %H:%M:%S")
            created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")

            obj['header']['sqlTime'] = sqlTime #date_util.utc_datetime_to_local(obj['header']['sqlTime'])
            obj['body']['created_at'] = created_at #date_util.utc_datetime_to_local(obj['body']['created_at'])

            data['results'].append(obj)

        mongodb.close()

        return Response(data = data, status = status.HTTP_200_OK)