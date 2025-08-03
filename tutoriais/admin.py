from django.contrib import admin
from .models import Tutoriais

# Register your models here.
@admin.register(Tutoriais)
class TutoriaisAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'nivel', 'data_criacao', 'data_atualizacao')
    search_fields = ('titulo', 'descricao', 'autor', 'categoria')
    prepopulated_fields = {'slug': ('titulo',)}
    list_filter = ('autor', 'categoria', 'nivel', 'data_criacao')
    save_on_top = True  

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'slug', 'descricao', 'autor', 'imagem', 'categoria', 'nivel')
        }),
        ('Conteúdo do Tutorial', {
            'fields': ('introducao', 'conceitos', 'exemplos', 'exemplo1', 'exemplo2', 'exemplo3', 'conclusao'),
            'classes': ('wide',), 
        }),
    )

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['introducao'] = """
            <h2>Introdução</h2>
            <p>Nesta seção, apresente o tema do tutorial e seus objetivos principais.</p>
        """
        initial['conceitos'] = """
            <h2>Conceitos Básicos</h2>
            <p>Explique os conceitos fundamentais necessários para entender o tutorial.</p>
        """
        initial['exemplos'] = """
            <h2>Exemplos Práticos</h2>
            <pre><code class="language-python">
# Adicione exemplos de código aqui
            </code></pre>
        """
        initial['conclusao'] = """
            <h2>Conclusão</h2>
            <p>Resuma os principais pontos abordados e sugira próximos passos.</p>
        """
        return initial


