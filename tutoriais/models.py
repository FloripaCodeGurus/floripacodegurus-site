from django.db import models
from django.utils.text import slugify

# Create your models here.
class Tutoriais(models.Model):
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    descricao = models.TextField()
    texto_principal = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    autor = models.CharField(max_length=50)
    imagem = models.ImageField(upload_to='tutoriais_imagens/', blank=True, null=True)


    # Slug serve para deixar a URL mais amigável (Ao invés de tutorial/5, fica tutorial/postgres-tutorial)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

