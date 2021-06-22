from apps.users_app.models import Administrator
from django.shortcuts import render, redirect
from apps.users_app.forms.register import AdministratorForm
from apps.users_app.forms.login import LoginAdministrator, LoginUser
from apps.secr_app.forms.new_lawsuit import DefendantForm, LawsuitForm
from .makedata import make_user_type, make_lawsuit_state, make_court



def index(request):
    print("entra acá"*10)
    if  'id'  in request.session and 'user_type' in request.session: # hay sesión iniciada?
        if  request.session['user_type'] == "administrator": #es administrador? redirige a la app admin_app
            return redirect( '/administrator')
        if  request.session['user_type'] == "secretaria": #es secretaria? redirige a la app secr_app
            return redirect( '/secretary')
        if  request.session['user_type'] == "procuradora": #es procuradora? redirige a la app proc_app
            return redirect( '/procuradora')
    #si no hay sesión iniciada--------------------------------

    loginadministratorform = LoginAdministrator() 
    loginuserform = LoginUser()
    context = {
        'loginadministratorform' : loginadministratorform,
        'loginuserform' : loginuserform,
    }
    return render(request, 'landing.html', context)





def login_administrator(request):   #LOGIN ADMINISTRADOR
    loginadministratorform = LoginAdministrator(request.POST)
    loginuserform = LoginUser()
    if loginadministratorform.is_valid():
        this_user = loginadministratorform.login(request.POST)
        if this_user:
            print("Login satisfactorio")
            request.session['id'] = this_user.id
            request.session['user_type'] = "administrator"
            return redirect('/administrator') 
   # si no es válido render template del mismo form
    context = {
        'loginadministratorform': loginadministratorform,
        'loginuserform': loginuserform,
        'error_login_admin' : 'Usuario y/o contraseña incorrecto'
    }
    
    return render(request, 'landing.html', context)


def login_user(request): #LOGIN SECRETARIA Y PROCURADORA
    loginadministratorform = LoginAdministrator() 
    loginuserform = LoginUser(request.POST)
    print()
    if loginuserform.is_valid():
        this_user = loginuserform.login(request.POST)
        if this_user:
            request.session['id'] = this_user.id
            request.session['user_type'] = this_user.type.type_name
            

            if request.session['user_type'] == "secretaria":
                print("es secretaria")
                return redirect('/secretary')

            if request.session['user_type'] == "procuradora":
                print("es procuradora")
                return redirect('/procuradora')

        print("Login satisfactorio")
                
        
        # si no es válido render template del mismo form
      
    context = {
        'loginadministratorform': loginadministratorform,
        'loginuserform': loginuserform,
        'error_login_user' : 'Usuario y/o contraseña incorrecto'
    }
    return render(request, 'landing.html', context)



    

def make_administrator(request): # si es get, despliega el formulario para ingresar nuevo administrador/ si es post, verifica validación y guarda nuevo administrador
    if request.method == 'GET':
        administratorform = AdministratorForm()
        context = {
            'administratorform' : administratorform,
        }
        return render(request, 'make_administrator.html', context)

    else: # si es post
        administratorform = AdministratorForm(request.POST)
        if administratorform.is_valid():
            print('---el form es válido---')
            new_admin = administratorform.save()
            request.session['id'] = new_admin.id
            request.session['user_type'] = "administrator"

            return redirect('/administrator')
        else:
            print("--- el form NO es valido ----")

            context = {
                'administratorform' : administratorform,
            }

            return render(request, 'make_administrator.html', context)



def logout(request):
    request.session.delete()
    return redirect('/')


def makedata(request):
    make_user_type()
    make_lawsuit_state()
    make_court()

    return redirect('/')