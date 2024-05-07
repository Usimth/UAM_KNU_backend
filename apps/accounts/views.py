from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response


class Register(APIView):
    def post(self, request):
        # 역직렬화 (JSON -> model)
        serializer = UserSerializer(data=request.data)

        # 유효성 검사
        if serializer.is_valid():
            # DB에 저장
            user = serializer.save()
            return Response({'id': user.id, 'phone_number': user.phone_number}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
