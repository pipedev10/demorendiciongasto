from django.contrib import admin
from .models import  RendicionEstado,Rendicion,Centro,Item

# Register your models here.

admin.site.register(Centro)
admin.site.register(RendicionEstado)
admin.site.register(Rendicion)
admin.site.register(Item)
