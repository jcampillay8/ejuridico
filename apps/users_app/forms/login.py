from django.forms import ModelForm
from django import forms
from apps.users_app.models import Administrator, User



#construimos un form usando las librerías de django ( que no depende de un objeto proveniente de models)
class LoginAdministrator(forms.Form): # LoginForm hereda de (forms.Form) porque es un formulario que no viene de un models!!!
    email_admin = forms.EmailField(
        label = "Email", 
        widget= forms.TextInput(attrs = {"class":"form-control ", "style":"width: 300px;"}), 
        max_length=50, required=True,
        )


    password_admin = forms.CharField(
        label = "Contraseña",
        widget= forms.PasswordInput(attrs = {"class":"form-control ", "style":"width: 300px;"}),
        required=True,
        )

    def login(self, request):
        # comprueba sus validaciones (las que definí arriba)
        email_admin = self.cleaned_data.get('email_admin') 
        password_admin = self.cleaned_data.get('password_admin')
        user = Administrator.authenticate(email_admin, password_admin)  
        return user 



class LoginUser(forms.Form): # LoginForm hereda de (forms.Form) porque es un formulario que no viene de un models!!!
    email_user = forms.EmailField(
        label = "Email", 
        widget= forms.TextInput(attrs = {"class":"form-control ", "style":"width: 300px;"}),
        max_length=50, required=True,
        )

    password_user = forms.CharField( 
        label = "Contraseña",
        widget= forms.PasswordInput(attrs = {"class":"form-control ", "style":"width: 300px;"}),
        required=True
        )


    def login(self, request):
        # comprueba sus validaciones (las que definí arriba)

        email_user = self.cleaned_data.get('email_user') 
        password_user = self.cleaned_data.get('password_user')
        user = User.authenticate(email_user, password_user)  
        return user 