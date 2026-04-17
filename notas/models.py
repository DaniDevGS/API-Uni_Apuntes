import os
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone

class BaseModel(models.Model):
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

def generar_ruta_evaluacion(instance, filename):
    """
    Genera una ruta dinámica: evaluaciones/usuario/YYYY/MM/nombre_materia/archivo.ext
    """
    estudiante = instance.nota.corte.materia.estudiante.username
    materia = instance.nota.corte.materia.nombre
    materia_slug = materia.replace(" ", "_").lower()
    
    fecha = timezone.now()
    return f'evaluaciones/{estudiante}/{fecha.year}/{fecha.month}/{materia_slug}/{filename}'
        
class Profesor(BaseModel):
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profesores')
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Materia(BaseModel):
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='materias')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, blank=True, related_name='materias')

    def __str__(self):
        return self.nombre

    class Meta:
        unique_together = ('estudiante', 'nombre')

class Trimestre(BaseModel):
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trimestres')
    numero_trimestre = models.PositiveIntegerField(help_text="Ej: 1, 2, 3...")
    descripcion = models.TextField(blank=True)
    materias = models.ManyToManyField('Materia', related_name='trimestres', blank=True)

    def __str__(self):
        return f"Trimestre {self.numero_trimestre}"

    class Meta:
        unique_together = ('estudiante', 'numero_trimestre')

class Corte(BaseModel):
    numero = models.PositiveIntegerField(help_text="Número de corte dentro del trimestre, ej 1..4")
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='cortes')

    def __str__(self):
        return f"Corte {self.numero} - {self.materia.nombre}"

    def clean(self):
        if self.materia:
            existing = Corte.objects.filter(materia=self.materia).exclude(pk=self.pk).count()
            if existing >= 4:
                raise ValidationError("Una materia no puede tener más de 4 cortes.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Nota(BaseModel):
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    descripcion = models.TextField(blank=True)
    corte = models.ForeignKey(Corte, on_delete=models.CASCADE, related_name='notas')

    def __str__(self):
        return f"{self.valor} ({self.corte})"

    def clean(self):
        if self.corte:
            existing = Nota.objects.filter(corte=self.corte).exclude(pk=self.pk).count()
            if existing >= 2:
                raise ValidationError("Un corte no puede tener más de 2 notas.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Evaluacion(BaseModel):
    tipo = models.CharField(max_length=255, blank=True, help_text="Ej: Parcial, Tarea, Recuperación")
    puntuacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,help_text="Si se omite, se asigna el valor de la nota asociada")
    nota = models.ForeignKey(Nota, on_delete=models.CASCADE, related_name='evaluaciones')
    
    #? Porque shit tan grande XDDDD
    archivo = models.FileField(blank=True,
        upload_to=generar_ruta_evaluacion, 
        validators=[
            FileExtensionValidator(allowed_extensions=[
                # Documentos y Administración
                'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'csv',
                
                # Diseño Gráfico (Entregables y recursos)
                'png', 'jpg', 'jpeg', 'svg', 'tiff', 'psd', 'ai', 'indd',
                
                # Marketing y Multimedia
                'mp4', 'mov', 'gif', 'zip', 'rar'
            ])
        ],
        help_text="Formatos permitidos: Documentos, Diseños (AI, PSD), Imágenes y Video corto."
    )

    def __str__(self):
        return f"{self.tipo} - {self.puntuacion} ({self.nota})"

    def clean(self):
        if self.nota:
            existing = Evaluacion.objects.filter(nota=self.nota).exclude(pk=self.pk).count()
            if existing >= 2:
                raise ValidationError("Una nota no puede tener más de 2 evaluaciones.")

    def save(self, *args, **kwargs):
        if (self.puntuacion is None or self.puntuacion == '') and self.nota:
            self.puntuacion = self.nota.valor
        self.full_clean()
        super().save(*args, **kwargs)

# --- SEÑALES PARA LIMPIEZA DE ARCHIVOS ---

@receiver(post_delete, sender=Evaluacion)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Borra el archivo físico del almacenamiento cuando se elimina
    el objeto Evaluacion de la base de datos.
    """
    if instance.archivo:
        if os.path.isfile(instance.archivo.path):
            os.remove(instance.archivo.path)

@receiver(pre_save, sender=Evaluacion)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Borra el archivo antiguo del almacenamiento cuando se actualiza
    el objeto Evaluacion con un nuevo archivo.
    """
    if not instance.pk:
        return False

    try:
        old_file = Evaluacion.objects.get(pk=instance.pk).archivo
    except Evaluacion.DoesNotExist:
        return False

    new_file = instance.archivo
    if not old_file == new_file:
        if old_file and os.path.isfile(old_file.path):
            os.remove(old_file.path)
