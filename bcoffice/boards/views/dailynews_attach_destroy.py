from . import *


# Daily뉴스 첨부파일 제거
class DailyNewsAttachDestroy(DestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "daliy-attach-destroy"    
    
    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [DailyNewsAttachDestroyPermission]

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
        file_attach = FileAttachment.objects.filter(id = request.query_params['pk'])
        self.perform_destroy(file_attach)
        return Response(status=status.HTTP_204_NO_CONTENT)