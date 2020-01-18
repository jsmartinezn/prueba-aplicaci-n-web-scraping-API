from django.db import models

class Consulta(models.Model):
    nombre = models.CharField(max_length=50)
    numero = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return '%s %s' % (self.nombre, self.numero)
class Respuesta(models.Model):
    titulo = models.CharField(max_length=100)
    precio = models.FloatField(null=True, blank=True, default=None)
    vendidas = models.FloatField(null=True, blank=True, default=None)
    envio = models.CharField(max_length=50)


