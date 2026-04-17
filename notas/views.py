from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from .serializers import (
    ProfesorSerializer, ProfesorPOSTSerializer, MateriaSerializer, MateriaPOSTSerializer, TrimestreSerializer, TrimestrePOSTSerializer,
    CorteSerializer, CortePOSTSerializer, NotaSerializer, NotaPOSTSerializer, EvaluacionSerializer, EvaluacionPOSTSerializer
)
from .models import Profesor, Materia, Trimestre, Corte, Nota, Evaluacion
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, FloatField, Prefetch
from django.db.models.functions import Coalesce

class ProfesoresView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = Profesor.objects.filter(estudiante=request.user)
        serializer = ProfesorSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProfesorPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(estudiante=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfesoresViewDetalle(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, request, pk):
        return get_object_or_404(Profesor, pk=pk, estudiante=request.user)

    def get(self, request, pk=None):
        data = self.get_object(request, pk)
        serializer = ProfesorSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, pk=None):
        data = self.get_object(request, pk)
        serializer = ProfesorPOSTSerializer(data, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Profesor editado"}, status=status.HTTP_200_OK)
        
    def patch(self, request, pk=None):
        data = self.get_object(request, pk)
        serializer = ProfesorPOSTSerializer(data, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Profesor editado"}, status=status.HTTP_200_OK)
        
    def delete(self, request, pk=None):
        data = self.get_object(request, pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MateriasView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = Materia.objects.filter(estudiante=request.user)
        serializer = MateriaSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        prof_id = request.data.get('profesor')
        if prof_id and not Profesor.objects.filter(pk=prof_id, estudiante=request.user).exists():
            return Response({"error": "Profesor no válido o no pertenece al usuario."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = MateriaPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(estudiante=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MateriasViewDetalle(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, request, pk):
        return get_object_or_404(Materia, pk=pk, estudiante=request.user)

    def get(self, request, pk=None):
        data = self.get_object(request, pk)
        serializer = MateriaSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        data = self.get_object(request, pk)
        prof_id = request.data.get('profesor')
        if prof_id and not Profesor.objects.filter(pk=prof_id, estudiante=request.user).exists():
            return Response({"error": "Profesor no válido o no pertenece al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MateriaPOSTSerializer(data, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Materia editada"}, status=status.HTTP_200_OK)
        
    def patch(self, request, pk=None):
        data = self.get_object(request, pk)
        prof_id = request.data.get('profesor')
        if prof_id and not Profesor.objects.filter(pk=prof_id, estudiante=request.user).exists():
            return Response({"error": "Profesor no válido o no pertenece al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MateriaPOSTSerializer(data, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Materia editada"}, status=status.HTTP_200_OK)
        
    def delete(self, request, pk=None):
        data = self.get_object(request, pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TrimestresView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = Trimestre.objects.filter(estudiante=request.user)
        serializer = TrimestreSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        materias_ids = request.data.get('materias', [])
        if materias_ids:
            materias_validas = Materia.objects.filter(pk__in=materias_ids, estudiante=request.user).count()
            if materias_validas != len(materias_ids):
                return Response({"error": "Una o más materias no pertenecen al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TrimestrePOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(estudiante=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TrimestresViewDetalle(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, request, pk):
        return get_object_or_404(Trimestre, pk=pk, estudiante=request.user)

    def get(self, request, pk=None):
        data = self.get_object(request, pk)
        serializer = TrimestreSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        data = self.get_object(request, pk)
        materias_ids = request.data.get('materias', [])
        if materias_ids:
            materias_validas = Materia.objects.filter(pk__in=materias_ids, estudiante=request.user).count()
            if materias_validas != len(materias_ids):
                return Response({"error": "Una o más materias no pertenecen al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TrimestrePOSTSerializer(data, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Trimestre editado"}, status=status.HTTP_200_OK)
        
    def patch(self, request, pk=None):
        data = self.get_object(request, pk)
        if 'materias' in request.data:
            materias_ids = request.data.get('materias', [])
            materias_validas = Materia.objects.filter(pk__in=materias_ids, estudiante=request.user).count()
            if materias_validas != len(materias_ids):
                return Response({"error": "Una o más materias no pertenecen al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TrimestrePOSTSerializer(data, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Trimestre editado"}, status=status.HTTP_200_OK)
        
    def delete(self, request, pk=None):
        data = self.get_object(request, pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CortesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = Corte.objects.filter(materia__estudiante=request.user)
        serializer = CorteSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        materia_id = request.data.get('materia')
        if not materia_id or not Materia.objects.filter(pk=materia_id, estudiante=request.user).exists():
            return Response({"error": "Materia inválida o no pertenece al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CortePOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CortesViewDetalle(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, request, pk):
        return get_object_or_404(Corte, pk=pk, materia__estudiante=request.user)

    def get(self, request, pk=None):
        data = self.get_object(request, pk)
        serializer = CorteSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        data = self.get_object(request, pk)
        materia_id = request.data.get('materia')
        if materia_id and not Materia.objects.filter(pk=materia_id, estudiante=request.user).exists():
            return Response({"error": "Materia inválida o no pertenece al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CortePOSTSerializer(data, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Corte editado"}, status=status.HTTP_200_OK)
        
    def patch(self, request, pk=None):
        data = self.get_object(request, pk)
        materia_id = request.data.get('materia')
        if materia_id and not Materia.objects.filter(pk=materia_id, estudiante=request.user).exists():
            return Response({"error": "Materia inválida o no pertenece al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CortePOSTSerializer(data, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Corte editado"}, status=status.HTTP_200_OK)
        
    def delete(self, request, pk=None):
        data = self.get_object(request, pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotasView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = Nota.objects.filter(corte__materia__estudiante=request.user)
        serializer = NotaSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        corte_id = request.data.get('corte')
        if not corte_id or not Corte.objects.filter(pk=corte_id, materia__estudiante=request.user).exists():
            return Response({"error": "Corte inválido o no pertenece al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = NotaPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class NotasViewDetalle(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, request, pk):
        return get_object_or_404(Nota, pk=pk, corte__materia__estudiante=request.user)

    def get(self, request, pk=None):
        data = self.get_object(request, pk)
        serializer = NotaSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        data = self.get_object(request, pk)
        corte_id = request.data.get('corte')
        if corte_id and not Corte.objects.filter(pk=corte_id, materia__estudiante=request.user).exists():
            return Response({"error": "Corte inválido o no pertenece al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = NotaPOSTSerializer(data, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Nota editada"}, status=status.HTTP_200_OK)
        
    def patch(self, request, pk=None):
        data = self.get_object(request, pk)
        corte_id = request.data.get('corte')
        if corte_id and not Corte.objects.filter(pk=corte_id, materia__estudiante=request.user).exists():
            return Response({"error": "Corte inválido o no pertenece al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = NotaPOSTSerializer(data, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Nota editada"}, status=status.HTTP_200_OK)
        
    def delete(self, request, pk=None):
        data = self.get_object(request, pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EvaluacionesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = Evaluacion.objects.filter(nota__corte__materia__estudiante=request.user)
        serializer = EvaluacionSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        nota_id = request.data.get('nota')
        if not nota_id or not Nota.objects.filter(pk=nota_id, corte__materia__estudiante=request.user).exists():
            return Response({"error": "Nota inválida o no pertenece al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EvaluacionPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EvaluacionesViewDetalle(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, request, pk):
        return get_object_or_404(Evaluacion, pk=pk, nota__corte__materia__estudiante=request.user)

    def get(self, request, pk=None):
        data = self.get_object(request, pk)
        serializer = EvaluacionSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        data = self.get_object(request, pk)
        nota_id = request.data.get('nota')
        if nota_id and not Nota.objects.filter(pk=nota_id, corte__materia__estudiante=request.user).exists():
            return Response({"error": "Nota inválida o no pertenece al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EvaluacionPOSTSerializer(data, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Evaluación editada"}, status=status.HTTP_200_OK)
        
    def patch(self, request, pk=None):
        data = self.get_object(request, pk)
        nota_id = request.data.get('nota')
        if nota_id and not Nota.objects.filter(pk=nota_id, corte__materia__estudiante=request.user).exists():
            return Response({"error": "Nota inválida o no pertenece al usuario."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EvaluacionPOSTSerializer(data, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Evaluación editada"}, status=status.HTTP_200_OK)
        
    def delete(self, request, pk=None):
        data = self.get_object(request, pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EstadisticasDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        
        # 1. Optimizamos la consulta de Cortes para que traiga su suma ya calculada
        # Esto evita hacer un query por cada corte dentro del loop (N+1)
        cortes_con_suma = Corte.objects.annotate(
            nota_acumulada=Coalesce(Sum('notas__evaluaciones__puntuacion'), 0.0, output_field=FloatField())
        )

        # 2. Obtenemos materias con su nota final y precalificamos los cortes
        materias = Materia.objects.filter(estudiante=usuario).annotate(
            nota_final=Coalesce(Sum('cortes__notas__evaluaciones__puntuacion'), 0.0, output_field=FloatField())
        ).prefetch_related(
            Prefetch('cortes', queryset=cortes_con_suma, to_attr='cortes_optimizados')
        )
        
        materias_aprobadas_count = 0
        materias_peligro_count = 0
        materias_reprobadas_count = 0
        suma_promedios = 0
        
        materias_detalle = []
        
        for m in materias:
            nf = m.nota_final
            suma_promedios += nf
            
            # Lógica de estados IUTIRLA
            if nf >= 50:
                materias_aprobadas_count += 1
                estado = "Aprobada"
            elif nf >= 45:
                materias_peligro_count += 1
                estado = "Recuperatorio"
            else:
                materias_reprobadas_count += 1
                estado = "Reprobada"
                
            # Breakdown por corte usando los datos ya cargados en memoria (cortes_optimizados)
            cortes_info = []
            for c in m.cortes_optimizados:
                cortes_info.append({
                    "corte_numero": c.numero,
                    "nota_acumulada": c.nota_acumulada,
                    "maximo_posible": 25.0
                })
                
            materias_detalle.append({
                "materia_id": m.id,
                "nombre": m.nombre,
                "nota_final": nf,
                "estado": estado,
                "cortes": cortes_info
            })
            
        total_materias = len(materias_detalle)
        promedio_global = suma_promedios / total_materias if total_materias > 0 else 0
        mejor_materia_global = max(materias_detalle, key=lambda x: x["nota_final"]) if materias_detalle else None
        
        # 3. Mejor materia por trimestre (Optimizamos con prefetch_related para evitar más queries)
        trimestres = Trimestre.objects.filter(estudiante=usuario).prefetch_related('materias')
        mejores_por_trimestre = []
        
        # Creamos un mapa de ID -> Info para búsqueda rápida en el dashboard
        materias_map = {item["materia_id"]: item for item in materias_detalle}
        
        for t in trimestres:
            trimestre_materias = t.materias.all()
            if not trimestre_materias:
                continue
                
            mejor_m = None
            max_nota = -1
            
            for tm in trimestre_materias:
                m_info = materias_map.get(tm.id)
                if m_info and m_info["nota_final"] > max_nota:
                    max_nota = m_info["nota_final"]
                    mejor_m = m_info
                    
            if mejor_m:
                mejores_por_trimestre.append({
                    "trimestre": t.numero_trimestre,
                    "materia_nombre": mejor_m["nombre"],
                    "nota_final": max_nota
                })
                
        return Response({
            "promedio_global": round(promedio_global, 2),
            "materias_aprobadas": materias_aprobadas_count,
            "materias_peligro": materias_peligro_count,
            "materias_reprobadas": materias_reprobadas_count,
            "mejor_materia_absoluta": mejor_materia_global["nombre"] if mejor_materia_global else "N/A",
            "mejores_materias_por_trimestre": mejores_por_trimestre,
            "detalle_materias": materias_detalle
        }, status=status.HTTP_200_OK)
