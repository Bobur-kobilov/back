from . import *


# 코인가이드 로고 제거
class CoinGuideAttachDestroy(DestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "coinguide-attach-destroy" 

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [CoinGuideAttachDestroyPermission]
    
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = FileAttachmentSerializer
        return serializer
            
    # 쿼리셋 가져오기
    def get_queryset(self):
        return FileAttachment.objects.all()

    def get_object(self, id):
        return FileAttachment.objects.get(id = id)

    def destroy(self, request, *args, **kwargs):
        file_logo = FileAttachment.objects.filter(id = request.query_params['pk'])
        self.perform_destroy(file_logo)
        return Response(status=status.HTTP_204_NO_CONTENT)