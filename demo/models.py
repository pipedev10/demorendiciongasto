from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    def __str__(self):
        return "{}".format(self.nombre)

class Centro(models.Model):
    nombre = models.CharField(max_length=150)
    codigo = models.IntegerField()
    def to_dict(self):
        return {
            'nombre': self.nombre,
            'codigo':self.codigo
        }
    def __str__(self):
        return "{} {}".format(self.codigo,self.nombre)

class CentroUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    def to_dict(self):
        return {
            'usuario': self.usuario,
            'centro':self.centro
        }

class Rendicion(models.Model):
    TIPOS_DOCUMENTOS = (
        ('BO','BOLETA'),
        ('FA','FACTURA'),
        ('BE','BOLETA ELECTRÓNICA'),
        ('FE','FACTURA ELECTRÓNICA'),
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE,
    help_text='Seleccione el centro al cual corresponde',
    verbose_name = 'Centro')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    monto = models.IntegerField(
        help_text='Ingrese un monto',
    verbose_name = 'Monto')
    tipo_de_gasto = models.CharField(max_length=50,
    help_text='Ingrese el tipo de gasto',
    verbose_name = 'Tipos de gasto')
    tipo_de_documento = models.CharField(
        max_length=2,
        choices=TIPOS_DOCUMENTOS,
        default='BO',
    )
    comentario = models.TextField(max_length=250)
    comprobante = models.ImageField(upload_to="boletas/",
    help_text='Suba el comprobante de la compra',
    verbose_name = 'Comprobante')
    def obtener_estado_final(self):
        return RendicionEstado.objects.filter(rendicion=self).order_by('-id')[0].get_estado_display()
    def obtener_ultima_modificacion(self):
        return RendicionEstado.objects.filter(rendicion=self).order_by('-id')[0].created_at
    def obtener_creado(self):
        usr = RendicionEstado.objects.filter(rendicion=self).filter(estado="CR")[0].responsable
        print(usr)
        return "{} {}".format(usr.first_name,usr.last_name)
    def to_dict(self):
        return {
            'item': self.item,
            'centro':self.centro,
            'created_at':self.created_at,
            'id':self.id,
            'creado_por': self.obtener_creado(),
            'updated_at':self.updated_at,
            'monto':self.monto,
            'tipo_de_gasto':self.tipo_de_gasto,
            'tipo_de_documento':self.tipo_de_documento,
            'comentario':self.comentario,
            'comprobante':self.comprobante.url,
            'estado':self.obtener_estado_final(),
            'obtener_ultima_modificacion':self.obtener_ultima_modificacion()
            
        }

class RendicionEstado(models.Model):
    ESTADOS =  (
        ('CR','Creado'),
        ('RV','Re Validar'),
        ('RE','Rechazado'),
        ('AP','Aprobado'),
    )
    estado  = models.CharField(
        max_length=2,
        choices=ESTADOS,
        default='CR',
    )
    comentario = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE)
    rendicion = models.ForeignKey(Rendicion, on_delete=models.CASCADE)
    def to_dict(self):
        return {
            'estado': self.estado,
            'responsable': "{} {}".format(self.responsable.first_name,self.responsable.last_name),
            'rendicion':self.rendicion,
            'item': self.rendicion.item,
            'centro':self.rendicion.centro,
            'created_at':self.rendicion.created_at,
            'rn_creado':self.created_at,
            'rn_estado':self.get_estado_display(),
            'rn_comentario':self.comentario,
            'id':self.rendicion.id,
            'creado_por': self.rendicion.obtener_creado(),
            'updated_at':self.rendicion.updated_at,
            'monto':self.rendicion.monto,
            'tipo_de_gasto':self.rendicion.tipo_de_gasto,
            'tipo_de_documento':self.rendicion.tipo_de_documento,
            'comentario':self.rendicion.comentario,
            'comprobante':self.rendicion.comprobante.url,
            'estado':self.rendicion.obtener_estado_final(),
            'centro':self.rendicion.centro.nombre,
            'obtener_ultima_modificacion':self.rendicion.obtener_ultima_modificacion()
        }
   

