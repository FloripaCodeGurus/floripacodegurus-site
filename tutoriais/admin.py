from django.contrib import admin
from .models import Tutoriais

# Register your models here.
@admin.register(Tutoriais)
class TutoriaisAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_criacao', 'data_atualizacao')
    search_fields = ('titulo', 'descricao', 'texto_principal', 'autor')
    prepopulated_fields = {'slug': ('titulo',)}
    list_filter = ('autor', 'data_criacao')
    
