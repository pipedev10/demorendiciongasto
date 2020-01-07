from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.layout import Submit

from .models import  RendicionEstado,Rendicion,Centro,Item

class FormRendicion(forms.ModelForm):
    class Meta:
        model = Rendicion
        fields = ( 'centro', 'item', 'tipo_de_documento','monto','comentario','comprobante')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar'))

