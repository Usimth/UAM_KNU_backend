from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class VertiportView(APIView):
    # 인증된 사용자만 view 접근 허용 (get은 모두 허용)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 버티포트 조회
    def get(self, request):
        vertiports = Vertiport.objects.all()
        serializer = VertiportSerializer(vertiports, many=True)
        return Response({'message': 'get success', 'results': serializer.data}, status=status.HTTP_200_OK)

    # 버티포트 생성
    def post(self, request):
        # 역직렬화 (JSON -> model)
        serializer = VertiportSerializer(data=request.data)

        # 유효성 검사
        if serializer.is_valid():
            # DB에 저장
            vertiport = serializer.save()
            return Response({'message': 'post success', 'name': vertiport.name}, status=status.HTTP_200_OK)

        return Response({'message': 'post failed', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # 버티포트 삭제
    def delete(self, request, name):
        # 관리자만 삭제 가능
        if request.user.is_admin:
            try:
                vertiport = Vertiport.objects.get(pk=name)
                vertiport.delete()
                return Response({'message': 'delete success'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': 'delete failed'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'delete failed'}, status=status.HTTP_400_BAD_REQUEST)
