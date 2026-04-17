import os
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from notas.models import BaseModel, Materia

def generar_ruta_apunte(instance, filename):
    """Ruta: biblioteca/usuario/materia/archivo.ext"""
    estudiante = instance.estudiante.username
    materia_slug = instance.materia.nombre.replace(" ", "_").lower()
    return f'biblioteca/{estudiante}/{materia_slug}/{filename}'

# Create your models here.
class Apunte(BaseModel):
    titulo = models.CharField(max_length=255, blank=True, null=True)
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='apuntes')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='apuntes')
    descripcion = models.TextField(blank=True, null=True)
    
    #? Porque shit tan grande XDDDD
    archivo = models.FileField(blank=True,
        upload_to=generar_ruta_apunte, 
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
        return self.titulo if self.titulo else "Apunte sin título"

# --- SEÑALES PARA LIMPIEZA DE ARCHIVOS (BIBLIOTECA) ---

@receiver(post_delete, sender=Apunte)
def auto_delete_file_on_delete_biblioteca(sender, instance, **kwargs):
    if instance.archivo:
        if os.path.isfile(instance.archivo.path):
            os.remove(instance.archivo.path)

@receiver(pre_save, sender=Apunte)
def auto_delete_file_on_change_biblioteca(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = Apunte.objects.get(pk=instance.pk).archivo
    except Apunte.DoesNotExist:
        return False
    new_file = instance.archivo
    if not old_file == new_file:
        if old_file and os.path.isfile(old_file.path):
            os.remove(old_file.path)