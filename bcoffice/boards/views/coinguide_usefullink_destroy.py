from . import *


# 코인가이드 유용한링크 제거
class CoinGuideUsefulLinkDestroy(DestroyAPIView):
    #--------------------------------------
    #  PROPERTIES
    #--------------------------------------
    name = "coinguide-link-destroy"

    #--------------------------------------
    #  AUTHORITY
    #--------------------------------------
    permission_classes = [CoinGuideUsefulLinkDeletePermission]
    
    #--------------------------------------
    #  OVERRIDEN METHODS
    #--------------------------------------
    # 시리얼라이저 클래스 가져오기
    def get_serializer_class(self):
        serializer = CoinGuideUsefulLinkSerializer
        return serializer
            
    # 쿼리셋 가져오기
    def get_queryset(self):
        return CoinGuideUsefulLink.objects.all()

    def get_object(self, id):
        return CoinGuideUsefulLink.objects.get(id = id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(request.query_params['pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)