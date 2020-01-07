from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from demo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path('^password_reset/$', auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        html_email_template_name="registration/password_reset_email.html",
    ),
    name='password_reset'),
    path('todos_los_centros/',views.todos_los_centros,name="todos_los_centros"),
    path('crear_rendiciones/',views.crear_rendiciones,name="crear_rendiciones"),
    path('rendiciones_centro/<int:id>/',views.rendiciones_centro,name="rendiciones_centro"),
    path('detalle_rendicion/<uuid:id>/',views.detalle_rendicion,name="detalle_rendicion"),
    path('mis_rendiciones/',views.mis_rendiciones,name="mis_rendiciones"),
    path('login/',views.login,name="login"),
    path('home/',views.index,name="home"),
    path('aprobar_rendicion/<uuid:id>/',views.aprobar_rendicion,name="aprobar_rendicion"),
    path('solicitar_re_evaluar/<uuid:id>/',views.solicitar_re_evaluar,name="solicitar_re_evaluar"),
    
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)