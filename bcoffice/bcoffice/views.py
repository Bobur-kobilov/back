from django.conf                import settings
from django.shortcuts           import render
from rest_framework             import status, viewsets
from rest_framework.response    import Response
from rest_framework.views       import APIView
from rest_framework.decorators  import api_view

@api_view(['GET'])
def get_market_list(request):
    return Response(data=settings.MARKET_LIST, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_currency_list(request):
    return Response(data=settings.CURRENCY_LIST, status=status.HTTP_200_OK)
