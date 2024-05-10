from .models import State, Optimization
from rest_framework import serializers


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class OptimizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Optimization
        fields = '__all__'
