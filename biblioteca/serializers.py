from rest_framework import serializers
from .models import Apunte

class ApunteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apunte
        fields = ['id', 'titulo', 'estudiante', 'materia', 'descripcion', 'archivo']

class ApuntePOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apunte
        fields = ['titulo', 'materia', 'descripcion', 'archivo']