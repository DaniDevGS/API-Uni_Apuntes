from rest_framework import serializers
from .models import Profesor, Materia, Trimestre, Corte, Nota, Evaluacion

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ['id', 'nombre']

class ProfesorPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ['nombre']


class MateriaSerializer(serializers.ModelSerializer):
    profesor_nombre = serializers.ReadOnlyField(source='profesor.nombre')

    class Meta:
        model = Materia
        fields = ['id', 'nombre', 'descripcion', 'profesor', 'profesor_nombre']

class MateriaPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ['nombre', 'descripcion', 'profesor']


class TrimestreSerializer(serializers.ModelSerializer):
    materias = MateriaSerializer(many=True, read_only=True)
    class Meta:
        model = Trimestre
        fields = ['id', 'numero_trimestre', 'descripcion', 'materias']

class TrimestrePOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trimestre
        fields = ['numero_trimestre', 'descripcion', 'materias']

class CorteSerializer(serializers.ModelSerializer):
    materia_nombre = serializers.ReadOnlyField(source='materia.nombre')

    class Meta:
        model = Corte
        fields = ['id', 'numero', 'materia', 'materia_nombre']

class CortePOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corte
        fields = ['numero', 'materia']


class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = ['id', 'tipo', 'puntuacion', 'nota', 'archivo']

class EvaluacionPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = ['tipo', 'puntuacion', 'nota', 'archivo']


class NotaSerializer(serializers.ModelSerializer):
    evaluaciones = EvaluacionSerializer(many=True, read_only=True)

    class Meta:
        model = Nota
        fields = ['id', 'valor', 'descripcion', 'corte', 'evaluaciones']

class NotaPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = ['valor', 'descripcion', 'corte']
