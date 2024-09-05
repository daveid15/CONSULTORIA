from .forms import UserCreationFormWithEmail, EmailForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render,redirect,get_object_or_404, render_to_response
from django import forms
from .models import Profile
from django.core.mail import send_mail
from django.http import HttpResponse

from django.conf import settings #importamos el archivo settings, para usar constantes declaradas en él
from django.core.mail import EmailMultiAlternatives #libreria para el envio de correos

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'
    
    def get_form(self, form_class=None):
        form = super(SignUpView,self).get_form()
        #modificamos en tiempo real
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'Nombre de usuario'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2','placeholder':'Dirección de correo'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2','placeholder':'Ingrese su contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2','placeholder':'Re ingrese su contraseña'})    
        return form

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):

    success_url = reverse_lazy('profile')
    template_name = 'registration/profiles_form.html'

    def get_object(self):
        #recuperasmo el objeto a editar
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('check_group_main')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        #recuperasmo el objeto a editar
        return self.request.user
    
    def get_form(self, form_class=None):
        form = super(EmailUpdate,self).get_form()
        #modificamos en tiempo real
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2','placeholder':'Dirección de correo'})
        return form
@login_required
def profile_edit(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        phone = request.POST.get('phone')
        User.objects.filter(pk=request.user.id).update(first_name=first_name)
        User.objects.filter(pk=request.user.id).update(last_name=last_name)
        Profile.objects.filter(user_id=request.user.id).update(phone=phone)
        Profile.objects.filter(user_id=request.user.id).update(mobile=mobile)
        messages.add_message(request, messages.INFO, 'Perfil Editado con éxito') 
    profile = Profile.objects.get(user_id = request.user.id)
    template_name = 'registration/profile_edit.html'
    return render(request,template_name,{'profile':profile})



@login_required
def send_mail_ejemplo1(request):
    subject = 'hola'
    message = 'hola correo.'
    from_email = 'tu_correo@gmail.com'
    to_email = ['pedrozzlp@gmail.com']
    send_mail(subject, message, from_email, to_email)
    template_name = 'registration/password_reset_done'
    return render(request,template_name)
 
 
"""@login_required
def ejemplos_correo1(request):
    #llamos al metodo que envia el correo
    send_mail_ejemplo1(request,'rene@softiago.cl','dato por parametro ejemplo')
    messages.add_message(request, messages.INFO, 'correo enviado')
    return redirect('ejemplos_main')"""   

@login_required
def ejemplos_correo1(request,mail_to,data_1):
    #Ejemplo que permite enviar un correo solo con texto, el metodo, recibe por parametro la información para su ejecución    
    from_email = settings.DEFAULT_FROM_EMAIL #exporta desde el settings.py, el correo de envio por defecto
    subject = "Asunto del correo"    
    html_content = """
                    <html>
                        <head>
                            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                        </head>
                         <body>
                            <h3>Estimad@</h3>
                            <p>Es es el cuerpo que agrega el dato por parametro """+str(data_1)+""" mas texto .</p>
                            <p>otro párrafo</p>
                            <br/>
                            <p>Le saluda</p>
                            <p>Equipo de soluciones pyme.</p>
                            <br/>
                            <p><small>Correo generado automáticamente, por favor no responder.<small></p>
                        </body>
                    </html>            
                """
    msg = EmailMultiAlternatives(subject, html_content, from_email, [mail_to])
    msg.content_subtype = "html"
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@login_required
def ejemplos_correo2(request):
    #llamos al metodo que envia el correo
    send_mail_ejemplo2(request,'rene@softiago.cl','Ejemplo 2 con archivo')
    messages.add_message(request, messages.INFO, 'correo enviado')
    return redirect('ejemplos_main')   

@login_required
def ejemplos_correo2(request):
    #llamos al metodo que envia el correo
    send_mail_ejemplo2(request,'rene@softiago.cl','Ejemplo 2 con archivo')
    messages.add_message(request, messages.INFO, 'correo enviado')
    return redirect('ejemplos_main')   

@login_required
def send_mail_ejemplo2(request,mail_to,data_1):
    #Ejemplo que permite enviar un correo agregando un excel creado con info de la bd

    #archivo
    import os #debe ubicarlo en el inicio del archivo
    from email.mime.multipart import MIMEMultipart #debe ubicarlo en el inicio del archivo
    from email.mime.text import MIMEText #debe ubicarlo en el inicio del archivo
    from email.mime.base import MIMEBase #debe ubicarlo en el inicio del archivo
    from email import encoders #debe ubicarlo en el inicio del archivo

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#directorio base del proyecto en el servidor
    BASE_PATH = os.path.join(BASE_DIR,"core","static","core")#lugar donde se guarda el archivo
    file_name = "nombre_archivo.xls"#trate de que no se muy largo
    file_send = BASE_PATH+"/"+file_name
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Agenda')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True   
    columns = ['Habilidad','Tipo']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    time_format = xlwt.XFStyle()
    time_format.num_format_str = 'hh:mm:ss'   
    rows = Habilidad.objects.all().order_by('nombre')         
    for row in rows:
        row_num += 1
        for col_num in range(len(columns)):
            if col_num == 0:
                ws.write(row_num, col_num, row.nombre, date_format)
            if col_num == 1:
                ws.write(row_num, col_num, row.nivel, font_style)                                               
    wb.save(file_send)  
    #fin archivo
    from_email = settings.DEFAULT_FROM_EMAIL #exporta desde el settings.py, el correo de envio por defecto
    subject = "Asunto del correo"    
    html_content = """
                    <html>
                        <head>
                            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                        </head>
                        <body>
                            <h3>Estimad@</h3>
                            <p>Es es el cuerpo que agrega el dato por parametro """+str(data_1)+""" mas texto .</p>
                            <p><small>Correo generado automáticamente, por favor no responder.<small></p>
                        </body>
                    </html>            
                """
    msg = EmailMultiAlternatives(subject, html_content, from_email, [mail_to])
    msg.content_subtype = "html"
    msg.attach_alternative(html_content, "text/html")

    msg = EmailMultiAlternatives(subject, html_content, from_email, [mail_to])
    msg.content_subtype = "html"
    archivo_adjunto = open(file_send,'rb')
    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto    
    adjunto_MIME.add_header('Content-Disposition',"attachment; filename= %s" % file_name)
    # Y finalmente lo agregamos al mensaje
    msg.attach(adjunto_MIME)


    msg.send()
