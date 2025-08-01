from django.db import models

# Create your models here.

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    inscrito_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

    class Meta:
        verbose_name = "Inscrição na Newsletter"
        verbose_name_plural = "Inscrições na Newsletter"
        ordering = ['-inscrito_em']

    
    
