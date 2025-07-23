from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings

# Create your models here.
class Tutoriais(models.Model):
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    descricao = models.TextField()
    
    # Main content sections with default values
    introducao = CKEditor5Field(
        verbose_name="Introdução",
        default="<h2>Introdução</h2><p>Nesta seção, apresente o tema do tutorial e seus objetivos principais.</p>",
        config_name='extends'
    )
    conceitos = CKEditor5Field(
        verbose_name="Conceitos Básicos",
        default="<h2>Conceitos Básicos</h2><p>Explique os conceitos fundamentais necessários para entender o tutorial.</p>",
        config_name='extends'
    )
    exemplos = CKEditor5Field(
        verbose_name="Exemplos Práticos",
        default="<h2>Exemplos Práticos</h2><pre><code class='language-python'># Adicione exemplos de código aqui</code></pre>",
        config_name='extends'
    )
    conclusao = CKEditor5Field(
        verbose_name="Conclusão",
        default="<h2>Conclusão</h2><p>Resuma os principais pontos abordados e sugira próximos passos.</p>",
        config_name='extends'
    )
    
    # Additional fields
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tutoriais')
    imagem = models.ImageField(upload_to='escola/static/escola/imagens/tutoriais/', blank=True, null=True)
    categoria = models.CharField(max_length=50, default="Python", 
                               choices=[
                                   ("Python", "Python"),
                                   ("Django", "Django"),
                                   ("Flask", "Flask"),
                                   ("Data Engineering", "Data Engineering"),
                                   ("Java Script", "Java Script"),
                                   ("Go", "Go"),
                                   ("Linux", "Linux"),
                                   ("Machine Learning", "Machine Learning"),
                                   ("BioPython", "BioPython"),
                                   ("Data Science", "Data Science"),
                                   ("Web Development", "Web Development"),
                                    ("PostgreSQL", "PostgreSQL"),
                                    ("MySQL", "MySQL"),
                                    ("MongoDB", "MongoDB"),
                                    ("Docker", "Docker"),
                                    ("Kubernetes", "Kubernetes"),
                                    ("Git", "Git"),
                                    ("GitHub", "GitHub"),
                                    ("CI/CD", "CI/CD"),
                                    ("DevOps", "DevOps"),
                                    ("Cloud Computing", "Cloud Computing"),
                               ])
    nivel = models.CharField(max_length=20, default="Iniciante",
                           choices=[
                               ("Iniciante", "Iniciante"),
                               ("Intermediário", "Intermediário"),
                               ("Avançado", "Avançado"),
                           ])

    # Slug serve para deixar a URL mais amigável (Ao invés de tutorial/5, fica tutorial/postgres-tutorial)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Tutorial"
        verbose_name_plural = "Tutoriais"
        ordering = ['-data_criacao']

