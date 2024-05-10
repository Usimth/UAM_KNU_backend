from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .optimization import *

class optimizer(APIView):
    def get(self,request:Request ):
        vert = Optimization(0.1)
        solution = vert.optimizing()
        return Response(solution,status=status.HTTP_200_OK)
