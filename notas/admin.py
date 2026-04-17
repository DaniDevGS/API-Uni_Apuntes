from django.contrib import admin
from .models import *
from biblioteca.models import Apunte

# Register your models here.
admin.site.register(Profesor)
admin.site.register(Materia)
admin.site.register(Trimestre)
admin.site.register(Corte)
admin.site.register(Nota)
admin.site.register(Evaluacion)

admin.site.register(Apunte)