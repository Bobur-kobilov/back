from . import *


# 공지사항 첨부파일 제거
class NoticeAttachDestroy(DestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "notice-attach-destroy"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [NoticeAttachDestroyPermission]

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
        instance = self.get_object(request.query_params['pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)