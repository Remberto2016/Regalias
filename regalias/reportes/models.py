from django.db import models

class Reportes(models.Model):
    user = models.CharField(max_length=100)
    def __unicode__(self):
        return self.user
    def __str__(self):
        return self.user
    class Meta:
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'