from . import *
import redis
import time as t
import threading
import dateutil.parser
from datetime import *
import json 
import ast
from django.core.cache  import cache
# 게시물 이미지 업로드

class ImageUpload(APIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "image-upload"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [ImageUploadPermission]

    parser_classes = [MultiPartParser]
    def get(self,request):
        data = self.getRedisData(request="all")
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
       
        if "banner" in request.data:
            response = self.updateBanner(request)
            return Response(data=response, status=status.HTTP_200_OK)

        else:    
            global end_date

            if "button_link" in request.data:
                button_link = request.data['button_link']
            if "button_text" in request.data:
                button_text = request.data['button_text']
                    
            start_date = None
            
            end_date = None
            if "start_date" in request.data:
                start_date = request.data['start_date'] 
            if "end_date" in request.data:
                end_date = request.data['end_date']

            if "images" in request.FILES:
                key = self.saveS3(image=request.FILES['images'], start_date=start_date, button_link=button_link,button_text=button_text)
                data = {
                    "link" : 'https://' + settings.AWS_S3_CUSTOM_DOMAIN + "/" + key
                }
            if "delete_key" in request.data:
                data = self.deleteRedisKey()

            return Response(data=data, status=status.HTTP_200_OK)

    def redisSet(self, action=None):
        global end_date
        
        if action == "delete_key":
            cache.delete("welcome:popups")
        else:
            global redisData        
            data = str(redisData).replace("'", '"')
            cache.set("welcome:popups",data,timeout=None)
        if end_date is not None and end_date is not '':
            end_date = int(end_date)
            cache.expire("welcome:popups",end_date)
    
    def saveS3(self, image=None,start_date=None,button_link=None,button_text=None):
        if image is not None:
            up_file = image
            extention_split = up_file.name.split(".")
            extention = extention_split[extention_split.__len__() - 1]
            file_name = str(uuid.uuid4()) + "." + extention
            dt = datetime.now().strftime('/%Y/%m/%d/')
            key = 'static' + dt + file_name

            s3 = boto3.resource('s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            client = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

            response = client.put_object(
            Key=key
            , Body=up_file.read()
            , ACL = 'public-read'
            )
            if button_link is not None and button_text is not None:
                global redisData
                redisData = [{
                "img_src": "https://" + settings.AWS_S3_CUSTOM_DOMAIN + "/" + key
                , "link": button_link
                , "button_text": button_text
                }]
                if start_date is not None and start_date is not '':
                    start_date = int(start_date)
                    now = datetime.now()
                    run_at = now + timedelta(seconds=start_date)
                    delay = (run_at - now).total_seconds()
                    threading.Timer(delay, self.redisSet).start()  
                else:
                    self.redisSet()
            return key
    def deleteRedisKey(self):
        self.redisSet(action="delete_key")
        return  "Deleted"

    def updateBanner(self,request):
        response = self.getRedisData(request)
        return response
    
    def getRedisData(self, request):
        LINK = 'https://' + settings.AWS_S3_CUSTOM_DOMAIN + "/"
        data = cache.get('welcome:banners')
        data = ast.literal_eval(data)
        if 'action' in request.data:
            response = data
        else:
            if "leftBanner" in request.data:
                response = "leftBanner"
                key  = self.saveS3(image=request.data['leftBanner'])
                left_img_src = LINK + key
                left_img_link = request.data['leftBannerLink']
            else:
                left_img_src = data['left']['img_src']
                left_img_link = data['left']['link']

            if "rightBanner" in request.data:
                response = "bottomBanner"
                key = self.saveS3(image=request.data['rightBanner'])
                right_bottom_img_src = LINK + key
                right_bottom_img_link = request.data['rightBannerLink']
                right_bottom_title = request.data['right_bottom_title']
            else:
                right_bottom_img_src = data['right_bottom']['img_src']
                right_bottom_img_link = data['right_bottom']['link']
                right_bottom_title = data['right_bottom']['title_text']
            if "bottomBanner" in request.data:
                response = "rightBanner"
                key = self.saveS3(image=request.data['bottomBanner'])
                right_top_img_src = LINK + key
                right_top_img_link = request.data['bottomBannerLink']
            else:
                right_top_img_src = data['right_top']['img_src']
                right_top_img_link = data['right_top']['link']

            redisData = {
                "left":{
                    "img_src":left_img_src,
                    "link": left_img_link
                },
                "right_bottom":{
                    "img_src": right_bottom_img_src,
                    "link": right_bottom_img_link,
                    "title_text": right_bottom_title
                },
                "right_top": {
                    "img_src": right_top_img_src,
                    "link": right_top_img_link
                }
            }
            redisData = str(redisData).replace("'",'"')
            
            self.setRedisBanner(data=redisData)
        return response
    
    def setRedisBanner(self,data=None):

        cache.set("welcome:banners", data,timeout=None)
    


        


