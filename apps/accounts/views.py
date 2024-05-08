from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterView(APIView):
    def post(self, request):
        # 역직렬화 (JSON -> model)
        serializer = UserSerializer(data=request.data)

        # 유효성 검사
        if serializer.is_valid():
            # DB에 저장
            user = serializer.save()
            return Response({'message': 'register success', 'id': user.id, 'phone_number': user.phone_number},
                            status=status.HTTP_200_OK)

        return Response({'message': 'register failed', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AuthView(APIView):
    # 로그인
    def post(self, request):
        # user 탐색
        user = authenticate(id=request.data.get("id"), password=request.data.get("password"))

        if user is not None:
            # JWT 발급
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    'message': 'login success',
                    'id': user.id,
                    'token': {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            # JWT을 쿠키에 저장
            res.set_cookie('access', access_token, httponly=True)
            res.set_cookie('refresh', refresh_token, httponly=True)
            return res
        else:
            return Response({'message': 'login failed'}, status=status.HTTP_400_BAD_REQUEST)
