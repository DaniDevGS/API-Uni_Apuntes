from django.shortcuts import render
from .models import Apunte
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ApunteSerializer
from notas.models import *

# Create your views here.
class ApuntesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = Apunte.objects.filter(estudiante=request.user)
        serializer = ApunteSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ApuntePOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(estudiante=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ApuntesViewDetalle(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, request, pk):
        return get_object_or_404(Apunte, pk=pk, estudiante=request.user)

    def get(self, request, pk=None):
        data = self.get_object(request, pk)
        serializer = ApunteSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, pk=None):
        data = self.get_object(request, pk)
        serializer = ApuntePOSTSerializer(data, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Apunte editado"}, status=status.HTTP_200_OK)
        
    def patch(self, request, pk=None):
        data = self.get_object(request, pk)
        serializer = ApuntePOSTSerializer(data, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Apunte editado"}, status=status.HTTP_200_OK)
        
    def delete(self, request, pk=None):
        data = self.get_object(request, pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EstadisticasDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        notas = Notas.objects.filter(estudiante=request.user)
        
        promedio_global_trimestre