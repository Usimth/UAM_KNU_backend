from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response


class VertiportView(APIView):
    # 버티포트 조회
    def get(self, request):
        vertiports = Vertiport.objects.all()
        serializer = VertiportSerializer(vertiports, many=True)
        return Response({'message': 'get success', 'results': serializer.data}, status=status.HTTP_200_OK)
