from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.defaulttags import register

from .models import  RendicionEstado,Rendicion,Centro,Item
from .forms import FormRendicion

MSJ_CREATED_OK = "La operación se ha completado correctamente"
MSJ_CREATED_FAIL = "Ha ocurrido un error :(, Intente nuevamente :D"

@login_required
def index(request):
    return render(request,'menu.html')

@staff_member_required
@login_required
def todos_los_centros(request):
    try:
        context = {}
        context['lists'] = Centro.objects.all()
        context['ths'] = ['codigo','nombre']
        context['xheaders'] = ['codigo','nombre']
        context['tipo'] = "centro"
        context['title'] = "Todos los centros"
        return render(request,'lists.html',context)
    except Exception as ex:
        messages.add_message(request, messages.WARNING, "{}. {}".format(MSJ_CREATED_FAIL,ex))
        print(ex)
    return HttpResponseRedirect(reverse('home'))

@staff_member_required
@login_required
def rendiciones_centro(request,id):
    try:
        context = {}
        centro = Centro.objects.get(id=id)
        context['lists'] = Rendicion.objects.filter(centro=centro)
        context['ths'] = ['Monto','Item','Estado','creado por','created_at','Módificado']
        context['xheaders'] = ['monto','item','estado','creado_por','created_at','obtener_ultima_modificacion']
        context['tipo'] = "detalle2"
        context['title'] = "Rendición de {}".format(centro.nombre)
        return render(request,'lists.html',context)
    except Exception as ex:
        messages.add_message(request, messages.WARNING, "{}. {}".format(MSJ_CREATED_FAIL,ex))
    return HttpResponseRedirect(reverse('home'))

@login_required    
def detalle_rendicion(request,id):
    try:
        context = {}
        context['lists'] = RendicionEstado.objects.filter(rendicion=id)
        context['ths'] = ['Estado','Módificado','Por','comentario']
        context['xheaders'] = ['rn_estado','rn_creado','responsable','rn_comentario']
        context['detalle'] = RendicionEstado.objects.filter(rendicion=id).order_by('-id')[0]
        return render(request,'detalle.html',context)
    except Exception as ex:
        messages.add_message(request, messages.WARNING, "{}. {}".format(MSJ_CREATED_FAIL,ex))
    return HttpResponseRedirect(reverse('home'))


@staff_member_required
@login_required
def aprobar_rendicion(request,id):
    try:
        if request.POST:
            re = RendicionEstado(comentario=request.POST.get('comentario',''),estado=request.POST.get('estado','RE') ,responsable=request.user, rendicion=Rendicion.objects.get(id=id))
            re.save()
            return HttpResponseRedirect(reverse('detalle_rendicion',kwargs={'id':id}))
            messages.add_message(request, messages.SUCCESS, MSJ_CREATED_OK)
    except Exception as ex:
        messages.add_message(request, messages.WARNING, "{}. {}".format(MSJ_CREATED_FAIL,ex))
    return HttpResponseRedirect(reverse('home'))


@login_required
def mis_rendiciones(request):
    try:
        context = {}
        context['ths'] = ['$Monto','Item','Estado','Centro','created_at','Módificado']
        context['xheaders'] = ['monto','item','estado','centro','created_at','obtener_ultima_modificacion']
        context['lists'] = RendicionEstado.objects.filter(responsable=request.user).filter(estado="CR")
        context['tipo'] = "detalle"
        return render(request,'lists.html',context)
    except Exception as ex:
        messages.add_message(request, messages.WARNING, "{}. {}".format(MSJ_CREATED_FAIL,ex))
    return HttpResponseRedirect(reverse('home'))
@login_required
def solicitar_re_evaluar(request,id):
    try:
        if request.POST:
            re = RendicionEstado(comentario=request.POST.get('comentario',''),estado='RV' ,responsable=request.user, rendicion=Rendicion.objects.get(id=id))
            re.save()
            messages.add_message(request, messages.SUCCESS, MSJ_CREATED_OK)
            return HttpResponseRedirect(reverse('detalle_rendicion',kwargs={'id':id}))
    except Exception as ex:
        messages.add_message(request, messages.WARNING, "{}. {}".format(MSJ_CREATED_FAIL,ex))
    return HttpResponseRedirect(reverse('home'))


@login_required
def crear_rendiciones(request):
    try:
        context = {}
        context['title'] = "Crear rendición"
        if request.POST:
            form = FormRendicion(request.POST, request.FILES)
            if form.is_valid:
                elemento = form.save(commit=False)
                elemento.save()
                re = RendicionEstado(estado="CR",comentario="Se ha creado con exito",responsable=request.user,rendicion=elemento)
                re.save()
                messages.add_message(request, messages.SUCCESS, MSJ_CREATED_OK)
                return HttpResponseRedirect(reverse('mis_rendiciones'))
            messages.add_message(request, messages.WARNING, MSJ_CREATED_FAIL)
            context['form'] = form
        else:
            context['form'] = FormRendicion()
        return render(request,'add.html',context)
    except Exception as ex:
        messages.add_message(request, messages.WARNING, "{}. {}".format(MSJ_CREATED_FAIL,ex))
    return HttpResponseRedirect(reverse('home'))


@register.filter
def get_item(dictionary, key):
    return dictionary.to_dict().get(key)

@register.filter
def get_class(value):
  return value.__class__.__name__

def login(request):
    return render(request, 'registration/login.html', {})


def error_404_view(request, exception):
    response = render_to_response('error_404.html', {})
    response.status_code = 404
    return response